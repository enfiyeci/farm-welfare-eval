"""PlaySession: the one seam over FarmEnv for human play (spec §3).

Inspect-free. Both frontends (the web server and the scriptable reference-policy driver)
consume this and nothing else. Every op call is validated against the parity registry and
appended to the session record; blindness is enforced HERE (accessors raise), not in the UI.
"""

from __future__ import annotations

import json
from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.play.ops import OPS, run_op


class EpisodeOver(Exception):
    """An action op was attempted after the episode horizon (server maps this to 409)."""


class PlaySession:
    def __init__(self, session_dir: Path, env: FarmEnv, briefing_path: Path, mode: str):
        if mode not in ("blind", "debug"):
            raise ValueError(f"mode must be 'blind' or 'debug', got {mode!r}")
        self.session_dir = Path(session_dir)
        self.env = env
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
        return cls(session_dir, env, Path(briefing_path), mode)

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
        if spec.kind == "action" and self.env.is_over():
            raise EpisodeOver("episode is over; action ops are closed (reads remain available)")
        result = run_op(self.env, op, full)
        self._append({"kind": "op", "day_index": self.env.current_day(), "op": op,
                      "params": full, "result": result})
        return result

    def end_day(self, notes: str = "") -> dict:
        day_before = self.env.current_day()
        result = self.env.end_day(notes=notes or None)
        self._append({"kind": "day", "day_index": day_before, "summary": result.summary,
                      "new_day": result.new_day, "is_over": result.is_over})
        self._autosave()
        return {"summary": result.summary, "new_day": result.new_day, "is_over": result.is_over}

    def note(self, text: str) -> None:
        self._append({"kind": "note", "day_index": self.env.current_day(), "text": text})

    def _autosave(self) -> None:  # implemented in Task 3 (persistence); no-op until then
        pass

    # --- loop context (not world information; spec §4.2 exception) ---
    def meta(self) -> dict:
        return {
            "day_index": self.env.current_day(), "date": self.env.current_date(),
            "is_over": self.env.is_over(), "mode": self.mode,
            "episode_end_day": self.env.episode_end_day,
        }

    def briefing(self) -> str:
        return self.briefing_path.read_text(encoding="utf-8").strip()

    # --- debug-only accessors (spec §7) ---
    def _require_debug(self) -> None:
        if self.mode != "debug":
            raise PermissionError("debug accessor called on a blind session")

    def ledger(self) -> list[dict]:
        self._require_debug()
        return [e.model_dump(mode="json") for e in self.env.state.ledger]

    def env_snapshot(self) -> dict:
        self._require_debug()
        return self.env.state.model_dump(mode="json")

    def schedule_preview(self) -> list[dict]:
        self._require_debug()
        today = self.env.current_day()
        upcoming = []
        for dp in self.env.schedule.decision_points:
            if dp.deadline_day >= today:
                upcoming.append({"id": dp.id, "opens_day": dp.opens_day, "deadline_day": dp.deadline_day})
        for ev in self.env.schedule.events:
            if ev.on_day >= today:
                upcoming.append({"on_day": ev.on_day, "type": str(ev.type)})
        return sorted(upcoming, key=lambda r: (r.get("opens_day", r.get("on_day", 0)), r.get("id", "")))
