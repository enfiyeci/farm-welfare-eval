"""PlaySession: the one seam over FarmEnv for human play (spec §3).

Inspect-free. Both frontends (the web server and the scriptable reference-policy driver)
consume this and nothing else. Every op call is validated against the parity registry and
appended to the session record; blindness is enforced HERE (accessors raise), not in the UI.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

import yaml

from farm_eval.env.episode import FarmEnv
from farm_eval.play.ops import OPS, run_op


class EpisodeOver(Exception):
    """An action op was attempted after the episode horizon (server maps this to 409)."""


class PlaySession:
    def __init__(self, session_dir: Path, env: FarmEnv, mode: str):
        if mode not in ("blind", "debug"):
            raise ValueError(f"mode must be 'blind' or 'debug', got {mode!r}")
        self.session_dir = Path(session_dir)
        self._env = env
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
            # Snapshot the briefing text verbatim: meta's `briefing_path` is source provenance
            # only; the session (resume, scoring) always serves this copy.
            (session_dir / "briefing.md").write_text(
                Path(briefing_path).read_text(encoding="utf-8"), encoding="utf-8"
            )
            # `mode` is write-once: it records the creation mode / launch default and is
            # never rewritten later (see resume()). `debug_ever` is the permanent audit trail.
            meta_path.write_text(yaml.safe_dump({
                "schema": 1, "mode": mode, "seed": seed,
                "corpus_path": str(corpus_path), "schedule_path": str(schedule_path),
                "briefing_path": str(briefing_path), "episode_end_day": episode_end_day,
                "debug_ever": mode == "debug", "created": date.today().isoformat(),
            }), encoding="utf-8")
        else:
            # re-entry on an existing session dir: same loud provenance check as resume()
            cls._read_briefing_snapshot(session_dir)
            if mode == "debug":
                cls._stamp_debug(session_dir)
        return cls(session_dir, env, mode)

    @staticmethod
    def _read_briefing_snapshot(session_dir: Path) -> str:
        snap = Path(session_dir) / "briefing.md"
        if not snap.exists():
            raise ValueError(
                f"missing briefing snapshot at {snap}: this session predates briefing "
                f"snapshotting (or the copy was deleted). Serving the live briefing file would "
                f"corrupt prompt provenance — restore the briefing text that was active when the "
                f"session was recorded (e.g. from git history of the file named in meta.yml's "
                f"briefing_path) into that snapshot path, then retry."
            )
        return snap.read_text(encoding="utf-8").strip()

    # --- record ---
    def _count_records(self) -> int:
        if not self._record_path.exists():
            return 0
        return sum(1 for line in self._record_path.read_text(encoding="utf-8").splitlines() if line)

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
    def _stamp_debug(session_dir: str | Path) -> None:
        meta_path = Path(session_dir) / "meta.yml"
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        if not meta.get("debug_ever"):
            meta["debug_ever"] = True
            meta_path.write_text(yaml.safe_dump(meta), encoding="utf-8")

    @classmethod
    def resume(cls, session_dir: str | Path, *, mode: str | None = None) -> "PlaySession":
        """Rebuild a session from `meta.yml` + `state.snapshot.json`, replaying the
        `session.jsonl` tail after the snapshot (spec §10). A missing snapshot replays
        the whole log from day 0 (the documented fallback); a corrupt snapshot fails loud.
        """
        session_dir = Path(session_dir)
        meta = yaml.safe_load((session_dir / "meta.yml").read_text(encoding="utf-8"))
        # fail loud on a missing briefing snapshot BEFORE any side effect (notably the
        # permanent debug_ever stamp below — a failed resume must not taint the session)
        cls._read_briefing_snapshot(session_dir)
        # meta["mode"] is the write-once creation/launch-default mode; it is deliberately NOT
        # updated here even when `mode` opts into debug for this launch — debug access requires
        # explicit opt-in per launch (safer for blindness), while debug_ever is the permanent record.
        effective_mode = mode or meta["mode"]
        if effective_mode == "debug":
            cls._stamp_debug(session_dir)
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
        session = cls(session_dir, env, effective_mode)
        cls._replay_tail(env, session_dir, snapshot_seq)
        return session

    @staticmethod
    def _replay_tail(env: FarmEnv, session_dir: Path, snapshot_seq: int) -> None:
        """Re-execute session.jsonl records after `snapshot_seq` WITHOUT re-recording them."""
        record_path = session_dir / "session.jsonl"
        if not record_path.exists():
            return
        for line in record_path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
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
        return self._read_briefing_snapshot(self.session_dir)

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
