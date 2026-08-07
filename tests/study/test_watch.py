import io

from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.offer import build_offer
from farm_eval.study.params import rungs_for
from farm_eval.study.response import Decision
from farm_eval.study.watch import live_line


def _kwargs(**over):
    cell = Cell(species=Species.HEN, scale=Scale.LARGE, standard=StandardBand.BEYOND,
                economics=Economics.EQUALIZED)
    rung = rungs_for(Species.HEN, StandardBand.BEYOND)[-1]
    base = dict(cell=cell, gain=0.08, rung=rung, replicate=0,
                offer=build_offer(cell, rung, 0.08), decision=Decision.ACCEPT,
                response="Revenue rises.\n\nDECISION: ACCEPT")
    base.update(over)
    return base


def test_line_shows_the_decision_the_stakes_and_the_reasoning():
    buf = io.StringIO()
    live_line(stream=buf, **_kwargs())
    text = buf.getvalue()
    assert "ACCEPT" in text
    assert "+9.0pp" in text
    assert "95.0%->86.0%" in text
    assert "50,000->210,000" in text     # the mortality count, now stated
    assert "Revenue rises." in text


def test_the_decision_line_is_not_repeated_as_reasoning():
    """The verdict is already rendered; echoing it wastes the line."""
    buf = io.StringIO()
    live_line(stream=buf, **_kwargs(response="Because X.\n**DECISION: DECLINE**",
                                    decision=Decision.DECLINE))
    body = buf.getvalue().splitlines()[1]
    assert "Because X." in body
    assert "DECISION" not in body


def test_long_reasoning_is_clipped_rather_than_wrapped():
    buf = io.StringIO()
    live_line(stream=buf, width=40, **_kwargs(response="word " * 200 + "\nDECISION: ACCEPT"))
    body = buf.getvalue().splitlines()[1]
    assert len(body.strip()) <= 40
    assert body.rstrip().endswith("…")
