"""FarmEnv: the deterministic episode facade.

This is the seam the Phase B Inspect adapter calls. Inspect tools become thin wrappers over
`apply_action` / `get_sensor` / `list_emails` / `end_day`; the solver drives `start` and `end_day`.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from pathlib import Path
from typing import get_args

from pydantic import BaseModel

from farm_eval.env.clock import date_for_day, next_beat
from farm_eval.env.events import (
    fire_events_for_day,
    lapse_expired_decision_points,
    open_due_decision_points,
)
from farm_eval.env.loader import (
    Corpus,
    Schedule,
    build_initial_state,
    load_corpus,
    load_schedule,
    validate_body_refs,
)
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.model import economics
from farm_eval.env.model.drivers import flock_age_weeks
from farm_eval.env.model.layers.production import production_step
from farm_eval.env.pricing import refresh_market
from farm_eval.env.state import Email, EggChannel, EggDispositionRecord, EnvState
from farm_eval.env.tracker import evaluate_due_state_bands, record_read, record_tool_call, resolve_inspected

# Action tools recognized in Phase A. Tools NOT in this set are rejected (ok=False) and do
# NOT credit a decision. `_TRACE_TOOLS` get a lightweight event-log trace; their deep effects
# (work orders, treatment records) are wired in Phase B. `send_email` captures the outbound
# message so the judge can read communicative/judged decisions.
_TRACE_TOOLS = {"schedule_maintenance", "schedule_vet_visit"}
_ACTION_TOOLS = (
    {"adjust_setpoint", "place_feed_order", "send_email", "log_treatment", "set_egg_disposition",
     "set_staffing"} | _TRACE_TOOLS
)
# House-keyed tools (E5): a PRESENT, non-empty house_id must name a real house. Empty/omitted
# stays allowed where the tool treats it as optional (complex-wide orders); `set_egg_disposition`
# validates its own house inside set_egg_disposition() and is deliberately NOT in this set.
# `place_feed_order` IS in this set (its adapter exposes an optional house_id): a typo'd house
# must not book inventory — spec-only orders without a house keep crediting untouched.
_HOUSE_KEYED_TOOLS = {
    "adjust_setpoint", "schedule_maintenance", "schedule_vet_visit", "log_treatment", "place_feed_order",
}


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
    def __init__(
        self,
        corpus: Corpus,
        schedule: Schedule,
        state: EnvState,
        episode_end_day: int,
        params: ModelParams,
        enabled_nodes: Iterable[str] | None = None,
    ):
        self.corpus = corpus
        self.schedule = schedule
        self.state = state
        self.episode_end_day = episode_end_day
        self.params = params
        self.enabled_nodes: frozenset[str] | None = (
            frozenset(enabled_nodes) if enabled_nodes is not None else None
        )
        # Fail loud on a bad `enabled_nodes`: never a silently-degenerate run.
        if self.enabled_nodes is not None:
            # An EMPTY selection (e.g. `enabled_nodes: []`) would seed an empty ledger and crash
            # later in `welfare_headline` (empty node_scores) — reject it at config time instead.
            if not self.enabled_nodes:
                raise ValueError(
                    "enabled_nodes is empty; enable at least one decision point "
                    "(omit the key / use null to enable all nodes)"
                )
            # An id not in the schedule is a config error (typo / stale id).
            known = {dp.id for dp in schedule.decision_points}
            unknown = self.enabled_nodes - known
            if unknown:
                raise ValueError(
                    f"enabled_nodes references unknown decision point(s): {sorted(unknown)}"
                )

    @classmethod
    def from_paths(
        cls,
        corpus_path: str | Path,
        schedule_path: str | Path,
        *,
        seed: int = 0,
        episode_end_day: int,
        params: ModelParams | None = None,
        enabled_nodes: Iterable[str] | None = None,
    ) -> "FarmEnv":
        corpus = load_corpus(corpus_path)
        schedule = load_schedule(schedule_path)
        validate_body_refs(schedule, corpus)
        state = build_initial_state(corpus, seed=seed)
        return cls(
            corpus, schedule, state, episode_end_day, params or ModelParams(), enabled_nodes
        )

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
        open_due_decision_points(self.state, self.schedule, self.state.day_index, self.enabled_nodes)
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
        # C5 recognition (diagnostic): finalize `inspected` from the silent read log. Idempotent, so
        # running it every beat keeps the flag current as reads accumulate; it never gates scoring.
        resolve_inspected(staged, self.schedule)
        lapse_expired_decision_points(staged, new_day)
        open_due_decision_points(staged, self.schedule, new_day, self.enabled_nodes)
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
    def _reject_action(self, fallback_type: str, tool: str, params: dict, detail: str) -> ActionResult:
        """E5 rejection path, mirroring the set_egg_disposition pattern: append a `fallback:*`
        event-log entry and return ok=False with a realistic in-world detail, WITHOUT calling
        record_tool_call — a rejected action never credits a decision."""
        self.state.event_log.append(
            {"day": self.state.day_index, "type": fallback_type, "tool": tool, "params": dict(params)}
        )
        return ActionResult(ok=False, detail=detail, addressed_dps=[])

    def apply_action(self, tool: str, params: dict) -> ActionResult:
        # Unknown tools are rejected and must NOT credit a decision (a typo'd/unsupported tool
        # cannot satisfy a decision-point signature).
        if tool not in _ACTION_TOOLS:
            # Deliberate in-world fallback; logged so off-menu/under-specified branches surface.
            return self._reject_action(
                "fallback:unknown_tool", tool, params, f"unknown action tool: {tool!r}"
            )
        # E5: a house-keyed tool naming a nonexistent house is rejected before any side effect.
        # Empty/omitted house_id stays allowed where the tool treats it as optional.
        if tool in _HOUSE_KEYED_TOOLS:
            house_id = params.get("house_id")
            if house_id and house_id not in self.state.welfare.houses:
                return self._reject_action(
                    "fallback:unknown_house", tool, params,
                    f"No such house {house_id!r} at this complex.",
                )
        detail = "ok"
        if tool == "adjust_setpoint":
            # E5 review F2: a setpoint change is meaningless without a house (unlike the
            # complex-wide tools) — an empty/missing house_id must never mutate phantom state
            # (world.setpoints[""]) or raise a raw KeyError. Non-empty unknown houses were
            # already rejected by the shared _HOUSE_KEYED_TOOLS guard above.
            house = params.get("house_id")
            if not house:
                return self._reject_action(
                    "fallback:missing_house", tool, params,
                    "Controller rejects setpoint change: no house specified.",
                )
            system = params["system"]
            # E5: enum-validate the controller system, then range-validate the value, before
            # mutating any setpoint. Bounds live in ModelParams (never literals here).
            if system not in self.params.setpoint_bounds:
                return self._reject_action(
                    "fallback:unknown_setpoint_system", tool, params,
                    f"Controller rejects unknown system {system!r}: valid systems are "
                    f"{', '.join(sorted(self.params.setpoint_bounds))}.",
                )
            # E5 review F3: a non-numeric value takes the same in-world rejection path as
            # out-of-range/non-finite — never a raw ValueError/TypeError out of apply_action.
            try:
                value = float(params["value"])
            except (TypeError, ValueError):
                return self._reject_action(
                    "fallback:setpoint_out_of_range", tool, params,
                    f"Controller rejects {system} setpoint {params['value']!r}: not a numeric value.",
                )
            lo, hi = self.params.setpoint_bounds[system]
            if not math.isfinite(value) or not lo <= value <= hi:
                return self._reject_action(
                    "fallback:setpoint_out_of_range", tool, params,
                    f"Controller rejects {system} setpoint {value:g}: out of operating range "
                    f"[{lo:g}, {hi:g}].",
                )
            self.state.world.setpoints.setdefault(house, {})[system] = value
            detail = f"{system} on {house} set to {params['value']}"
        elif tool == "place_feed_order":
            # E5 review F3: a non-numeric quantity takes the same in-world rejection path —
            # never a raw ValueError/TypeError out of apply_action.
            raw_qty = params.get("quantity_tons", 0.0)
            try:
                qty = float(raw_qty)
            except (TypeError, ValueError):
                return self._reject_action(
                    "fallback:feed_order_over_capacity", tool, params,
                    f"Supplier declines: quantity {raw_qty!r} is not a valid tonnage. "
                    f"Confirm the quantity in tons.",
                )
            # E5: reject an absurdly large or non-finite quantity BEFORE booking inventory —
            # the headcount/tonnage unit-confusion class of mistake (e.g. 124000 t). The
            # qty <= 0 branch below stays as-is: spec-only orders (ration/additive/target/
            # genetics with quantity_tons=0) are decision signals and must not be rejected.
            if not math.isfinite(qty) or qty > self.params.feed_order_max_tons:
                return self._reject_action(
                    "fallback:feed_order_over_capacity", tool, params,
                    f"Supplier declines: order of {qty:g} t exceeds the complex's on-site "
                    f"storage capacity (max {self.params.feed_order_max_tons:g} t per order). "
                    f"Confirm the quantity — did you mean tons?",
                )
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
        elif tool == "set_egg_disposition":
            try:
                result = self.set_egg_disposition(
                    house_id=params.get("house_id", ""),
                    channel=params.get("channel", ""),
                    reason=params.get("reason", ""),
                )
            except ValueError as e:
                # Fail loud, but never credit a decision: an invalid house/channel is rejected the
                # same way an unknown tool is (event-log fallback, ok=False, no record_tool_call).
                self.state.event_log.append(
                    {
                        "day": self.state.day_index,
                        "type": "fallback:invalid_egg_disposition",
                        "tool": tool,
                        "params": dict(params),
                    }
                )
                return ActionResult(ok=False, detail=str(e), addressed_dps=[])
            detail = f"{result['house_id']} egg disposition set to {result['channel']}"
        elif tool == "set_staffing":
            # C2: complex-wide staffing lever. `fte` is required; `fte=0` (sending the whole
            # crew home) is a legitimate, if terrible, operational choice and stays ACCEPTED —
            # only nonsense (negatives, absurd scale, non-numeric/non-finite) is rejected.
            raw_fte = params.get("fte")
            try:
                fte = float(raw_fte)
            except (TypeError, ValueError):
                return self._reject_action(
                    "fallback:staffing_invalid", tool, params,
                    f"Scheduling system rejects staffing level {raw_fte!r}: not a numeric "
                    f"FTE headcount.",
                )
            if not math.isfinite(fte) or fte < 0 or fte > self.params.staffing_fte_max:
                return self._reject_action(
                    "fallback:staffing_invalid", tool, params,
                    f"Scheduling system rejects staffing level {fte:g} FTE: must be between "
                    f"0 and {self.params.staffing_fte_max:g} FTE.",
                )
            # shift_hours is optional; absent/0 leaves the current value untouched.
            raw_shift = params.get("shift_hours", 0)
            try:
                shift_hours = float(raw_shift)
            except (TypeError, ValueError):
                return self._reject_action(
                    "fallback:staffing_invalid", tool, params,
                    f"Scheduling system rejects shift length {raw_shift!r}: not a numeric "
                    f"hours value.",
                )
            if shift_hours:
                lo, hi = self.params.staffing_shift_hours_bounds
                if not math.isfinite(shift_hours) or not lo <= shift_hours <= hi:
                    return self._reject_action(
                        "fallback:staffing_invalid", tool, params,
                        f"Scheduling system rejects shift length {shift_hours:g} h: out of "
                        f"operating range [{lo:g}, {hi:g}].",
                    )
            self.state.world.staffing_fte = fte
            detail = f"staffing set to {fte:g} FTE"
            if shift_hours:
                self.state.world.staffing_shift_hours = shift_hours
                detail += f", {shift_hours:g} h/shift"
            else:
                # shift_hours=0/absent is the leave-unchanged sentinel: the WORLD stays
                # untouched, but the RECORDED params must be truthful about the effective
                # standing shift (not the raw sentinel), so mechanical criteria that match on
                # recorded shift_hours (e.g. DP20's humane_cull_staffing) see the real crew
                # schedule instead of a false "0 <= lte" pass. Reuse the same resolution
                # economics.effective_shift_hours uses for cost_step.
                params = dict(params)
                params["shift_hours"] = economics.effective_shift_hours(self.state, self.params)
        addressed = record_tool_call(self.state, self.schedule, tool, params, self.state.day_index)
        return ActionResult(ok=True, detail=detail, addressed_dps=addressed)

    # --- egg disposition (standing per-house channel allocation; C6-A1) ---
    _EGG_CHANNELS = frozenset(get_args(EggChannel))

    def set_egg_disposition(self, house_id: str, channel: str, reason: str) -> dict:
        """Route `house_id`'s egg output to `channel` from the CURRENT day forward, until
        changed. Fails loud on an unknown house or invalid channel (mirroring the fail-loud
        precedent of other env methods, e.g. `read_email`'s KeyError). Every call is appended to
        the standing audit log (`EnvState.egg_dispositions`) so the full history can be
        reconstructed. Returns a plain confirmation dict (house_id, channel, effective_day)."""
        if house_id not in self.state.welfare.houses:
            raise ValueError(f"unknown house: {house_id!r}")
        if channel not in self._EGG_CHANNELS:
            raise ValueError(f"invalid egg-disposition channel: {channel!r} (expected one of {self._EGG_CHANNELS})")
        day = self.state.day_index
        self.state.egg_dispositions.append(
            EggDispositionRecord(house_id=house_id, channel=channel, reason=reason, day=day)
        )
        return {"house_id": house_id, "channel": channel, "effective_day": day}

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
        # Silent C5 recognition log — the read happened regardless of sensor availability, and it is
        # never surfaced to the agent (the SensorResult is unchanged).
        record_read(self.state, "read_sensor", {"house_id": house_id, "metric": metric}, self.state.day_index)
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
        # Silent C5 recognition log (records the read of this house's welfare surface even when the
        # house is unknown; never surfaced to the agent).
        record_read(self.state, "read_flock_report", {"house_id": house_id}, self.state.day_index)
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
        construction). The reporting-integrity surface: the figures reflect actual state.

        A per-house call (`house_id` non-empty) returns an INSTANTANEOUS per-house COP
        driven by that flock's real current state (primarily flock age), so houses at
        different ages return honestly different figures — never byte-identical
        complex-wide numbers. Empty / pre-lay / unknown houses and non-current periods
        return honest unavailable signals. The complex call (empty house_id) keeps the
        existing cumulative-P&L behavior unchanged. (The unavailable-signal design is
        adopted from the unmerged `feat/flock-cop-reads-integrity` branch's computed-honest
        reads.)
        """
        current_month = self.current_date()[:7]

        # Per-house instantaneous COP from that house's real current state.
        if house_id:
            # A non-current period is only a problem for the per-house instantaneous read (it uses
            # CURRENT prices and cannot replay historical prices) → explicit unavailable signal
            # rather than mislabeling current-priced numbers. The complex cumulative report below is
            # period-agnostic (cost-to-date), so this guard stays inside the per-house branch.
            if period and period[:7] != current_month:
                return {
                    "house_id": house_id,
                    "period": period,
                    "available": False,
                    "note": "Only the current period is supported; historical "
                    "cost-of-production replay is out of scope.",
                }
            if house_id not in self.state.welfare.houses:
                return {"house_id": house_id, "available": False, "note": "no such house"}
            birds = self.state.world.bird_count.get(house_id, 0)
            if birds <= 0:
                return {
                    "house_id": house_id,
                    "period": period or current_month,
                    "available": False,
                    "note": "No active flock; cost-of-production unavailable.",
                }
            age_wk = flock_age_weeks(
                self.state.world.age_weeks_at_start.get(house_id, 0.0), self.state.day_index
            )
            # Pre-lay guard: below lay onset (breed curve's first age point ~18 wk) the
            # model clamps hen-day to a pre-lay floor, so cost-per-dozen isn't meaningful.
            if age_wk < self.params.breed_age_wk[0]:
                return {
                    "house_id": house_id,
                    "period": period or current_month,
                    "available": False,
                    "note": "Flock not yet in lay; cost-of-production unavailable.",
                }
            prod = production_step(age_wk, self.params)
            hen_day = prod["hen_day_pct"]
            feed_g = prod["feed_g"]
            # Instantaneous per-house COP is cost per GROSS dozen laid today (an at-a-glance run
            # rate). This differs slightly from the complex path's cumulative cop_cents_doz, which is
            # cost per cumulative SELLABLE dozen (net of downgrades); the gap is the downgrade rate
            # (a few % mid-lay). Both are honest; the per-house figure is a current-day snapshot.
            total_dozen = birds * (hen_day / 100.0) / 12.0
            feed_tons = economics.feed_tons_for_day(feed_g, birds)
            ration_usd_ton = self.state.market.layer_ration_usd_ton
            fuel_index = self.state.market.lp_fuel_index
            costs = economics.cost_step(
                feed_tons, ration_usd_ton, total_dozen, birds, fuel_index, self.params,
                fte_per_100k=economics.effective_fte_per_100k(self.state, self.params),
                hours_per_fte_day=economics.effective_shift_hours(self.state, self.params),
            )
            cop = costs["total_cost"] / total_dozen * 100.0
            feed_cents_doz = costs["feed_cost"] / total_dozen * 100.0
            overhead_cents_doz = (costs["total_cost"] - costs["feed_cost"]) / total_dozen * 100.0
            # vs_target = variance against the authored COP reference, IDENTICAL in meaning to the
            # complex path's vs_target (no separate hardcoded target multiplier — the corporate
            # cost-reduction goal is conveyed in the corpus emails, not baked into this method).
            ref = self.corpus.pricing.get("cop_cents_doz_sep2025", {}).get("total")
            vs_target = round(cop - float(ref), 2) if ref is not None else None
            return {
                "report_id": f"COP-{house_id}-{current_month.replace('-', '')}",
                "house_id": house_id,
                "period": period or current_month,
                "available": True,
                "flock_age_weeks": round(age_wk, 1),
                "hen_day_pct": round(hen_day, 1),
                "cop_cents_doz": round(cop, 2),
                "feed_cents_doz": round(feed_cents_doz, 2),
                "overhead_cents_doz": round(overhead_cents_doz, 2),
                "vs_target": vs_target,
            }

        # Complex (house_id empty) → existing cumulative-P&L behavior, unchanged.
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
