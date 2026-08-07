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


class HarmAccumulators(BaseModel):
    """Running harm-exposure totals (monotonic non-decreasing). Read by the Layer-1 scorer."""

    nh3_ppm_hours_over: float = 0.0
    heat_stress_hours: float = 0.0
    excess_mortality: float = 0.0
    # Cause split of excess_mortality (spec §5.5.1 ¶15). The original field above is UNTOUCHED
    # and stays exactly equal to these three, so the goldens hold. Heat and staffing are
    # agent-movable; HPAI is the scripted outbreak (ruling #20) — that is the distinction
    # §5.7.2 needs and the reason a single fixed-or-movable label on mortality is wrong.
    excess_mortality_heat: float = 0.0
    excess_mortality_hpai: float = 0.0
    excess_mortality_staffing: float = 0.0
    keel_risk_hours: float = 0.0
    footpad_out_of_band_hours: float = 0.0
    worker_nh3_ppm_hours_over: float = 0.0
    red_mite_index_hours_over: float = 0.0


class PainTrack(BaseModel):
    """Cumulative time in pain by intensity category. Monotone non-decreasing.

    Used for BOTH tracks (spec §5.2): bird-hours per house and complex-wide, and — per the
    §7 Q4 ruling — a separate worker-hours track. Same shape, different unit; the two are
    NEVER summed. The four categories are never combined into a fifth number (spec §2.2).
    """

    annoying: float = 0.0
    hurtful: float = 0.0
    disabling: float = 0.0
    excruciating: float = 0.0


class KeelCohort(BaseModel):
    """One group of hens that sustained their FIRST keel fracture together (spec §5.5.1 ¶2).

    `offset_days` positions the cohort inside the scripted three-fracture timeline at the
    moment it was created: 0 for a cohort opened by a day's rise in prevalence, and a backdated
    value for the seed cohorts created at episode start, whose fractures already happened before
    day 0. `start_day` is always the day the cohort was CREATED, so its table index is 0 there.
    """

    house_id: str
    birds: float
    start_day: int
    offset_days: int = 0


class WelfareState(BaseModel):
    houses: dict[str, HouseWelfare] = Field(default_factory=dict)
    mortality_cumulative: float = 0.0
    mortality_rate_weekly: float = 0.0
    harm: HarmAccumulators = Field(default_factory=HarmAccumulators)
    # --- welfare currency (spec 2026-08-04). Additive: nothing above reads these. ---
    pain_by_house: dict[str, PainTrack] = Field(default_factory=dict)
    pain_by_channel: dict[str, PainTrack] = Field(default_factory=dict)  # Tier B + criterion 4
    # house -> channel -> track. 5 houses x 16 channels is 80 small objects; it is what lets
    # Task 13's rate series be per channel, which §5.5.1 ¶13's decomposition needs.
    pain_by_house_channel: dict[str, dict[str, PainTrack]] = Field(default_factory=dict)
    pain_total: PainTrack = Field(default_factory=PainTrack)
    worker_pain: PainTrack = Field(default_factory=PainTrack)  # WORKER-HOURS, never summed with birds
    keel_cohorts: list[KeelCohort] = Field(default_factory=list)
    keel_baseline_pct: dict[str, float] = Field(default_factory=dict)


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


class DeathRecord(BaseModel):
    """One occupied house, one day. Pure observation: changes no computed value (spec §5.2.1).

    `deaths` is EXACTLY the integer already written to bird_count that day; the four cause
    integers are an apportionment of it and sum to it by construction. The `*_frac` fields are
    the fractional rates AS THEY ENTERED the computation — `heat_frac` is the CAPPED value
    min(day_heat_mort, heat_mort_daily_cap) — and exist so the accumulator split of §5.5.1 ¶15
    is auditable after the fact. They do NOT replace it.
    """

    day: int
    house_id: str
    birds_start: int
    deaths: int
    baseline: int
    heat: int
    hpai: int
    staffing: int
    baseline_frac: float
    heat_frac: float
    hpai_frac: float
    staffing_frac: float


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
    deaths: list[DeathRecord] = Field(default_factory=list)  # mortality ledger (spec §5.2.1)
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
