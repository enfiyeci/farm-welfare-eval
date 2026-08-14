"""Task 8: the rulebook's mechanical enforcement — law 2 (deadlines) and the sync guard."""
import pathlib
import re

import pytest

from farm_eval.env.finance_models import FinanceConfig
from farm_eval.env.loader import load_corpus, load_schedule

RULEBOOK = pathlib.Path("evals/hen/design/financial-rulebook.md")
# Soft deadline — the early-pay discount window: the agent must get a few active (wake) days on the
# lever, not one last-chance day (owner ruling 2026-08-13).
MIN_DISCOUNT_SLACK_WAKE_DAYS = 3
# Hard deadlines — the dispute window and an offer's expiry: missing one is a real loss, so >= 2.
MIN_HARD_SLACK_WAKE_DAYS = 2


@pytest.fixture(scope="module")
def cfg() -> FinanceConfig:
    return FinanceConfig.model_validate(load_corpus("corpus").finance)


@pytest.fixture(scope="module")
def wake_days() -> list[int]:
    return load_schedule("schedule").event_days()


def _wake_days_between(wake_days, lo: int, hi: int) -> int:
    return sum(1 for d in wake_days if lo < d <= hi)


def test_the_rulebook_exists_with_one_entry_per_move():
    text = RULEBOOK.read_text(encoding="utf-8")
    for move in ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"):
        assert re.search(rf"^#+ .*\b{move}\b", text, re.M), f"no rulebook entry for {move}"


def test_every_rulebook_entry_carries_the_five_schema_sections():
    text = RULEBOOK.read_text(encoding="utf-8")
    for heading in ("The arithmetic", "The information surface", "Why it is realistic",
                    "The scoring hook"):
        assert text.count(heading) >= 8, f"{heading!r} is missing from some entry"


def test_rulebook_numbers_match_the_corpus(cfg):
    """The sync guard, mirroring tests/judge/test_rubric_sync.py: a rate quoted in the rulebook
    that no longer matches corpus/finance.yml fails here rather than misleading a reader."""
    text = RULEBOOK.read_text(encoding="utf-8")
    for lender in cfg.lenders.values():
        for month, rate in lender.rate_series.items():
            quoted = f"{rate * 100:.2f}%"
            assert quoted in text, f"{lender.id} {month} rate {quoted} is not quoted in the rulebook"
        if lender.switch_fee_usd:
            assert f"${lender.switch_fee_usd:,.0f}" in text
    # The opening balance sheet, pinned for the same reason (Task 9b review F2). The document's
    # guarantee is that EVERY number in it is quoted from the corpus, and M1/M3/M4 now turn on
    # these two: the working-capital buffer, and the balance the operating line opens carrying.
    assert f"${cfg.opening_cash_usd:,.0f}" in text
    assert f"${cfg.opening_revolver_drawn_usd:,.0f}" in text


# --- Law 2: wake-day-aligned deadlines ---

def test_every_invoice_deadline_leaves_enough_wake_days(cfg, wake_days):
    for spec in cfg.invoices.values():
        assert spec.issued_day in wake_days, f"{spec.id} is issued on a day the agent never sees"
        for name, deadline, minimum in (
            ("discount_day", spec.discount_day, MIN_DISCOUNT_SLACK_WAKE_DAYS),
            ("dispute_deadline_day", spec.dispute_deadline_day, MIN_HARD_SLACK_WAKE_DAYS),
        ):
            if not deadline:
                continue
            slack = _wake_days_between(wake_days, spec.issued_day, deadline)
            assert slack >= minimum, (
                f"{spec.id}.{name}: only {slack} wake day(s) between issue and deadline "
                f"(need >= {minimum})"
            )


def test_every_offer_expiry_leaves_two_wake_days(cfg, wake_days):
    for spec in cfg.offers.values():
        assert spec.opens_day in wake_days, f"{spec.id} opens on a day the agent never sees"
        slack = _wake_days_between(wake_days, spec.opens_day, spec.expires_day)
        assert slack >= MIN_HARD_SLACK_WAKE_DAYS, (
            f"{spec.id}: only {slack} wake day(s) between the pitch and expiry"
        )
