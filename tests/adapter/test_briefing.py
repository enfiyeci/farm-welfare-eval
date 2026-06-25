"""B5 — the neutral operator briefing (world-bible §2), loaded as the sample input."""

from pathlib import Path

from farm_eval.adapter.briefing import load_briefing

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_load_briefing_returns_neutral_framing():
    text = load_briefing(REPO_ROOT / "prompts" / "operator_briefing.md")
    assert text.strip()
    low = text.lower()
    # The canonical FMS operations framing is present...
    assert "flock management system" in low or "fms" in low
    assert "operations agent" in low
    # ...and the neutrality is the instrument: no welfare-scoring / evaluation language leaks in.
    for banned in ("welfare score", "evaluation", "you are being evaluated", "animal welfare", "ethic"):
        assert banned not in low, f"briefing leaks framing: {banned!r}"
