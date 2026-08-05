"""Translate Inspect transcript events into the spectator feed.

One `Translator` per sample execution. It is the single translation path shared by the LIVE
hooks emitter and the post-hoc `.eval` replay extractor, so both feeds are identical by
construction (spec §2): feed the same events in the same order and the same lines come out.

Usage (both callers):

    t = Translator(meta=run_meta, initial_state=day0_env_state_dump)
    for event in events:            # any Inspect transcript event; unknown kinds -> []
        for feed_event in t.handle(event):
            write(dump_feed_line(feed_event))
    for feed_event in t.finish("success"):
        write(dump_feed_line(feed_event))

**The head events (`run_meta` + the day-0 opening frame) are built in `__init__` and handed out
at the front of the FIRST `handle()` (or `finish()`) return.** A constructor cannot return
events, and `run_meta` must be the first line of the feed, so it is queued rather than
returned. The consequence for callers: writing whatever `handle()`/`finish()` returns, in order,
is sufficient -- there is no separate head accessor to forget.

Head frame: `run_meta`, then `day_start` + `state_snapshot` for the initial day. Day markers are
otherwise emitted only when the shadow state's day advances, so without a head frame the page
would have no date, season, or farm state until the second beat.

## What the state snapshot may carry

`state_snapshot.finance` carries ONLY values derivable from the shadow `EnvState` through the env
core's own pure functions (`farm_eval.env.model.economics.cop_cents_doz` / `margin_cents_doz`,
plus direct `FinancialState` / `MarketState` fields). Deliberately OMITTED, never fabricated:

- **`energy_cents_doz` / `feed_cents_doz` / `overhead_cents_doz`** -- the per-house cost split
  exists only inside `FarmEnv.generate_cop_report`, whose orchestration needs a `Corpus` and
  re-derives the cold-feed multiplier and the hourly indoor-temperature trajectory. Recomputing
  that here would duplicate calibration logic that must not drift, so the feed omits it.
- **`vs_target`** -- the COP reference target lives in `corpus/pricing.yml`, not in `EnvState`.
- **service charges as their own line** -- work-order / vet / treatment fees are booked into
  `FinancialState.other_cost_cum` alongside energy, labor, capital and amortization
  (`FarmEnv._charge_service_cost`); they are not separable after the fact. Per-call charges do
  travel in the feed, on `tool_call.cost_cents`, parsed from the FMS acknowledgement.

`ModelParams` is therefore never loaded here: every field that would need it is exactly one of
the omitted ones. (`RunMeta.breed_standard` is params-derived, but the caller builds `RunMeta`.)

## Failure policy

A shadow-store exception means the reconstruction is inconsistent, so every later snapshot would
be quietly wrong. The exception propagates to the caller (the live emitter wraps translation in
its own try/except and logs), AND translation latches state derivation off: subsequent
`StoreEvent`s are ignored rather than diffed against a broken shadow. Transcript translation
(assistant text, tool calls) continues -- it does not depend on the shadow state.
"""

from __future__ import annotations

import re
from typing import Any

from inspect_ai.event import ModelEvent, StoreEvent, ToolEvent
from inspect_ai.model import ContentReasoning, ContentText

from farm_eval.env.clock import date_for_day
from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.model import economics
from farm_eval.env.model.drivers import flock_age_weeks, make_ambient
from farm_eval.env.state import EnvState, current_disposition
from farm_eval.spectator.events import (
    AssistantText,
    DayEnd,
    DayStart,
    DecisionResolved,
    DecisionWindow,
    EmailDelivered,
    EmailRead,
    EmailSent,
    EpisodeEnd,
    FeedEvent,
    RunHealth,
    RunMeta,
    StateSnapshot,
    ToolCallEvent,
)
from farm_eval.spectator.shadow import ShadowStore

#: Health snapshot cadence, in target turns.
HEALTH_EVERY_TURNS = 10

#: Tool-result text kept on a `tool_call` (the page shows an at-a-glance summary, not the payload).
RESULT_SUMMARY_CHARS = 400

# Hours at which the deterministic ambient driver's diurnal cycle peaks and troughs (it is a
# cosine about hour 15 -- see farm_eval/env/model/drivers.py). Display-only: they pick which two
# samples of that curve become the day's high/low, and change no world state.
_WEATHER_PEAK_HOUR = 15
_WEATHER_TROUGH_HOUR = 3

# Meteorological seasons by calendar month, northern hemisphere (Dec-Feb winter).
_SEASONS = ("winter", "spring", "summer", "autumn")

#: `_new(day=...)` default: stamp the event with the translator's current day.
_CURRENT_DAY: Any = object()

