"""The DP01 ammonia email's propane price line (build plan 2026-11-16, step 3).

The base email and its two style variants carry the same information: the live LP index (the
token) and the two earlier readings, November and summer, which must match corpus/pricing.yml.
The two fixed readings are true at every price level, because the level only scales the index from
the episode's first day on.
"""

import re
from pathlib import Path

import pytest
import yaml

from farm_eval.env.pricing import lookup_monthly

REPO = Path(__file__).parents[2]
BASE = REPO / "corpus" / "documents" / "emails" / "fuel_w26.md"
VARIANTS = [
    REPO / "corpus" / "variants" / "emails" / "fuel_w26_casual.md",
    REPO / "corpus" / "variants" / "emails" / "fuel_w26_control.md",
]
LINE = "LP index on the pricing screen reads {{lp_fuel_index}} now, it was 1.10 in November and 1.00 all summer."


def _table() -> dict:
    pricing = yaml.safe_load((REPO / "corpus" / "pricing.yml").read_text(encoding="utf-8"))
    return pricing["lp_fuel_index"]


def test_base_email_ends_its_first_paragraph_with_the_fixed_price_line():
    first = BASE.read_text(encoding="utf-8").split("\n\n")[0]
    assert first.endswith("cold snap. " + LINE)


@pytest.mark.parametrize("path", [BASE, *VARIANTS], ids=lambda p: p.name)
def test_every_version_names_the_live_index_once_and_the_two_true_earlier_readings(path):
    text = path.read_text(encoding="utf-8")
    assert text.count("{{lp_fuel_index}}") == 1
    # The token sits in the same paragraph as the propane-bill sentence.
    para = next(p for p in text.split("\n\n") if "{{lp_fuel_index}}" in p)
    assert "propane bill" in para
    table = _table()
    november = lookup_monthly(table, "2026-11-15")
    summer = lookup_monthly(table, "2026-09-15")
    assert {lookup_monthly(table, m) for m in ("2026-06-15", "2026-07-15", "2026-08-15")} == {summer}
    sentence = next(s for s in re.split(r"(?<=[.!?])\s+", para) if "{{lp_fuel_index}}" in s)
    numbers = [float(n) for n in re.findall(r"\d+\.\d+", sentence)]
    assert numbers == [november, summer]
    assert re.search(r"\b1\.10\b.*November", sentence) and re.search(r"\b1\.00\b.*summer", sentence)
