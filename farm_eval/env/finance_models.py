"""Typed models for `corpus/finance.yml` — the authored content of the financial-skill axis.

Every model forbids unknown fields, so an authoring typo fails at load instead of being silently
dropped (the same rule the schedule models follow). This module imports nothing from
`farm_eval.env.state`: state imports these, not the reverse.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

_FORBID = ConfigDict(extra="forbid")

# The ONLY cost coefficients a vendor offer may move. Every one of these is a pure cost line that
# no welfare layer reads, which is what makes the whole offer mechanism provably welfare-neutral.
# Widening this set requires a new neutrality probe (see the L8 plan, Task 10) — it is not a
# routine edit.
WELFARE_INERT_EFFECT_KEYS = frozenset({
    "energy_base_usd_bird_day",   # non-HVAC electricity: lights, office, egg room
    "other_var_usd_doz",          # packaging + supplies
    "maintenance_callout_usd",    # service-contract price
    "vet_visit_usd",              # service-contract price
})


class Lender(BaseModel):
    """One operating-line provider. `rate_series` is a monthly YYYY-MM table of ANNUAL rates,
    resolved with the same carry-forward semantics as the corpus price tables."""

    model_config = _FORBID

    id: str
    name: str
    kind: str = "bank"
    rate_series: dict[str, float] = Field(default_factory=dict)
    switch_fee_usd: float = 0.0
    patronage_rebate_frac: float = 0.0


class InvoiceLine(BaseModel):
    """One billed line. `error` is DESIGNER-SIDE ground truth — it is never surfaced to the agent
    by any read tool. `checkable_via` names the in-world record that proves the error, and the
    rulebook's law-1 probe asserts that record is actually reachable."""

    model_config = _FORBID

    id: str
    description: str
    amount_usd: float
    error: bool = False
    checkable_via: str = ""


class InvoiceSpec(BaseModel):
    """One authored statement. Day fields are absolute in-world day indices, authored onto the
    wake-day grid with >= 2 played days of slack (rulebook law 2, enforced by the schedule lint)."""

    model_config = _FORBID

    id: str
    vendor: str
    issued_day: int
    discount_pct: float = 0.0
    discount_day: int = 0
    net_day: int = 0
    dispute_deadline_day: int = 0
    dispute_lag_days: int = 5
    lines: list[InvoiceLine] = Field(default_factory=list)


class OfferOption(BaseModel):
    model_config = _FORBID

    id: str
    label: str
    upfront_usd: float = 0.0
    effect_key: str
    effect_multiplier: float = 1.0

    @field_validator("effect_key")
    @classmethod
    def _welfare_inert(cls, key: str) -> str:
        if key not in WELFARE_INERT_EFFECT_KEYS:
            raise ValueError(
                f"offer effect_key {key!r} is not welfare-inert; allowed keys are "
                f"{sorted(WELFARE_INERT_EFFECT_KEYS)}"
            )
        return key


class OfferSpec(BaseModel):
    model_config = _FORBID

    id: str
    vendor: str
    opens_day: int
    expires_day: int
    quality: Literal["good", "marginal", "bad", "scam"]
    options: list[OfferOption] = Field(default_factory=list)


class FinanceConfig(BaseModel):
    """The whole authored finance block. Default-constructed (every field empty, `enabled=False`)
    it is an inert no-op, so any state built without `corpus/finance.yml` behaves exactly as it
    did before this axis existed."""

    model_config = _FORBID

    enabled: bool = False
    opening_cash_usd: float = 0.0
    default_lender_id: str = ""
    lenders: dict[str, Lender] = Field(default_factory=dict)
    money_market_yield: dict[str, float] = Field(default_factory=dict)
    # Cumulative on-site feed storage across the complex (Task 6). Corpus content, not a
    # ModelParams field: the bin capacity of THIS complex is farm content. 0.0 = uncapped,
    # so a corpus without the key behaves exactly as the world did before Task 6.
    feed_storage_cap_tons: float = 0.0
    # Authored statements (Task 4, M5/M6), keyed by invoice id. A schedule `invoice` event looks
    # one up here to fire it; `finance.open_invoice` also registers a directly-passed spec here
    # (idempotent) so a later pay_invoice/dispute_charge can resolve it without a schedule event.
    invoices: dict[str, InvoiceSpec] = Field(default_factory=dict)
    offers: dict[str, OfferSpec] = Field(default_factory=dict)
