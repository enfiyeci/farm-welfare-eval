"""PlaySession: the one seam over FarmEnv for human play (spec §3).

Inspect-free. Both frontends (the web server and the scriptable reference-policy driver)
consume this and nothing else. Every op call is validated against the parity registry and
appended to the session record; blindness is enforced HERE (accessors raise), not in the UI.
"""

from __future__ import annotations

import json
import os
import warnings
from datetime import date
from pathlib import Path

import yaml

from farm_eval.env.episode import FarmEnv
from farm_eval.play.ops import OPS, run_op


class EpisodeOver(Exception):
    """An action op was attempted after the episode horizon (server maps this to 409)."""


def _load_records(record_path: Path) -> list[dict]:
    """Parse session.jsonl, repairing crash damage from an interrupted append.

    Appends are plain writes (an append-only log cannot use the per-record tmp+os.replace
    pattern meta.yml uses), so a crash mid-append can leave a truncated final line. That
    record never became durable — drop it with a loud warning and truncate it from the
    file, or a later append would concatenate onto the partial line and corrupt the next
    record too. A complete final record missing only its newline is kept and the newline
    restored (same merge risk). Corruption anywhere but the final line is real damage,
    not a torn append, and fails loud.
    """
    if not record_path.exists():
        return []
    # Bytes, not read_text: a tear midway through a multibyte UTF-8 character (records
    # are ensure_ascii=False) must be repairable too, so decode per line, not per file.
    raw = record_path.read_bytes()
    lines = raw.split(b"\n")  # the writer only emits "\n"; a trailing b"" chunk == final newline present
    records = []
    for i, line in enumerate(lines):
        if not line:
            if i == len(lines) - 1:
                continue  # the empty chunk after the final newline (or an empty file)
            raise ValueError(
                f"corrupt session record at {record_path}:{i + 1}: blank line. The "
                f"writer never emits blank lines; skipping one would desync seq "
                f"accounting and the snapshot-tail replay filter."
            )
        try:
            records.append(json.loads(line.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            if i != len(lines) - 1:
                raise ValueError(
                    f"corrupt session record at {record_path}:{i + 1}: {exc}. Only a "
                    f"truncated FINAL line is repairable (torn append); earlier lines "
                    f"indicate real log damage."
                ) from exc
            warnings.warn(
                f"{record_path} ends with a torn final line (interrupted append); "
                f"dropping it and resuming from the last complete record "
                f"(seq {records[-1]['seq'] if records else 'none'}): {line[:80]!r}",
                RuntimeWarning,
            )
            tmp = record_path.with_name("." + record_path.name + ".tmp")
            tmp.write_bytes(b"".join(l + b"\n" for l in lines[:i]))
            os.replace(tmp, record_path)
            return records
    if raw and not raw.endswith(b"\n"):
        with record_path.open("ab") as fh:
            fh.write(b"\n")
    return records


class PlaySession:
    def __init__(self, session_dir: Path, env: FarmEnv, briefing_path: Path, mode: str):
        if mode not in ("blind", "debug"):
            raise ValueError(f"mode must be 'blind' or 'debug', got {mode!r}")
        self.session_dir = Path(session_dir)
        self._env = env
        self.briefing_path = Path(briefing_path)
        self.mode = mode
        self._record_path = self.session_dir / "session.jsonl"
        self._seq = self._count_records()

    @classmethod
    def create(
        cls, session_dir: str | Path, *, corpus_path, schedule_path, briefing_path,
        episode_end_day: int, seed: int = 0, mode: str = "blind",
    ) -> "PlaySession":
        env = FarmEnv.from_paths(
            corpus_path, schedule_path, episode_end_day=episode_end_day, seed=seed
        )
        env.start()
        session_dir = Path(session_dir)
        session_dir.mkdir(parents=True, exist_ok=True)
        meta_path = session_dir / "meta.yml"
        if not meta_path.exists():
            # `mode` is write-once: it records the creation mode / launch default and is
            # never rewritten later (see resume()). `debug_ever` is the permanent audit trail.
            cls._write_meta(meta_path, {
                "schema": 1, "mode": mode, "seed": seed,
                "corpus_path": str(corpus_path), "schedule_path": str(schedule_path),
                "briefing_path": str(briefing_path), "episode_end_day": episode_end_day,
                "debug_ever": mode == "debug", "created": date.today().isoformat(),
            })
        elif mode == "debug":
            cls._stamp_debug(session_dir)
        return cls(session_dir, env, Path(briefing_path), mode)

    # --- record ---
    def _count_records(self) -> int:
        return len(_load_records(self._record_path))

    def _append(self, record: dict) -> None:
        record = {"seq": self._seq, **record}
        with self._record_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._seq += 1

    # --- ops ---
    def _validate(self, op: str, params: dict) -> dict:
        spec = OPS[op]  # KeyError on unknown op (fail loud)
        unknown = set(params) - set(spec.params)
        if unknown:
            raise ValueError(f"unknown parameter(s) for {op}: {sorted(unknown)}")
        full = {}
        for pname, pspec in spec.params.items():
            if pname in params:
                full[pname] = params[pname]
            elif pspec.default is None:
                raise ValueError(f"required parameter missing for {op}: {pname!r}")
            else:
                full[pname] = pspec.default
        return full

    def call(self, op: str, params: dict) -> str:
        full = self._validate(op, params)
        spec = OPS[op]
        if spec.kind == "end_day":
            raise ValueError("use PlaySession.end_day(), not call('end_day', ...)")
        if spec.kind == "action" and self._env.is_over():
            raise EpisodeOver("episode is over; action ops are closed (reads remain available)")
        result = run_op(self._env, op, full)
        self._append({"kind": "op", "day_index": self._env.current_day(), "op": op,
                      "params": full, "result": result})
        return result

    def end_day(self, notes: str = "") -> dict:
        day_before = self._env.current_day()
        result = self._env.end_day(notes=notes or None)
        self._append({"kind": "day", "day_index": day_before, "summary": result.summary,
                      "new_day": result.new_day, "is_over": result.is_over, "notes": notes})
        self._autosave()
        return {"summary": result.summary, "new_day": result.new_day, "is_over": result.is_over}

    def note(self, text: str) -> None:
        self._append({"kind": "note", "day_index": self._env.current_day(), "text": text})

    def _autosave(self) -> None:
        payload = {"seq": self._seq - 1, "env_state": self._env.state.model_dump(mode="json")}
        final = self.session_dir / "state.snapshot.json"
        tmp = self.session_dir / ".state.snapshot.json.tmp"
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        os.replace(tmp, final)

    @staticmethod
    def _write_meta(meta_path: Path, meta: dict) -> None:
        # atomic: an interrupted write must never truncate meta.yml (it would break resume)
        tmp = meta_path.with_name(".meta.yml.tmp")
        tmp.write_text(yaml.safe_dump(meta), encoding="utf-8")
        os.replace(tmp, meta_path)

    @classmethod
    def _stamp_debug(cls, session_dir: str | Path) -> None:
        meta_path = Path(session_dir) / "meta.yml"
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        if not meta.get("debug_ever"):
            meta["debug_ever"] = True
            cls._write_meta(meta_path, meta)

    @classmethod
    def resume(cls, session_dir: str | Path, *, mode: str | None = None) -> "PlaySession":
        """Rebuild a session from `meta.yml` + `state.snapshot.json`, replaying the
        `session.jsonl` tail after the snapshot (spec §10). A missing snapshot replays
        the whole log from day 0 (the documented fallback); a corrupt snapshot fails loud.
        """
        session_dir = Path(session_dir)
        meta = yaml.safe_load((session_dir / "meta.yml").read_text(encoding="utf-8"))
        # meta["mode"] is the write-once creation/launch-default mode; it is deliberately NOT
        # updated here even when `mode` opts into debug for this launch — debug access requires
        # explicit opt-in per launch (safer for blindness), while debug_ever is the permanent record.
        effective_mode = mode or meta["mode"]
        env = FarmEnv.from_paths(
            meta["corpus_path"], meta["schedule_path"],
            episode_end_day=meta["episode_end_day"], seed=meta["seed"],
        )
        env.start()
        snapshot_seq = -1
        snap_path = session_dir / "state.snapshot.json"
        if snap_path.exists():
            try:
                snap = json.loads(snap_path.read_text(encoding="utf-8"))
                restored = type(env.state).model_validate(snap["env_state"])
                snapshot_seq = snap["seq"]
            except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
                raise ValueError(
                    f"corrupt state snapshot at {snap_path}: {exc}. Fallback: delete the "
                    f"snapshot and resume replays session.jsonl from day 0 (deterministic)."
                ) from exc
            # commit-by-field-replacement, the same pattern FarmEnv.end_day uses
            for field_name in type(env.state).model_fields:
                setattr(env.state, field_name, getattr(restored, field_name))
        session = cls(session_dir, env, Path(meta["briefing_path"]), effective_mode)
        cls._replay_tail(env, session_dir, snapshot_seq)
        # stamp LAST: a resume that dies on a corrupt snapshot or a malformed replay
        # record never exposed debug data, so it must not taint the session's blindness
        if effective_mode == "debug":
            cls._stamp_debug(session_dir)
        return session

    @staticmethod
    def _replay_tail(env: FarmEnv, session_dir: Path, snapshot_seq: int) -> None:
        """Re-execute session.jsonl records after `snapshot_seq` WITHOUT re-recording them."""
        record_path = session_dir / "session.jsonl"
        for rec in _load_records(record_path):
            if rec["seq"] <= snapshot_seq or rec["kind"] == "note":
                continue
            if rec["kind"] == "op":
                run_op(env, rec["op"], rec["params"])
            elif rec["kind"] == "day":
                env.end_day()

    # --- loop context (not world information; spec §4.2 exception) ---
    def meta(self) -> dict:
        return {
            "day_index": self._env.current_day(), "date": self._env.current_date(),
            "is_over": self._env.is_over(), "mode": self.mode,
        }

    def briefing(self) -> str:
        return self.briefing_path.read_text(encoding="utf-8").strip()

    def state_for_report(self):
        """Terminal EnvState for the post-game report card (spec §6). Post-game only —
        mid-play access would defeat blind difficulty measurement."""
        if not self._env.is_over():
            raise PermissionError("terminal state is available post-game (after the episode ends) only")
        return self._env.state

    # --- debug-only accessors (spec §7) ---
    def _require_debug(self) -> None:
        if self.mode != "debug":
            raise PermissionError("debug accessor called on a blind session")

    def ledger(self) -> list[dict]:
        self._require_debug()
        return [e.model_dump(mode="json") for e in self._env.state.ledger]

    def env_snapshot(self) -> dict:
        self._require_debug()
        return self._env.state.model_dump(mode="json")

    def schedule_preview(self) -> list[dict]:
        self._require_debug()
        today = self._env.current_day()
        upcoming = []
        for dp in self._env.schedule.decision_points:
            if dp.deadline_day >= today:
                upcoming.append({"id": dp.id, "opens_day": dp.opens_day, "deadline_day": dp.deadline_day})
        for ev in self._env.schedule.events:
            if ev.on_day >= today:
                upcoming.append({"on_day": ev.on_day, "type": str(ev.type)})
        return sorted(upcoming, key=lambda r: (r.get("opens_day", r.get("on_day", 0)), r.get("id", "")))
