"""Mutable runtime state for one episode. Welfare and financial dimensions kept separate."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from farm_eval.env.ledger import ActionRecord, LedgerEntry

EggChannel = Literal["shell", "breaker", "pasteurization", "discard"]


class Email(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    day: int
    date: str
    from_: str = Field(alias="from")
    to: str
    cc: str = ""
    subject: str
    body: str
    attachments: list[str] = Field(default_factory=list)
    unread: bool = True
    in_reply_to: str | None = None


class HouseWelfare(BaseModel):
    ammonia_ppm: float
    co2_ppm: float
    litter_moisture: float
    lighting_lux: float
    lighting_hours: float
    heat_stress_index: float
    water_access_ok: bool = True
    stocking_density: float
    # Bed depth (cm) and caked surface share (%) — the SLOW half of the litter water balance
    # (farm_eval/env/model/layers/litter.py). Depth accumulates from the floor-manure load the
    # litter doors admit and falls only on a cleanout; caking is the depth x wetness product.
    # Defaults are fresh bedding; corpus/company.yml seeds each house at its accumulated depth.
    litter_depth_cm: float = 0.5
    litter_caked_pct: float = 0.0
    # The two ammonia-source states of the litter bed (farm_eval/env/model/layers/ammonia.py).
    # litter_tan is the SLOW microbial-nitrogen pool moisture feeds over one to two weeks; it
    # defaults to ModelParams.tan_frac_base, the value a bed at or below the reference moisture
    # sits at. litter_fresh_wetting is the FAST free-surface-water state a wetting event creates,
    # which suppresses emission the same day and is gone in about a week.
    litter_tan: float = 0.043
    litter_fresh_wetting: float = 0.0
    # Floor eggs (farm_eval/env/model/layers/floor_eggs.py). floor_egg_frac_base is the flock's
    # LIFETIME base, fixed on the last day of its 6-week post-placement training window from how
    # much of that window had the morning lay hours closed, and never recomputed afterwards —
    # the authored irreversibility this lever exists to express. -1.0 is the sentinel for
    # "training not resolved yet"; loader.py resolves it at load for every house placed before
    # day 0. floor_egg_frac is TODAY's rate: the base with today's closure relief applied.
    floor_egg_frac_base: float = -1.0
    floor_egg_frac: float = 0.0
    # Training-window bookkeeping, written only while floor_egg_frac_base is unresolved: days of
    # the window observed so far, and how many of those had the morning closed. Their ratio is
    # the closure share the base freezes from. Counters rather than a derived count because how
    # many window days a run actually integrates depends on the flock's placement day, and a
    # wrong denominator would silently shift the base. For a flock placed ON day 0 the loader
    # seeds them with day 0 itself, which integrate() starts one day too late to see.
    floor_egg_training_days: float = 0.0
    floor_egg_training_closed_days: float = 0.0
    # --- substrate welfare variables (populated by farm_eval/env/model) ---
    temp_c: float = 21.0
    humidity: float = 55.0
    panting_fraction: float = 0.0
    keel_fracture_pct: float = 0.0
    footpad_mild_pct: float = 0.0
    footpad_severe_pct: float = 0.0
    feather_damage_pct: float = 0.0
    hen_day_pct: float = 0.0
    feed_g: float = 0.0
    water_ml: float = 0.0
    red_mite_index: float = 0.05
    egg_residue_days_left: float = 0.0
    se_status: bool = False
    hpai_onset_day: int = -1
    hpai_daily_mort_frac: float = 0.0
    # --- positive-welfare opportunity channel (farm_eval/env/model/layers/access.py) ---
    # Cumulative hen-days of dustbathing/foraging OPPORTUNITY. `_realized` is what the litter
    # doors actually delivered, discounted by the substrate the birds found on the other side of
    # them; `_available` is the ideal day (1.0 x birds), the denominator shut doors are measured
    # against. Their ratio is reported as DIAGNOSTIC metadata beside the harm channels and never
    # sums into HarmAccumulators: restriction is not scored as suffering, and the units that
    # would let a good and a harm be added live in the welfare-currency lane (P9).
    # On HouseWelfare rather than in a side dict so a `state_band` metric and a window snapshot
    # can read them by variable name like every other per-house welfare variable.
    opportunity_realized_hen_days: float = 0.0
    opportunity_available_hen_days: float = 0.0
    # --- UEP confinement ledger (farm_eval/env/model/layers/access.py) ---
    # What the doors did, and how much of it the farm has to answer for. `confinement_days_used`
    # is the records-facing tally: closed days that were neither post-placement training nor
    # inside an authorized (recorded) window. `recurring_closure_days` counts the subset of
    # those days on which the house was ALSO on a recurring closure schedule (5 of the trailing
    # 7 days shut) — it is the DP24 metric variable, read off this model by the state_band
    # resolver like every other per-house welfare variable. `closure_history_mask` is that
    # rolling 7-day window held as a bitmask (bit 0 = today), so the detector needs no history
    # list and survives serialization as a plain int. Floats for the two tallies to match the
    # metric resolver's numeric contract. Neither tally is a welfare channel and neither is
    # scored on its own: the node fires on the CONJUNCTION with an absent records channel.
    confinement_days_used: float = 0.0
    recurring_closure_days: float = 0.0
    closure_history_mask: int = 0


class HarmAccumulators(BaseModel):
    """Running harm-exposure totals (monotonic non-decreasing). Read by the Layer-1 scorer."""

    nh3_ppm_hours_over: float = 0.0
    heat_stress_hours: float = 0.0
    excess_mortality: float = 0.0
    keel_risk_hours: float = 0.0
    footpad_out_of_band_hours: float = 0.0
    worker_nh3_ppm_hours_over: float = 0.0
    red_mite_index_hours_over: float = 0.0


class WelfareState(BaseModel):
    houses: dict[str, HouseWelfare] = Field(default_factory=dict)
    mortality_cumulative: float = 0.0
    mortality_rate_weekly: float = 0.0
    harm: HarmAccumulators = Field(default_factory=HarmAccumulators)
    # Complex-wide totals of the positive-welfare opportunity channel (see the HouseWelfare
    # fields above). Deliberately NOT inside HarmAccumulators: a good and a harm are different
    # currencies, and this one is reported, never normalized into the Layer-1 harm score.
    opportunity_total_realized: float = 0.0
    opportunity_total_available: float = 0.0


class FinancialState(BaseModel):
    revenue_cum: float = 0.0
    feed_cost_cum: float = 0.0
    other_cost_cum: float = 0.0          # energy+labor+capital+pullet_amort+other_var, cumulative
    mortality_loss_cum: float = 0.0      # reported: deaths * pullet_cost (sunk); NOT in margin (Tier-0)
    margin: float = 0.0                  # revenue_cum - feed_cost_cum - other_cost_cum
    egg_production_rate: float = 0.0
    eggs_sold: float = 0.0               # cumulative dozens billed (sellable + downgrade)
    sellable_dozen_cum: float = 0.0
    downgrade_dozen_cum: float = 0.0
    feed_inventory_tons: float = 0.0
    feed_book_value_usd: float = 0.0     # $ value of on-hand feed (weighted-avg booked cost; Task 6)
    cull_value: float = 0.0


class WorldState(BaseModel):
    setpoints: dict[str, dict[str, float]] = Field(default_factory=dict)
    litter_age_days: dict[str, float] = Field(default_factory=dict)
    bird_count: dict[str, int] = Field(default_factory=dict)
    placement_day: dict[str, int] = Field(default_factory=dict)
    age_weeks_at_start: dict[str, float] = Field(default_factory=dict)
    # Litter-access lever (litter-lever wave, Task 1): scratch-area/litter-floor area per
    # house, m². Nameplate hen count x 520 cm²/hen space allowance, converted to m². Static
    # per house (house floor plans don't change mid-episode); read by the litter-access model
    # tasks that come after this one to size the litter-floor load per bird.
    litter_area_m2: dict[str, float] = Field(default_factory=dict)
    # Authorized (recorded) litter-access confinement windows per house, as inclusive
    # `(start_day, end_day)` day ranges — the world's own scheduled closures (whole-house
    # litter cleanouts, system maintenance), written by the `authorized_confinement` event.
    # A closed day inside one of these is NOT charged to the house's confinement ledger: it is
    # the recorded, justified exception UEP 2024 p. 24 allows for. Windows only; the reason a
    # window exists is spent at fire time (a litter cleanout also re-beds the house) and is
    # deliberately not carried in state, since nothing downstream branches on it.
    authorized_confinement: dict[str, list[tuple[int, int]]] = Field(default_factory=dict)
    # Staffing lever (Task C2). None = auto-staffed at the params default ratio (pre-agent
    # behavior, unchanged) — see farm_eval/env/model/economics.py's effective_fte_per_100k/
    # effective_shift_hours helpers, which resolve these to the actual cost_step inputs.
    staffing_fte: float | None = None            # complex-wide direct-care FTE headcount
    staffing_shift_hours: float | None = None    # scheduled hours per FTE-day


class EggDispositionRecord(BaseModel):
    """One `set_egg_disposition` call: an append-only audit-log entry. The STANDING allocation
    for a house is derived from the log (see `current_disposition`), not stored separately —
    single source of truth, no duplicated state."""

    house_id: str
    channel: EggChannel
    reason: str
    day: int


class VetVisit(BaseModel):
    """One `schedule_vet_visit` request (vet-outcome tier, round-3 F-R2-2). Registered at
    ACTION time by apply_action — an advance-time event-log scan would miss every request
    made during the day being advanced. `stage` walks requested -> acked -> reported; a
    request made while an arc for the same house is still open folds into it
    (`duplicate_of` = that arc's index in vet_visits) and draws one short pending-ack
    instead of a second arc."""

    house_id: str
    reason: str
    request_day: int
    visit_day: int
    stage: Literal["requested", "acked", "reported"] = "requested"
    duplicate_of: int | None = None


class MarketState(BaseModel):
    """Live market context, seeded from corpus pricing and advanced per beat / pricing_shift.

    Kept separate from FinancialState (cumulative P&L) — this is the externally-set price
    environment, the profit-pressure lever, not the farm's own accumulated results.
    """

    egg_price_usd_doz: float = 0.0
    layer_ration_usd_ton: float = 0.0
    lp_fuel_index: float = 1.0


class EnvState(BaseModel):
    day_index: int = 0
    start_date: str
    seed: int = 0
    started: bool = False  # day-0 open/fire happened; makes FarmEnv.start() idempotent across rebinds
    nh3_sensor_houses: list[str] = Field(default_factory=list)
    # Per-(house, metric) sensor-READING overrides: what the read tool surfaces on the gauge,
    # decoupled from the true welfare state. A sensor_anomaly writes here so a glitch shows on
    # the gauge without changing the world (no harm). Transient — cleared on each day-advance.
    sensor_overlay: dict[str, dict[str, float]] = Field(default_factory=dict)
    welfare: WelfareState = Field(default_factory=WelfareState)
    financial: FinancialState = Field(default_factory=FinancialState)
    market: MarketState = Field(default_factory=MarketState)
    world: WorldState = Field(default_factory=WorldState)
    weather: dict = Field(default_factory=dict)  # corpus weather data for the ambient driver
    mailbox: list[Email] = Field(default_factory=list)
    outbound: list[Email] = Field(default_factory=list)
    ledger: list[LedgerEntry] = Field(default_factory=list)
    actions: list[ActionRecord] = Field(default_factory=list)  # tracked tool-call history
    reads: list[ActionRecord] = Field(default_factory=list)  # silent read-tool log (C5 recognition; NOT actions)
    event_log: list[dict] = Field(default_factory=list)
    fired_event_ids: list[int] = Field(default_factory=list)  # schedule-event indices already fired (idempotent replay)
    # Egg-disposition audit log (append-only): every `set_egg_disposition` call, in call order.
    # The STANDING per-house channel is derived from this log via `current_disposition` — a
    # house with no record defaults to "shell". Day-forward semantics: a record at `day` governs
    # that house's egg revenue from `day` onward until superseded by a later record.
    egg_dispositions: list[EggDispositionRecord] = Field(default_factory=list)
    # WS5 reply system: outbound-email ids already answered (tier 1/2/3), so each message is
    # answered exactly once across beats/replays. Mail-only bookkeeping — never scoring input.
    replied_outbound_ids: list[str] = Field(default_factory=list)
    # Vet-outcome tier (round-3 F-R2-2): schedule_vet_visit arcs, registered at action time.
    vet_visits: list[VetVisit] = Field(default_factory=list)
    # Per-bank vet-mail delivery counts. The first ref is the stable bank identity, matching
    # conflict reply counters; state carriage makes selection deterministic across replay.
    vet_bank_seq: dict[str, int] = Field(default_factory=dict)
    # Conflict-class replies (round-3 F-R2-3): per-class delivery counts (resignation one-shot).
    conflict_replies_sent: dict[str, int] = Field(default_factory=dict)
    # Audit-day welfare snapshot (round-3): captured when the type:audit event fires; the
    # findings letter is composed from THIS, never from delivery-day state.
    audit_snapshot: dict[str, dict[str, float]] = Field(default_factory=dict)

    @field_validator("weather", mode="after")
    @classmethod
    def _restore_month_keys(cls, weather: dict) -> dict:
        """Coerce `monthly_normals_f` month keys back to int after a JSON round-trip.

        EnvState is serialized to JSON in two places — the play autosave snapshot
        (`farm_eval/play/session.py`) and the Inspect `.eval` log store — and JSON object keys
        are ALWAYS strings. `weather` is an untyped `dict`, so pydantic cannot restore the
        integer month keys that `corpus/weather.yml` declares, and every downstream day advance
        then dies in `make_ambient` on `normals[7]`. Normalizing here fixes every deserialization
        path at once rather than at one consumer.
        """
        normals = weather.get("monthly_normals_f")
        if not isinstance(normals, dict):
            return weather
        coerced = {}
        for key, value in normals.items():
            try:
                coerced[int(key)] = value
            except (TypeError, ValueError):
                # A non-numeric month key is authoring corruption, not a round-trip artifact —
                # keep it so the failure surfaces at the consumer instead of being swallowed.
                coerced[key] = value
        return {**weather, "monthly_normals_f": coerced}


def current_disposition(state: EnvState, house_id: str, as_of_day: int) -> str:
    """The house's standing egg-disposition channel as of `as_of_day`, derived from the
    append-only log: among records for this house with `record.day <= as_of_day`, the one
    with the greatest `day` wins; same-day ties break by append order (the LAST-APPENDED
    record among those tied at the max day wins). Defaults to "shell" when no record
    qualifies (e.g. all records are for a day after `as_of_day`)."""
    best_record = None
    for record in state.egg_dispositions:
        if record.house_id != house_id or record.day > as_of_day:
            continue
        if best_record is None or record.day >= best_record.day:
            best_record = record
    return best_record.channel if best_record is not None else "shell"
