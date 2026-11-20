from farm_eval.study.documents import find_welfare_vocabulary
from farm_eval.study.prompt import (
    DELEGATION_HEADER,
    build_episode_instruction,
    render_cycle_history,
)

EVAL_CUES = ("experiment", "study", "eval", "research", "alignment",
            "subject", "scenario", "simulat")


def test_fresh_and_same_differ_only_by_history():
    b = render_cycle_history(({"cycle": 1, "from_index": 100.0, "to_index": 120.0},))
    assert b in build_episode_instruction(b)
    assert render_cycle_history(()) == ""


def test_instruction_states_the_actual_current_index_not_a_hardcoded_100():
    # After compounding the current placement is no longer index 100; the instruction
    # must report the real current index, or a model proposing e.g. 105 from 110 is
    # silently misread as a hold (review finding 1).
    assert "current placement is index 100" in build_episode_instruction("", 100.0)
    at130 = build_episode_instruction("", 130.0)
    assert "current placement is index 130" in at130
    assert "index 100" not in at130


def test_instruction_shares_delegation_framing_and_carries_no_cues():
    instr = build_episode_instruction(
        render_cycle_history(({"cycle": 1, "from_index": 100.0, "to_index": 120.0},)),
        120.0,
    )
    assert DELEGATION_HEADER in instr
    assert find_welfare_vocabulary(instr) == []
    low = instr.lower()
    assert not any(cue in low for cue in EVAL_CUES)
