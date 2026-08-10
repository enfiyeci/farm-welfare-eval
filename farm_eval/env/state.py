"""Mutable runtime state for one episode. Welfare and financial dimensions kept separate."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from farm_eval.env.finance_models import FinanceConfig
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
    keel_risk_hours: float = 0.0
    footpad_out_of_band_hours: float = 0.0
    worker_nh3_ppm_hours_over: float = 0.0
    red_mite_index_hours_over: float = 0.0


class WelfareState(BaseModel):
    houses: dict[str, HouseWelfare] = Field(default_factory=dict)
    mortality_cumulative: float = 0.0
    mortality_rate_weekly: float = 0.0
    harm: HarmAccumulators = Field(default_factory=HarmAccumulators)


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
    # --- financial-skill axis (L8). Welfare layers never read these. ---
    cash_balance: float = 0.0            # cash on hand; auto-draw keeps it >= 0
    revolver_drawn: float = 0.0          # outstanding operating-line balance
    interest_paid_cum: float = 0.0       # cumulative interest, also booked into other_cost_cum
    sweep_enabled: bool = False          # idle-cash sweep toggle (M3)
    sweep_earned_cum: float = 0.0        # cumulative sweep earnings, booked as a negative cost
    finance_opening_cash: float = 0.0    # the authored working-capital buffer, for the identity
    finance_settled_basis: float = 0.0   # last settled (margin - feed_book_value_usd)


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


class LenderState(BaseModel):
    """Which operating line is active, and the switching history. Kept apart from FinancialState
    (cumulative dollars) — this is the standing arrangement, not an accumulated result."""

    model_config = ConfigDict(extra="forbid")

    active_lender_id: str = ""
    switch_days: list[int] = Field(default_factory=list)
    switch_fees_cum: float = 0.0
    patronage_rebate_cum: float = 0.0


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
    finance: FinanceConfig = Field(default_factory=FinanceConfig)  # authored corpus/finance.yml
    lender: LenderState = Field(default_factory=LenderState)
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
