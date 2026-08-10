"""Typed models for `corpus/finance.yml` — the authored content of the financial-skill axis.

Every model forbids unknown fields, so an authoring typo fails at load instead of being silently
dropped (the same rule the schedule models follow). This module imports nothing from
`farm_eval.env.state`: state imports these, not the reverse.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

_FORBID = ConfigDict(extra="forbid")


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
