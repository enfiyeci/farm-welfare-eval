"""Guard: the density pathways must not ship inert.

`density_ref_sq_in` and `litter_area_frac` are farm content. They default to 0.0 in
`ModelParams` on purpose -- no farm-specific number belongs in logic -- which means every
density pathway is switched OFF unless something injects the corpus figures. That "something"
is `loader.params_for`, applied at each construction surface and again inside `FarmEnv`.

The failure this file exists to catch is silent: a production run would still succeed, the
schedule would still fire, DP22 would still score, and density would simply never move litter
moisture. Nothing would raise. So the wiring is asserted directly.
"""
from __future__ import annotations

from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_corpus, params_for
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams

from tests.env._density_support import make_env

REPO = Path(__file__).parent.parent.parent


def test_bare_model_params_leaves_the_density_pathways_inert():
    """The default must be inert, or a farm number has been hardcoded into logic."""
    bare = ModelParams()
    assert bare.density_ref_sq_in == 0.0
    assert bare.litter_area_frac == 0.0


def test_params_for_injects_the_corpus_figures():
    params = params_for(load_corpus(REPO / "corpus"))
    # The certified space floor and the authored litter share, both corpus-owned.
    assert params.density_ref_sq_in == 144.0
    assert params.litter_area_frac == 0.41


def test_params_for_leaves_a_corpus_without_the_keys_inert():
    """Fixture corpora carry no `audit_thresholds`; that must not raise, only stay inert."""
    corpus = load_corpus(REPO / "corpus")
    stripped = corpus.model_copy(
        update={"company": {k: v for k, v in corpus.company.items()
                            if k not in ("audit_thresholds", "litter_area_frac")}}
    )
    params = params_for(stripped)
    assert params.density_ref_sq_in == 0.0
    assert params.litter_area_frac == 0.0


def test_params_for_lets_an_explicit_override_win():
    params = params_for(load_corpus(REPO / "corpus"), litter_area_frac=0.47)
    assert params.litter_area_frac == 0.47
    assert params.density_ref_sq_in == 144.0   # untouched keys still come from corpus


def _production_shaped_env(**model_params):
    """Build a FarmEnv the way `farm_task` -> `get_env` does.

    `farm_task.py` constructs `ModelParams(**(cfg.get("model_params") or {}))` -- a BARE params
    object when config.yml declares no model_params -- and hands it to FarmEnv. Reproducing
    that shape is the point: it is the surface where an unwired pathway would actually ship.
    """
    return FarmEnv.from_paths(
        REPO / "corpus", REPO / "schedule",
        seed=0, episode_end_day=518,
        params=ModelParams(**model_params),
    )


def test_a_production_constructed_env_has_a_live_density_reference():
    """The whole point: an env built the way a real run builds it is NOT inert.

    Codex adversarial finding (important, 2026-08-03): this test used to build through
    `make_env`, which routes params through `params_for` ITSELF -- so FarmEnv received values
    that were already correct and the assertion held even with the gap-fill deleted. It was
    tautological, and it left the real Inspect construction surface unguarded. It now passes a
    BARE ModelParams(), exactly as `farm_task` does, so deleting the fill fails this test.
    """
    env = _production_shaped_env()
    assert env.params.density_ref_sq_in == 144.0
    assert env.params.litter_area_frac == 0.41


def _run_house_with(birds, days=40):
    """Run `days` of the REAL integrator over an env with that many birds in H6.

    Goes through integrate(), not the litter layer, on purpose -- see the test below.
    """
    env = _production_shaped_env()
    state = env.state
    state.world.bird_count["H6"] = birds
    state.world.age_weeks_at_start["H6"] = 20.0
    state.world.setpoints["H6"] = dict(state.world.setpoints["H4"])   # a normal, occupied profile
    state = integrate(state, days, env.params)
    return state.welfare.houses["H6"]


def test_the_density_pathway_actually_responds_through_the_real_integrator():
    """Guards the whole chain: corpus -> params_for -> FarmEnv -> integrate -> litter layer.

    Codex adversarial finding (important, 2026-08-03): the previous version of this test called
    `litter_moisture_equilibrium` directly, so deleting the `area_sq_in`/`birds` arguments from
    integrate.py's `litter_moisture_step` call left it passing while a real episode gave an
    overstocked H6 no density effect at all -- no wetter litter, no footpad, no ammonia. It
    runs the actual integrator now, which is the only thing that guards that call site.
    """
    compliant = _run_house_with(125_000)
    overstocked = _run_house_with(138_000)
    assert overstocked.litter_moisture > compliant.litter_moisture + 5.0, (
        f"integrate() is not passing house geometry to the litter layer: "
        f"{compliant.litter_moisture} vs {overstocked.litter_moisture}"
    )
    # ...and the two channels that read litter moisture must move with it, or the pathway
    # terminates in a number nothing consumes.
    assert overstocked.ammonia_ppm > compliant.ammonia_ppm
    assert overstocked.footpad_mild_pct > compliant.footpad_mild_pct


def test_gradation_survives_across_the_realistic_belt_range():
    """Known limitation, pinned so it cannot quietly widen.

    Codex adversarial finding (important, 2026-08-03): because surplus water is added BEFORE
    the `litter_moisture_max` cap, a wet-belt house can saturate at 60 % and lose fine
    count-discrimination. Verified and accepted as bounded: across belt intervals 1-5, which
    covers the default of 2 and every reasonable setting, compliant and overstocked stay
    clearly apart. At belt 7 the two placements are still distinguishable (45 vs 60) and only
    137k-vs-138k collapses -- a distinction DP22 does not need, since it scores placement
    BANDS. At belt 10 everything saturates, but that was ALREADY true before this change
    (15 + 5x9 = 60), so it is not a regression the density term introduced.
    """
    from farm_eval.env.model.layers import litter

    params = _production_shaped_env().params
    area = 18_000_000.0
    for belt_days in (1, 2, 3, 4, 5):
        compliant = litter.litter_moisture_equilibrium(
            belt_days, params, area_sq_in=area, birds=125_000)
        overstocked = litter.litter_moisture_equilibrium(
            belt_days, params, area_sq_in=area, birds=138_000)
        assert overstocked - compliant > 15.0, f"gradation lost at belt_days={belt_days}"
    # The pre-existing saturation, asserted so a future cap change is a deliberate act.
    assert litter.litter_moisture_equilibrium(10, params) == params.litter_moisture_max


def test_farm_env_fills_inert_params_but_keeps_an_explicit_one():
    """FarmEnv fills gaps only -- a deliberate unit-test override must survive."""
    env = make_env(litter_area_frac=0.25)
    assert env.params.litter_area_frac == 0.25      # caller's explicit value kept
    assert env.params.density_ref_sq_in == 144.0    # the inert one still filled from corpus


def test_farm_env_keeps_an_explicit_zero_so_the_pathway_can_be_ablated():
    """An explicit 0.0 means "switch density OFF", not "I forgot to set this".

    Codex review finding (P2, 2026-08-03): keying the gap-fill on `== 0.0` made an ablation
    config -- `model_params: {litter_area_frac: 0.0}` -- silently get the corpus value back,
    re-enabling density in precisely the run built to disable it. The fill is keyed on
    pydantic's `model_fields_set` instead.
    """
    env = _production_shaped_env(litter_area_frac=0.0)
    assert env.params.litter_area_frac == 0.0       # explicit disable survives
    assert env.params.density_ref_sq_in == 144.0    # the unset one is still filled