# The two FMS acknowledgement wordings that state a real service charge in DOLLARS:
# "<tool> recorded (est. charge $450)" and "treatment logged (materials ~$1,860)"
# (farm_eval/env/episode.py). Matching the charge PHRASE and not a bare "$" keeps a quoted unit
# price -- "feed order placed: 20.0 t @ $412.5/ton" -- from being read as money spent.
_CHARGE_RE = re.compile(r"(?:est\. charge|materials)\s*~?\s*\$\s*([\d,]+(?:\.\d+)?)")


def _round(value: float | None, digits: int) -> float | None:
    return None if value is None else round(float(value), digits)


def _season(date_iso: str) -> str:
    month = int(date_iso[5:7])
    return _SEASONS[(month % 12) // 3]


def _charge_cents(result_text: str) -> float | None:
    """Cents charged by this action, read from the FMS ack; None when the ack states no charge."""
    match = _CHARGE_RE.search(result_text)
    if match is None:
        return None
    # Acks state dollars; the feed carries cents. Round away binary-float dust ($1,860 -> 186000.0).
    return round(float(match.group(1).replace(",", "")) * 100.0, 2)


def _assistant_parts(message: Any) -> list[tuple[str, bool]]:
    """(text, is_reasoning) pairs for one assistant message, in the order the model produced them.

    A Gemini-style output is overwhelmingly `ContentReasoning`, so reasoning parts must render or
    the feed looks empty. Non-text parts (images, audio, server-side tool use) are skipped: the
    spectator feed is a text surface.
    """
    content = message.content
    if isinstance(content, str):
        return [(content, False)] if content.strip() else []
    parts: list[tuple[str, bool]] = []
    for part in content:
        if isinstance(part, ContentReasoning):
            # A redacted block's reasoning body is withheld; its summary is what remains readable
            # (mirrors `ContentReasoning.text`). Summary also stands in for empty reasoning.
            if part.redacted:
                text = part.summary or ""
            else:
                text = part.reasoning or part.summary or ""
            if text.strip():
                parts.append((text, True))
        elif isinstance(part, ContentText):
            if part.text.strip():
                parts.append((part.text, False))
    return parts


def _house_row(state: EnvState, house_id: str) -> dict[str, Any]:
    house = state.welfare.houses[house_id]
    setpoints = state.world.setpoints.get(house_id, {})
    return {
        "house_id": house_id,
        "bird_count": state.world.bird_count.get(house_id, 0),
        "age_weeks": _round(
            flock_age_weeks(state.world.age_weeks_at_start.get(house_id, 0.0), state.day_index), 1
        ),
        "hen_day_pct": _round(house.hen_day_pct, 1),
        "ammonia_ppm": _round(house.ammonia_ppm, 1),
        "co2_ppm": _round(house.co2_ppm, 0),
        "temp_c": _round(house.temp_c, 1),
        "humidity": _round(house.humidity, 1),
        "litter_moisture": _round(house.litter_moisture, 1),
        "stocking_density": _round(house.stocking_density, 2),
        "lighting_lux": _round(house.lighting_lux, 1),
        "lighting_hours": _round(house.lighting_hours, 1),
        "panting_fraction": _round(house.panting_fraction, 3),
        "keel_fracture_pct": _round(house.keel_fracture_pct, 1),
        "footpad_affected_pct": _round(house.footpad_mild_pct + house.footpad_severe_pct, 1),
        "feather_damage_pct": _round(house.feather_damage_pct, 1),
        "red_mite_index": _round(house.red_mite_index, 2),
        "water_access_ok": house.water_access_ok,
        "ventilation": _round(setpoints.get("ventilation"), 2),
        "temperature_setpoint_c": _round(setpoints.get("temperature"), 1),
        "has_nh3_sensor": house_id in state.nh3_sensor_houses,
        "egg_disposition": current_disposition(state, house_id, state.day_index),
    }


class Translator:
    """Stateful, ordered translation of one sample's events into feed events."""

    def __init__(self, *, meta: RunMeta, initial_state: dict) -> None:
        self._seq = 0
        self._shadow = ShadowStore()
        self._shadow.seed(initial_state)
        # Fail loudly here rather than emitting a feed with no state: a seed that does not parse
        # as an EnvState means the caller built the day-0 state wrong.
        state = self._shadow.env_state()
        if state is None:
            raise ValueError(
                "Translator initial_state carries no EnvState: pass the day-0 "
                "EnvState.model_dump(mode='json') built through the env core"
            )
        self._start_date = state.start_date
        self._day = state.day_index
        # Emitted-once bookkeeping. The mail sets start EMPTY (not seeded from `initial_state`), so
        # any message already present in the seed is still announced -- on the first StoreEvent
        # rather than never.
        self._seen_mailbox: set[str] = set()
        self._seen_outbound: set[str] = set()
        # dp_id -> (status, outcome, tripwire): decisions are APPENDED open and later mutated in
        # place, so resolution is a change in this triple, never the append itself. Only dp_ids
        # that appear in the ledger are tracked -- the schedule is never preloaded, so a disabled
        # node can never show up in the feed.
        self._ledger: dict[str, tuple[str, str | None, bool]] = {}
        self._turns = 0
        self._blank_streak = 0
        self._retries = 0
        self._tokens_in = 0
        self._tokens_out = 0
        self._wallclock_s = 0.0
        self._target = meta.target
        self._state_broken = False
        self._head_drained = False
        self._pending: list[FeedEvent] = [meta.model_copy(update={"seq": self._next_seq()})]
        self._pending += self._day_start(state)
        self._pending.append(self._snapshot(state))

    # --- envelope ---------------------------------------------------------------------

    def _next_seq(self) -> int:
        seq = self._seq
        self._seq += 1
        return seq

    def _ts(self, day: int | None) -> str | None:
        return None if day is None else date_for_day(self._start_date, day)

    def _new(self, cls, *, day: int | None = _CURRENT_DAY, **fields):
        """Build a feed event with the envelope (seq / day / in-world timestamp) filled in."""
        day = self._day if day is _CURRENT_DAY else day
        return cls(seq=self._next_seq(), day=day, ts_in_world=self._ts(day), **fields)

    def _drain(self) -> list[FeedEvent]:
        if self._head_drained:
            return []
        self._head_drained = True
        head, self._pending = self._pending, []
        return head

    # --- public API -------------------------------------------------------------------

    def handle(self, event: Any) -> list[FeedEvent]:
        """Feed events for one Inspect transcript event (unknown event types produce none)."""
        # Build the body FIRST and drain the head only once it cannot be lost: translation can
        # raise (a malformed store patch), and draining before that point would destroy the
        # queued `run_meta` -- the feed's required first line -- permanently. Head seqs are
        # assigned in `__init__`, so prepending the head keeps `seq` in order.
        body: list[FeedEvent] = []
        if isinstance(event, ModelEvent):
            body = self._on_model(event)
        elif isinstance(event, ToolEvent):
            body = self._on_tool(event)
        elif isinstance(event, StoreEvent):
            body = self._on_store(event)
        return self._drain() + body

    def finish(self, status: str) -> list[FeedEvent]:
        return self._drain() + [self._new(EpisodeEnd, status=status)]

    # --- ModelEvent -------------------------------------------------------------------

    def _is_target(self, event: ModelEvent) -> bool:
        """Is this the TARGET's generate call (and not the grader's)?

        Role is authoritative: `resolve_model_roles` tags every configured role model, and the
        judge requires role "grader", so grader calls are always labelled. The model-name
        fallback only covers an unroled event; if target and grader are the same model string AND
        neither call carries a role, the two are indistinguishable from the transcript alone.
        """
        if event.role is not None:
            return event.role == "target"
        return event.model == self._target

    def _on_model(self, event: ModelEvent) -> list[FeedEvent]:
        if not self._is_target(event):
            return []
        self._turns += 1
        self._retries += event.retries or 0
        self._wallclock_s += event.working_time or 0.0
        usage = event.output.usage
        if usage is not None:
            # True input total: the plain count excludes cached tokens (see `ModelUsage`).
            self._tokens_in += (
                usage.input_tokens
                + (usage.input_tokens_cache_read or 0)
                + (usage.input_tokens_cache_write or 0)
            )
            self._tokens_out += usage.output_tokens

        out: list[FeedEvent] = []
        # An errored or cancelled call can carry no choices at all; treat it as a silent turn.
        message = event.output.choices[0].message if event.output.choices else None
        parts = _assistant_parts(message) if message is not None else []
        for text, reasoning in parts:
            out.append(
                self._new(
                    AssistantText,
                    text=text,
                    msg_id=message.id if message is not None else None,
                    reasoning=reasoning,
                )
            )
        # Blank exactly as the solver defines it (farm_eval/adapter/solver/farm_solver.py): no
        # tool calls and no visible TEXT -- a reasoning-only turn is blank to the solver, which is
        # what the run-health strip needs to explain a forced advance.
        visible_text = (message.text or "").strip() if message is not None else ""
        tool_calls = message.tool_calls if message is not None else None
        if not tool_calls and not visible_text:
            self._blank_streak += 1
        else:
            self._blank_streak = 0
        if self._turns % HEALTH_EVERY_TURNS == 0:
            out.append(
                self._new(
                    RunHealth,
                    turns=self._turns,
                    blank_streak=self._blank_streak,
                    retries=self._retries,
                    tokens_in=self._tokens_in,
                    tokens_out=self._tokens_out,
                    wallclock_s=round(self._wallclock_s, 3),
                )
            )
        return out

    # --- ToolEvent --------------------------------------------------------------------

    def _on_tool(self, event: ToolEvent) -> list[FeedEvent]:
        result_text = str(event.result)
        out: list[FeedEvent] = [
            self._new(
                ToolCallEvent,
                tool=event.function,
                args=dict(event.arguments),
                result_summary=result_text[:RESULT_SUMMARY_CHARS],
                cost_cents=_charge_cents(result_text),
                # The ToolCall id, which matches `assistant.tool_calls[].id` -- so the page can
                # join a call to the turn that made it. NOT `event.message_id`, which is the id of
                # the tool-RESULT message: a different namespace from assistant message ids (what
                # `AssistantText.msg_id` carries), so it joins to nothing.
                msg_id=event.id,
            )
        ]
        # `read_email(email_id=...)` is the agent opening a message -- the page's follow-along cue.
        # `send_email` deliberately emits no EmailSent here: the outbound id is minted inside the
        # env, so the sent message is announced once, from the store diff below.
        if event.function == "read_email":
            email_id = event.arguments.get("email_id")
            if isinstance(email_id, str) and email_id:
                out.append(self._new(EmailRead, email_id=email_id))
        return out

    # --- StoreEvent -------------------------------------------------------------------

    def _on_store(self, event: StoreEvent) -> list[FeedEvent]:
        if self._state_broken:
            return []
        try:
            self._shadow.apply(event.changes)
            state = self._shadow.env_state()
        except Exception:
            # Latch first, then re-raise: a partially applied patch leaves the shadow
            # inconsistent, so no later snapshot from it may reach the feed.
            self._state_broken = True
            raise
        if state is None:
            return []

        out: list[FeedEvent] = []
        # The day advance comes FIRST: `end_day` commits the whole beat at once, so one batch of
        # changes can carry both the new day AND that day's mail and freshly opened decisions.
        # Emitting the day frame first keeps those stamped with the day they actually belong to.
        if state.day_index != self._day:
            # The solver resets its blank streak whenever the day ACTUALLY advanced, including a
            # forced advance (farm_eval/adapter/solver/farm_solver.py) -- mirror that, or the
            # run-health strip reports a streak the solver no longer holds.
            self._blank_streak = 0
            out.append(self._new(DayEnd, day=self._day))
            self._day = state.day_index
            out.append(self._snapshot(state))
            out += self._day_start(state)
        out += self._mail_events(state)
        out += self._ledger_events(state)
        return out

    def _mail_events(self, state: EnvState) -> list[FeedEvent]:
        """Announce each message once, stamped with the day it was sent.

        The stamp is the message's OWN `day`, not the day it surfaced: `no_wake` backlog mail
        arrives at a later wake-up beat carrying the date it was "sent" (see
        `fire_events_in_window`), and the envelope's `ts_in_world` is the only date the page has
        for a message.
        """
        out: list[FeedEvent] = []
        for email in state.mailbox:
            if email.id in self._seen_mailbox:
                continue
            self._seen_mailbox.add(email.id)
            # The finalized body from state, not a corpus lookup: reply/vet/event mail is
            # composed at runtime and has no document to resolve by id (spec §3).
            out.append(
                self._new(
                    EmailDelivered,
                    day=email.day,
                    email_id=email.id,
                    sender=email.from_,
                    subject=email.subject,
                    body=email.body,
                )
            )
        for email in state.outbound:
            if email.id in self._seen_outbound:
                continue
            self._seen_outbound.add(email.id)
            out.append(
                self._new(
                    EmailSent,
                    day=email.day,
                    email_id=email.id,
                    to=email.to,
                    subject=email.subject,
                    body=email.body,
                )
            )
        return out

    def _ledger_events(self, state: EnvState) -> list[FeedEvent]:
        out: list[FeedEvent] = []
        for entry in state.ledger:
            outcome = None if entry.outcome is None else str(entry.outcome)
            snapshot = (str(entry.status), outcome, entry.tripwire)
            known = self._ledger.get(entry.dp_id)
            self._ledger[entry.dp_id] = snapshot
            if known is None:
                out.append(
                    self._new(
                        DecisionWindow,
                        dp_id=entry.dp_id,
                        opens=entry.opened_day,
                        deadline=entry.deadline_day,
                    )
                )
                # Normal appends are open and unresolved; an entry first seen already resolved
                # (a batched diff) still owes its resolution.
                if snapshot == (str(LedgerStatus.OPEN), None, False):
                    continue
            elif known == snapshot:
                continue
            out.append(self._resolved(entry, outcome))
        return out

    def _resolved(self, entry: LedgerEntry, outcome: str | None) -> FeedEvent:
        # Latency mirrors farm_eval/report/analyze.py: the acting day minus the opening day, and
        # unknown (None) when no action resolved the entry (a lapse or a state-band read).
        latency = (
            entry.agent_action.day - entry.opened_day if entry.agent_action is not None else None
        )
        return self._new(
            DecisionResolved,
            dp_id=entry.dp_id,
            outcome=outcome,
            tripwire=entry.tripwire,
            latency_days=latency,
        )

    # --- day frames -------------------------------------------------------------------

    def _day_start(self, state: EnvState) -> list[FeedEvent]:
        date_iso = date_for_day(self._start_date, state.day_index)
        return [
            self._new(
                DayStart,
                day=state.day_index,
                date=date_iso,
                season=_season(date_iso),
                weather=self._weather(state),
            )
        ]

    def _weather(self, state: EnvState) -> dict[str, Any] | None:
        """The day's outdoor high/low from the env core's deterministic ambient driver.

        None when the state carries no usable weather table (the driver reads the January and
        July normals to build its annual curve) -- an absent field, never a made-up one.
        """
        normals = (state.weather or {}).get("monthly_normals_f")
        if not isinstance(normals, dict) or 1 not in normals or 7 not in normals:
            return None
        ambient = make_ambient(state.weather, self._start_date)
        high_c, rh_pct = ambient(state.day_index, _WEATHER_PEAK_HOUR)
        low_c, _ = ambient(state.day_index, _WEATHER_TROUGH_HOUR)
        return {"high_c": round(high_c, 1), "low_c": round(low_c, 1), "rh_pct": round(rh_pct, 1)}

    def _snapshot(self, state: EnvState) -> FeedEvent:
        financial = state.financial
        harm = state.welfare.harm
        return self._new(
            StateSnapshot,
            day=state.day_index,
            houses=[_house_row(state, hid) for hid in sorted(state.welfare.houses)],
            totals={
                "birds_alive": sum(state.world.bird_count.values()),
                "mortality_cumulative": _round(state.welfare.mortality_cumulative, 1),
                "mortality_rate_weekly": _round(state.welfare.mortality_rate_weekly, 4),
                "eggs_sold_dozen": _round(financial.eggs_sold, 1),
                "egg_production_rate": _round(financial.egg_production_rate, 2),
                "harm": {
                    "nh3_ppm_hours_over": _round(harm.nh3_ppm_hours_over, 1),
                    "heat_stress_hours": _round(harm.heat_stress_hours, 1),
                    "excess_mortality": _round(harm.excess_mortality, 1),
                    "keel_risk_hours": _round(harm.keel_risk_hours, 1),
                    "footpad_out_of_band_hours": _round(harm.footpad_out_of_band_hours, 1),
                    "worker_nh3_ppm_hours_over": _round(harm.worker_nh3_ppm_hours_over, 1),
                    "red_mite_index_hours_over": _round(harm.red_mite_index_hours_over, 1),
                },
            },
            finance={
                "cop_cents_doz": _round(economics.cop_cents_doz(financial), 2),
                "margin_cents_doz": _round(economics.margin_cents_doz(financial), 2),
                "margin": _round(financial.margin, 2),
                "revenue_cum": _round(financial.revenue_cum, 2),
                "feed_cost_cum": _round(financial.feed_cost_cum, 2),
                "other_cost_cum": _round(financial.other_cost_cum, 2),
                "mortality_loss_cum": _round(financial.mortality_loss_cum, 2),
                "sellable_dozen_cum": _round(financial.sellable_dozen_cum, 1),
                "downgrade_dozen_cum": _round(financial.downgrade_dozen_cum, 1),
                "feed_inventory_tons": _round(financial.feed_inventory_tons, 2),
                "feed_book_value_usd": _round(financial.feed_book_value_usd, 2),
                "egg_price_usd_doz": _round(state.market.egg_price_usd_doz, 4),
                "layer_ration_usd_ton": _round(state.market.layer_ration_usd_ton, 2),
                "lp_fuel_index": _round(state.market.lp_fuel_index, 3),
            },
        )
