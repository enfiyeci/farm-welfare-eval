from farm_eval.env.loader import load_corpus, load_schedule, build_initial_state
from farm_eval.env.events import open_due_decision_points
from pathlib import Path

FIX = Path(__file__).parent.parent / "fixtures"


def test_opening_a_dp_carries_its_stakeholder_to_the_ledger():
    corpus = load_corpus(FIX / "corpus")
    schedule = load_schedule(FIX / "schedule")
    # Inject a stakeholder onto the first fixture decision point, then open it.
    schedule.decision_points[0].stakeholder = ["animal", "worker"]
    state = build_initial_state(corpus)
    open_due_decision_points(state, schedule, day=schedule.decision_points[0].opens_day)
    entry = next(e for e in state.ledger if e.dp_id == schedule.decision_points[0].id)
    assert entry.stakeholder == ["animal", "worker"]
