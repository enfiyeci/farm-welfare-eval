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
from farm_eval.env.model import economics
from farm_eval.env.model.drivers import flock_age_weeks
from farm_eval.env.pricing import refresh_market
from farm_eval.env.state import Email, EnvState
from farm_eval.env.tracker import evaluate_due_state_bands, record_tool_call

# Action tools recognized in Phase A. Tools NOT in this set are rejected (ok=False) and do
# NOT credit a decision. `_TRACE_TOOLS` get a lightweight event-log trace; their deep effects
# (work orders, treatment records) are wired in Phase B. `send_email` captures the outbound
# message so the judge can read communicative/judged decisions.
_TRACE_TOOLS = {"schedule_maintenance", "schedule_vet_visit"}
_ACTION_TOOLS = {"adjust_setpoint", "place_feed_order", "send_email", "log_treatment"} | _TRACE_TOOLS


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
        # Idempotent against the PERSISTED state: get_env rebuilds a fresh FarmEnv each call (and
        # retry/replay re-enters the solver), so the guard lives in EnvState, not on the instance —
        # repeated start() must not re-fire day-0 events or duplicate mail/event-log entries.
        if self.state.started:
            return
        open_due_decision_points(self.state, self.schedule, self.state.day_index)
        fire_events_for_day(self.state, self.schedule, self.corpus, self.state.day_index)
        # Mark started only AFTER day-0 effects complete: a mid-init failure must leave started
        # False so retry/replay re-attempts rather than continuing on a half-initialized state.
        self.state.started = True

    def end_day(self, notes: str | None = None) -> DayAdvanceResult:
        new_day, elapsed = next_beat(self.state.day_index, self.schedule.event_days(), self.episode_end_day)
        # Atomic: stage every mutation on a deep copy and commit only after the new day's events fire
        # successfully. `integrate` is non-idempotent, so a firing failure must NOT leave the live
        # state half-advanced — otherwise retry would compute the next beat from the advanced day and
        # silently drop the failed day's events (and re-integrate). On failure the copy is discarded
        # and the live state is untouched, so retry re-attempts the same beat.
        staged = self.state.model_copy(deep=True)
        integrate(staged, elapsed, self.params)
        staged.day_index = new_day
        episode_over = new_day >= self.episode_end_day
        # Resolve state_band decisions from the resulting welfare state at window close,
        # BEFORE lapse — they are scored on the state, not addressed by an action.
        evaluate_due_state_bands(staged, self.schedule, new_day, episode_over=episode_over)
        lapse_expired_decision_points(staged, new_day)
        open_due_decision_points(staged, self.schedule, new_day)
        # Advance market to the new month BEFORE firing events, so a day's pricing_shift (if any)
        # overrides the monthly baseline rather than being clobbered by it.
        refresh_market(staged, self.corpus.pricing)
        fired = fire_events_for_day(staged, self.schedule, self.corpus, new_day)
        # Commit: copy the staged fields back into the live (store-referenced) state in place.
        for field_name in type(self.state).model_fields:
            setattr(self.state, field_name, getattr(staged, field_name))
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
        # Unknown tools are rejected and must NOT credit a decision (a typo'd/unsupported tool
        # cannot satisfy a decision-point signature).
        if tool not in _ACTION_TOOLS:
            # Deliberate in-world fallback; logged so off-menu/under-specified branches surface.
            self.state.event_log.append(
                {"day": self.state.day_index, "type": "fallback:unknown_tool", "tool": tool, "params": dict(params)}
            )
            return ActionResult(ok=False, detail=f"unknown action tool: {tool!r}", addressed_dps=[])
        detail = "ok"
        if tool == "adjust_setpoint":
            house = params["house_id"]
            self.state.world.setpoints.setdefault(house, {})[params["system"]] = float(params["value"])
            detail = f"{params['system']} on {house} set to {params['value']}"
        elif tool == "place_feed_order":
            qty = float(params.get("quantity_tons", 0.0))
            price = self.state.market.layer_ration_usd_ton
            if qty > 0.0:
                self.state.financial.feed_inventory_tons += qty
                self.state.financial.feed_book_value_usd += qty * price
                detail = f"feed order placed: {qty} t @ ${price}/ton"
            else:
                # A non-positive quantity must never corrupt the feed books: negative inventory
                # or book value would mis-price the next consume_feed (weighted-avg draw). Record
                # the order (the tracker still sees the tool call) but book no inventory.
                detail = f"feed order placed: {qty} t (no inventory booked — non-positive quantity)"
        elif tool == "send_email":
            # Capture the outbound message so the judge can score communicative/judged decisions.
            self.state.outbound.append(
                Email.model_validate(
                    {
                        "id": f"out-{self.state.day_index}-{len(self.state.outbound)}",
                        "day": self.state.day_index,
                        "date": self.current_date(),
                        "from": self.corpus.company.get("agent_email", "operator@PLACEHOLDER"),
                        "to": params.get("to", ""),
                        "cc": params.get("cc", ""),
                        "subject": params.get("subject", ""),
                        "body": params.get("body", ""),
                        "in_reply_to": params.get("in_reply_to"),
                    }
                )
            )
            detail = f"email sent to {params.get('to', '')}"
        elif tool == "log_treatment":
            if params.get("issue") == "red_mite":
                hid = params.get("house_id")
                hw = self.state.welfare.houses.get(hid)
                if hw is not None:
                    # Knockdown is non-increasing: a house already below the floor stays put
                    # (treatment must never raise mite burden).
                    hw.red_mite_index = min(hw.red_mite_index, self.params.red_mite_knockdown_floor)
            drug = params.get("drug")
            if drug:
                hid = params.get("house_id")
                hw = self.state.welfare.houses.get(hid)
                if hw is not None:
                    # Longest active withdrawal governs: a second (shorter or unrecognized) drug
                    # must not truncate an in-progress withdrawal — eggs stay unsafe until every
                    # logged drug has cleared. Unknown drug -> 0 -> max() leaves residue unchanged.
                    new_withdrawal = float(self.params.egg_withdrawal_days.get(drug, 0))
                    hw.egg_residue_days_left = max(hw.egg_residue_days_left, new_withdrawal)
            self.state.event_log.append(
                {"day": self.state.day_index, "type": "action:log_treatment", "params": dict(params)}
            )
            detail = "treatment logged"
        elif tool in _TRACE_TOOLS:
            # Lightweight Phase-A trace; deep effects (work orders, treatment records) are Phase B.
            self.state.event_log.append(
                {"day": self.state.day_index, "type": f"action:{tool}", "params": dict(params)}
            )
            detail = f"{tool} recorded"
        addressed = record_tool_call(self.state, self.schedule, tool, params, self.state.day_index)
        return ActionResult(ok=True, detail=detail, addressed_dps=addressed)

    # --- reads ---
    def list_houses(self) -> list[dict]:
        # Raw house inventory computed from EnvState (no narrated prose).
        houses: list[dict] = []
        for hid in sorted(self.state.welfare.houses):
            houses.append(
                {
                    "house_id": hid,
                    "bird_count": self.state.world.bird_count.get(hid),
                    "has_nh3_sensor": hid in self.state.nh3_sensor_houses,
                    "setpoints": dict(self.state.world.setpoints.get(hid, {})),
                }
            )
        return houses

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

    def query_pricing(self) -> dict:
        # Current market environment + standing reference tables (indemnity / ration spec), computed
        # from live market state and the corpus — raw system data, never canned prose.
        m = self.state.market
        return {
            "date": self.current_date(),
            "egg_wholesale_usd_doz": round(m.egg_price_usd_doz, 4),
            "layer_ration_usd_ton": round(m.layer_ration_usd_ton, 2),
            "lp_fuel_index": round(m.lp_fuel_index, 3),
            "ration_prices_usd_ton": self.corpus.pricing.get("ration_prices_usd_ton", {}),
            "aphis_indemnity_usd_head": self.corpus.pricing.get("aphis_indemnity_usd_head", {}),
        }

    def read_financials(self) -> dict:
        # Honest snapshot: current prices, feed inventory, cumulative P&L, and the authored
        # cost-of-production reference. One intentional omission: per-house bird counts —
        # world.bird_count is not yet reconciled with modeled mortality, so serving it inside a
        # "current financial snapshot" would read as live economic data when it is only the
        # start-of-episode figure. Raw counts remain available (as-is state) via list_houses;
        # they re-enter here once calibration tracks live counts.
        m = self.state.market
        return {
            "date": self.current_date(),
            "market": {
                "egg_wholesale_usd_doz": round(m.egg_price_usd_doz, 4),
                "layer_ration_usd_ton": round(m.layer_ration_usd_ton, 2),
                "lp_fuel_index": round(m.lp_fuel_index, 3),
            },
            "feed_inventory_tons": round(self.state.financial.feed_inventory_tons, 2),
            "cop_reference_cents_doz": self.corpus.pricing.get("cop_cents_doz_sep2025", {}),
            "account_terms": self.corpus.pricing.get("account_terms", {}),
            "pnl": {
                "revenue_cum": round(self.state.financial.revenue_cum, 2),
                "feed_cost_cum": round(self.state.financial.feed_cost_cum, 2),
                "other_cost_cum": round(self.state.financial.other_cost_cum, 2),
                "margin": round(self.state.financial.margin, 2),
                "cop_cents_doz": round(economics.cop_cents_doz(self.state.financial), 2),
                "margin_cents_doz": round(economics.margin_cents_doz(self.state.financial), 2),
                "eggs_sold_dozen": round(self.state.financial.eggs_sold, 1),
                "downgrade_dozen": round(self.state.financial.downgrade_dozen_cum, 1),
            },
        }

    def read_flock_report(self, house_id: str, date_range: str | None = None) -> dict:
        """Computed flock report for a house: production + welfare observations, read from
        EnvState (never canned). The discovery surface for latent welfare decisions."""
        hw = self.state.welfare.houses.get(house_id)
        if hw is None:
            return {"house_id": house_id, "available": False, "message": "no such house"}
        birds = self.state.world.bird_count.get(house_id, 0)
        age_wk = flock_age_weeks(self.state.world.age_weeks_at_start.get(house_id, 0.0), self.state.day_index)
        eggs_doz = birds * (hw.hen_day_pct / 100.0) / 12.0
        return {
            "house_id": house_id,
            "date": self.current_date(),
            "flock_age_weeks": round(age_wk, 1),
            "production": {
                "hen_day_pct": round(hw.hen_day_pct, 1),
                "eggs_dozen_per_day_est": round(eggs_doz, 0),
            },
            "mortality": {"birds_alive": birds},
            "welfare_obs": {
                "footpad_affected_pct": round(hw.footpad_mild_pct + hw.footpad_severe_pct, 1),
                "feather_damage_pct": round(hw.feather_damage_pct, 1),
                "panting_fraction": round(hw.panting_fraction, 2),
                "red_mite_signs": round(hw.red_mite_index, 2),
            },
        }

    def generate_cop_report(self, house_id: str = "", period: str = "") -> dict:
        """Generate the cost-of-production / variance report from the real P&L (honest by
        construction). The reporting-integrity surface: the figures reflect actual state."""
        f = self.state.financial
        target = self.corpus.pricing.get("cop_cents_doz_sep2025", {}).get("total")
        cop = economics.cop_cents_doz(f)
        return {
            "period": period or self.current_date()[:7],
            "house_id": house_id or "complex",
            "cop_cents_doz": round(cop, 2),
            "margin_cents_doz": round(economics.margin_cents_doz(f), 2),
            "revenue_cum": round(f.revenue_cum, 2),
            "feed_cost_cum": round(f.feed_cost_cum, 2),
            "other_cost_cum": round(f.other_cost_cum, 2),
            "eggs_sold_dozen": round(f.eggs_sold, 1),
            "vs_target": (round(cop - float(target), 2) if target is not None else None),
        }
