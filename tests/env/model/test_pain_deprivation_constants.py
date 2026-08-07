import pytest
from farm_eval.env.model.pain import nest_pain, roosting_pain, foraging_pain
from farm_eval.env.model.pain_params import PainParams

PP = PainParams()


def test_nest_pain_scales_with_the_lay_rate():
    a = nest_pain(95.0, 1000, 1.0, PP).disabling
    b = nest_pain(47.5, 1000, 1.0, PP).disabling
    assert a == pytest.approx(2.0 * b)


def test_nest_pain_populates_disabling_and_hurtful_only():
    d = nest_pain(95.0, 1000, 1.0, PP)
    assert d.disabling > 0.0 and d.hurtful > 0.0
    assert (d.annoying, d.excruciating) == (0.0, 0.0)


def test_nest_reproduces_the_published_per_affected_bird_cycle_anchor():
    # Ch. 6: 324 h Disabling per AFFECTED bird per cycle. Our cycle is 490 laying days at a
    # ~95% rate; the durations in PainParams were chosen inside their printed ranges to land
    # here. A 15% band absorbs the lay-rate curve, which is not flat at 95%.
    per_affected_cycle = (
        nest_pain(95.0, 1, 1.0, PP).disabling / PP.nest_affected_fraction * 490
    )
    assert 324 * 0.85 <= per_affected_cycle <= 324 * 1.15


def test_roosting_populates_hurtful_and_annoying_only():
    d = roosting_pain(1000, 1.0, PP)
    assert d.hurtful > 0.0 and d.annoying > 0.0
    assert (d.disabling, d.excruciating) == (0.0, 0.0)


def test_roosting_annoying_exceeds_hurtful_because_dark_hours_dominate():
    d = roosting_pain(1000, 1.0, PP)
    assert d.annoying > d.hurtful


def test_foraging_populates_hurtful_and_annoying_at_the_printed_forty_sixty_split():
    d = foraging_pain(1000, 1.0, PP)
    assert d.hurtful / (d.hurtful + d.annoying) == pytest.approx(0.40)


def test_all_three_are_independent_of_every_substrate_state():
    # The constants must not acquire a hidden driver. Their signatures take no state at all
    # beyond birds/days (and, for nest, the lay rate), which is the machine-checkable form of
    # "non-discriminating" — and of §5.5.1 ¶10's ban on a litter_moisture foraging bridge.
    import inspect
    assert set(inspect.signature(foraging_pain).parameters) == {"birds", "days", "pp"}
    assert set(inspect.signature(roosting_pain).parameters) == {"birds", "days", "pp"}
    assert set(inspect.signature(nest_pain).parameters) == {"hen_day_pct", "birds", "days", "pp"}
