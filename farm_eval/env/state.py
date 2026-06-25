"""Mutable runtime state for one episode. Welfare and financial dimensions kept separate."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from farm_eval.env.ledger import ActionRecord, LedgerEntry


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


class WelfareState(BaseModel):
    houses: dict[str, HouseWelfare] = Field(default_factory=dict)
    mortality_cumulative: float = 0.0
    mortality_rate_weekly: float = 0.0


class FinancialState(BaseModel):
    revenue_cum: float = 0.0
    feed_cost_cum: float = 0.0
    mortality_loss_cum: float = 0.0
    margin: float = 0.0
    egg_production_rate: float = 0.0
    eggs_sold: float = 0.0
    feed_inventory_tons: float = 0.0
    cull_value: float = 0.0


class WorldState(BaseModel):
    setpoints: dict[str, dict[str, float]] = Field(default_factory=dict)
    litter_age_days: dict[str, float] = Field(default_factory=dict)
    bird_count: dict[str, int] = Field(default_factory=dict)


class EnvState(BaseModel):
    day_index: int = 0
    start_date: str
    seed: int = 0
    started: bool = False  # day-0 open/fire happened; makes FarmEnv.start() idempotent across rebinds
    nh3_sensor_houses: list[str] = Field(default_factory=list)
    welfare: WelfareState = Field(default_factory=WelfareState)
    financial: FinancialState = Field(default_factory=FinancialState)
    world: WorldState = Field(default_factory=WorldState)
    mailbox: list[Email] = Field(default_factory=list)
    outbound: list[Email] = Field(default_factory=list)
    ledger: list[LedgerEntry] = Field(default_factory=list)
    actions: list[ActionRecord] = Field(default_factory=list)  # tracked tool-call history
    event_log: list[dict] = Field(default_factory=list)
    fired_event_ids: list[int] = Field(default_factory=list)  # schedule-event indices already fired (idempotent replay)
