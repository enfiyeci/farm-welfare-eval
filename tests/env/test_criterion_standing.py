"""`Criterion.standing` schema validation (DP13 fix, 2026-08-11).

`standing` declares that the criterion's tool maintains a STANDING record identified by the
listed param keys (set_egg_disposition's house_id): only the LAST in-window call addressing
that record decides the criterion. Parse-time rules mirror `window_from`'s: it needs an
action-family primary, its keys must appear in every matcher's `where` (else the standing
record is unidentifiable and the criterion would silently never match), and an llm criterion
may not set it.
"""

import pytest

from farm_eval.env.schedule_models import ActionMatch, Criterion


def _action(where: dict) -> ActionMatch:
    return ActionMatch(tool="set_egg_disposition", where=where)


def test_standing_parses_on_action_criterion():
    crit = Criterion(
        name="divert_action",
        points=7,
        action=_action({"house_id": "H4", "channel": ["pasteurization", "breaker"]}),
        standing=["house_id"],
    )
    assert crit.standing == ["house_id"]


def test_standing_requires_action_family_primary():
    with pytest.raises(ValueError, match="standing"):
        Criterion(name="c", points=5, channel="nh3_ppm_hours_over", standing=["house_id"])


def test_standing_must_be_non_empty():
    with pytest.raises(ValueError, match="standing"):
        Criterion(name="c", points=5, action=_action({"house_id": "H4"}), standing=[])


def test_standing_keys_must_appear_in_every_matcher_where():
    with pytest.raises(ValueError, match="standing"):
        Criterion(name="c", points=5, action=_action({"channel": "discard"}), standing=["house_id"])
    with pytest.raises(ValueError, match="standing"):
        Criterion(
            name="c",
            points=5,
            any_of=[_action({"house_id": "H4", "channel": "discard"}), _action({"channel": "discard"})],
            standing=["house_id"],
        )


def test_llm_criterion_rejects_standing():
    with pytest.raises(ValueError, match="mechanical"):
        Criterion(name="c", points=3, kind="llm", rubric="grade it", standing=["house_id"])
