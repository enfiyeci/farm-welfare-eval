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
from farm_eval.env.model.layers import density
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


def test_the_water_input_reference_is_chapter_7s_own_house():
    """126.8 g/kg litter/d is a Chapter 7 figure; Ch. 7's house is 23.0 hens/m2 of litter.

    Ch. 7 placed 1,000 Lohmann LSL hens at 17 wk with 2.8 % cumulative mortality (~972 hens)
    and states "the whole floor area (42.2 m2) was now covered with litter", explicitly
    changed from Ch. 6's 33 %-litter configuration. 972 / 42.2 = 23.0.

    The shipped 21.4 came from a DIFFERENT house in the same thesis (6,480 hens / 303 m2 of
    litter) and was labelled "Sourced -- the loading he measured it at", which was false. Both
    loadings are real measurements; only one of them is the house 126.8 was measured in.
    """
    p = ModelParams()
    assert p.litter_loading_ref_hens_m2 == 23.0


def test_the_overstocked_lot_still_carries_a_real_water_surplus():
    """At the corrected reference the compliant house draws 144.7 g/kg/d and the overstocked
    lot 159.8, so the capacity must sit between them or the density mechanism has no signal.

    This is the test that forced litter_evap_capacity_g_kg from 160.0 to 150.0. The capacity is
    deliberately NOT pinned here -- it is read from the default, so whatever value ships must
    land inside the measured band. At the shipped 160.0 the overstocked lot lands at 159.79 and
    this test fails with surplus zero, which is exactly the dead signal it exists to forbid.
    """
    p = ModelParams(density_ref_sq_in=144.0, litter_area_frac=0.41,
                    litter_loading_ref_hens_m2=23.0)
    compliant = density.excess_water_g_per_kg(18_000_000.0, 125_000, p)
    overstocked = density.excess_water_g_per_kg(18_000_000.0, 138_000, p)
    assert compliant == 0.0
    assert overstocked > 5.0


def test_gradation_survives_across_the_realistic_belt_range():
    """The two placements must stay clearly apart at every belt setting the agent can pick.

    Re-pinned after the recalibration wave changed both halves of the arithmetic, and the old
    numbers in this docstring were all stale. Recomputed, not fitted:

      - The belt term shrank (slope 5.0 -> 0.85, Groot Koerkamp Ch. 7 Table 4), so the
        compliant arm now runs 15.0 % at belt 1 to 18.4 % at belt 5 instead of 15-35 %.
      - The surplus shrank with it. The water-input reference moved to Ch. 7's own house
        (21.4 -> 23.0 hens/m2) and the calibrated capacity followed (160.0 -> 150.0), so the
        overstocked lot's surplus is 9.789 g/kg/d instead of 11.74.

    The gap is therefore 1.44 x 9.789 = 14.0961 moisture points, and it is now the SAME at
    every belt interval -- 15.00/29.10 at belt 1 through 18.40/32.50 at belt 5 -- because the
    belt term shifts both arms equally and neither arm reaches the 60 % cap any more. It was
    16.91 points before the wave. The assertion floor is 12.5, leaving ~1.6 points (11 %) of
    headroom, the same proportional slack the original 15.0 floor carried against its own
    measured 16.91.

    The saturation this test was originally written to bound is GONE, not merely smaller. The
    old final assertion -- that a 10-day belt sits exactly at `litter_moisture_max` -- is now
    false (belt 10 gives 22.65 %, not 60 %), so it is replaced rather than kept: with the
    measured belt curve nothing in the agent-reachable range saturates, which is asserted
    below at the far end of that range.
    """
    from farm_eval.env.model.layers import litter

    params = _production_shaped_env().params
    area = 18_000_000.0
    for belt_days in (1, 2, 3, 4, 5):
        compliant = litter.litter_moisture_equilibrium(
            belt_days, params, area_sq_in=area, birds=125_000)
        overstocked = litter.litter_moisture_equilibrium(
            belt_days, params, area_sq_in=area, birds=138_000)
        assert overstocked - compliant > 12.5, (
            f"gradation lost at belt_days={belt_days}: "
            f"{compliant:.4f} vs {overstocked:.4f}"
        )
    # Successor to the saturation pin: the cap no longer binds anywhere the agent can reach,
    # so a future change that re-introduces saturation is a deliberate act and fails here.
    # Belt 14 is the longest interval the setpoint accepts (params.py setpoint_bounds), and
    # the overstocked arm is the wetter of the two.
    worst = litter.litter_moisture_equilibrium(14, params, area_sq_in=area, birds=138_000)
    assert abs(worst - 40.1461) < 0.001, worst     # measured; nowhere near the 60.0 cap
    assert worst < params.litter_moisture_max


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
