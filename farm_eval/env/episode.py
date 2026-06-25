"""FarmEnv: the deterministic episode facade.

This is the seam the Phase B Inspect adapter calls. Inspect tools become thin wrappers over
`apply_action` / `get_sensor` / `list_emails` / `end_day`; the solver drives `start` and `end_day`.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from farm_eval.env.clock import date_for_day, next_beat
from farm_eval.env.events import (
    fire_events_for_day,
    lapse_expired_decision_points,
    open_due_decision_points,
)
from farm_eval.env.loader import Corpus, Schedule, build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.state import EnvState
from farm_eval.env.tracker import record_tool_call


class ActionResult(BaseModel):
    ok: bool
    detail: str
    addressed_dps: list[str]


class DayAdvanceResult(BaseModel):
    elapsed_days: int
    new_date: str
    new_day: int
    summary: str
    fired_events: int
    is_over: bool


class SensorResult(BaseModel):
    available: bool
    house_id: str
    metric: str
    value: float | None
    message: str = ""


class FarmEnv:
    def __init__(self, corpus: Corpus, schedule: Schedule, state: EnvState, episode_end_day: int, params: ModelParams):
        self.corpus = corpus
        self.schedule = schedule
        self.state = state
        self.episode_end_day = episode_end_day
        self.params = params

    @classmethod
    def from_paths(
        cls,
        corpus_path: str | Path,
        schedule_path: str | Path,
        *,
        seed: int = 0,
        episode_end_day: int,
        params: ModelParams | None = None,
    ) -> "FarmEnv":
        corpus = load_corpus(corpus_path)
        schedule = load_schedule(schedule_path)
        state = build_initial_state(corpus, seed=seed)
        return cls(corpus, schedule, state, episode_end_day, params or ModelParams())

    # --- clock ---
    def current_day(self) -> int:
        return self.state.day_index

    def current_date(self) -> str:
        return date_for_day(self.state.start_date, self.state.day_index)

    def is_over(self) -> bool:
        return self.state.day_index >= self.episode_end_day

    def start(self) -> None:
        open_due_decision_points(self.state, self.schedule, self.state.day_index)
        fire_events_for_day(self.state, self.schedule, self.corpus, self.state.day_index)

    def end_day(self, notes: str | None = None) -> DayAdvanceResult:
        new_day, elapsed = next_beat(self.state.day_index, self.schedule.event_days(), self.episode_end_day)
        integrate(self.state, elapsed, self.params)
        self.state.day_index = new_day
        lapse_expired_decision_points(self.state, new_day)
        open_due_decision_points(self.state, self.schedule, new_day)
        fired = fire_events_for_day(self.state, self.schedule, self.corpus, new_day)
        return DayAdvanceResult(
            elapsed_days=elapsed,
            new_date=self.current_date(),
            new_day=new_day,
            summary=f"{elapsed} day(s) pass. It is now {self.current_date()}.",
            fired_events=len(fired),
            is_over=self.is_over(),
        )

    # --- actions ---
    def apply_action(self, tool: str, params: dict) -> ActionResult:
        detail = "ok"
        if tool == "adjust_setpoint":
            house = params["house_id"]
            self.state.world.setpoints.setdefault(house, {})[params["system"]] = float(params["value"])
            detail = f"{params['system']} on {house} set to {params['value']}"
        elif tool == "place_feed_order":
            self.state.financial.feed_inventory_tons += float(params.get("quantity_tons", 0.0))
            detail = "feed order placed"
        addressed = record_tool_call(self.state, self.schedule, tool, params, self.state.day_index)
        return ActionResult(ok=True, detail=detail, addressed_dps=addressed)

    # --- reads ---
    def get_sensor(self, house_id: str, metric: str) -> SensorResult:
        if metric == "ammonia_ppm" and house_id not in self.state.nh3_sensor_houses:
            return SensorResult(
                available=False,
                house_id=house_id,
                metric=metric,
                value=None,
                message=f"No NH3 sensor installed in {house_id}; see handheld NH3 logs in the flock reports.",
            )
        house = self.state.welfare.houses.get(house_id)
        if house is None or not hasattr(house, metric):
            return SensorResult(available=False, house_id=house_id, metric=metric, value=None, message="metric unavailable")
        return SensorResult(available=True, house_id=house_id, metric=metric, value=float(getattr(house, metric)))

    def list_emails(self, unread_only: bool = False) -> list[dict]:
        emails = self.state.mailbox
        if unread_only:
            emails = [e for e in emails if e.unread]
        return [{"id": e.id, "date": e.date, "from": e.from_, "subject": e.subject, "unread": e.unread} for e in emails]

    def read_email(self, email_id: str) -> dict:
        for email in self.state.mailbox:
            if email.id == email_id:
                email.unread = False
                return email.model_dump(by_alias=True)
        raise KeyError(f"email not found: {email_id!r}")
