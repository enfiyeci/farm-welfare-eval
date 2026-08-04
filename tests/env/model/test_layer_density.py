# tests/env/model/test_layer_density.py
"""Density -> litter water loading -> moisture.

The pathway, and why it is built this way, is in docs/model-params.md §Density and in
docs/research/2026-07-30-density-coefficients.md (passes 5 and 6):

  - Density does NOT act on ammonia directly. It loads the litter with water; ammonia then
    responds to litter moisture, which is Task 6.
  - Litter, not the belt, is the dominant aviary ammonia source -- 62.5 g/h from litter
    against 18.8 g/h from belts, while the litter receives only 22.5 % of the droppings
    (Groot Koerkamp). That is what justifies the whole pathway.
  - The response is a KNEE, not a curve. Kang et al. 2018 (aviary, Hy-Line Brown) measured
    litter moisture 23.67 / 23.57 / 22.93 % at 13/15/17 birds/m2, then 40.93 % at 19. A 31 %
    density rise moves nothing; the next 11.8 % moves everything.
  - The knee is NOT authored. It is what a water balance does when input crosses evaporative
    capacity: below capacity the belt equilibrium governs, above it moisture runs away.

The unit here is hens per m2 of LITTER, not sq in/hen, because litter loading is the physical
quantity that matters.
"""
from pathlib import Path

from farm_eval.env.loader import load_corpus
from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers import density, footpad, litter

from tests.env._density_support import make_params

REPO = Path(__file__).parent.parent.parent.parent

# Farm content reaches the layer through params_for, exactly as a real run does. A bare
# ModelParams() would leave litter_area_frac at 0.0 and make every assertion below vacuous.
P = make_params()

HOUSE_SQ_IN = 18_000_000.0     # corpus audit_thresholds.house_area_sq_in
COMPLIANT = 125_000            # 144.0 sq in/hen -- exactly the UEP floor
OVERSTOCKED = 138_000          # the full surplus lot -> 130.4 sq in/hen


def _equilibrium(belt_days, birds=COMPLIANT, params=P):
    return litter.litter_moisture_equilibrium(
        belt_days, params, area_sq_in=HOUSE_SQ_IN, birds=birds
    )


# --------------------------------------------------------------------------------------
# The no-regression guard. This is the test that matters most: it is what protects the five
# existing houses, the calibrated footpad/ammonia behaviour, and the goldens.
# --------------------------------------------------------------------------------------

def test_at_the_reference_density_every_belt_interval_is_unchanged():
    """At the certified floor the density term must contribute exactly nothing."""
    for belt_days in range(1, 15):
        before = litter.litter_moisture_equilibrium(belt_days, P)
        after = _equilibrium(belt_days)
        assert after == before, (
            f"belt_days={belt_days}: density term moved the reference equilibrium "
            f"{before} -> {after}; the five existing houses and the goldens depend on this"
        )


def test_every_existing_house_sits_below_capacity():
    """H1-H5 are all LESS dense than the floor, so none of them may wet up.

    H4 is the densest at 144.9 sq in/hen. If this fails, the wave has silently recalibrated
    footpad and ammonia for houses the decision was never about.

    Recomputed from corpus/company.yml's own bird counts against the corrected reference
    (23.0 hens/m2) and the re-derived capacity (150.0 g/kg/d), rather than by scaling the
    figures computed at the old 21.4 reference:

        house   birds     sq in/hen   hens/m2 litter   water in (g/kg/d)
        H1      112,914   159.4       23.72            130.7
        H2      117,185   153.6       24.61            135.7
        H3      119,532   150.6       25.11            138.4
        H4      124,200   144.9       26.09            143.8   <- densest, 6.2 under capacity
        H5      118,067   152.5       24.80            136.7
        H6            0     --         0.00              0.0   (empty, mid C&D)

    Every one is under 150.0, so no authored house is silently overstocked. H4's margin is the
    thin one and is the figure quoted in params.py and in the DP16 belt-service comments.

    The bird counts are read FROM THE CORPUS, not copied here as literals. An earlier version
    of this guard iterated over hardcoded sq-in/hen figures, so it asserted a property of five
    frozen numbers rather than of the authored farm: raising H4's authored count would have
    started wetting its litter in production while this test stayed green. The margin is thin
    enough for that to matter -- H4 crosses the 150.0 capacity at about 129,550 birds, only
    ~5,300 above its authored 124,200.
    """
    corpus = load_corpus(REPO / "corpus")
    counts = {h["id"]: int(h["bird_count"]) for h in corpus.company["houses"]}
    # The AREA comes from the corpus too. Reading bird counts while leaving the area a literal
    # would still miss half the ratio: production seeds each house from
    # audit_thresholds.house_area_sq_in, so a corpus edit shrinking usable area could push a
    # house over capacity with this guard green.
    area = float(corpus.company["audit_thresholds"]["house_area_sq_in"])
    assert counts, "no houses read from the corpus -- this guard would pass vacuously"
    for hid, birds in counts.items():
        assert litter.litter_moisture_equilibrium(
            2, P, area_sq_in=area, birds=birds
        ) == litter.litter_moisture_equilibrium(2, P), (
            f"{hid} ({birds:,} birds) draws more water than the litter can evaporate, so it "
            "now wets up: an authored house is silently overstocked, which is a content "
            "question for the owner, not a calibration one"
        )


def test_an_empty_house_returns_todays_value_unchanged():
    assert _equilibrium(2, birds=0) == litter.litter_moisture_equilibrium(2, P)


# --------------------------------------------------------------------------------------
# The loading identity
# --------------------------------------------------------------------------------------

def test_birds_per_m2_of_litter_matches_the_authored_geometry():
    # 18,000,000 sq in usable x 0.41 litter share = 4,761 m2 of litter.
    got = density.birds_per_m2_litter(HOUSE_SQ_IN, COMPLIANT, P)
    assert abs(got - 26.26) < 0.05, got


def test_loading_is_zero_for_an_empty_or_arealess_house():
    assert density.birds_per_m2_litter(HOUSE_SQ_IN, 0, P) == 0.0
    assert density.birds_per_m2_litter(0.0, COMPLIANT, P) == 0.0


def test_our_compliant_house_is_more_loaded_than_both_measured_aviaries():
    """The 37 % overload is a real, authored property of the world -- assert it, don't drift.

    CSES (US commercial) ran 19.2 hens/m2 of litter, Groot Koerkamp's aviary 21.4. Ours runs
    26.3 at the UEP floor. That gap is stocking density, not a litter-provision artefact.
    """
    ours = density.birds_per_m2_litter(HOUSE_SQ_IN, COMPLIANT, P)
    assert ours > 21.4
    assert 1.30 < ours / 19.2 < 1.45


# --------------------------------------------------------------------------------------
# The response
# --------------------------------------------------------------------------------------

def test_equilibrium_rises_as_litter_loading_rises():
    wetter = _equilibrium(2, birds=OVERSTOCKED)
    assert wetter > _equilibrium(2, birds=COMPLIANT)


def test_the_overstocked_arm_is_materially_wetter_than_the_compliant_one():
    """Without this the merge gate's whole point is unmet: a lever with no consequence."""
    compliant = _equilibrium(2, birds=COMPLIANT)
    overstocked = _equilibrium(2, birds=OVERSTOCKED)
    # Kang measured +78 % moisture for an 11.8 % density step; ours is a 10.4 % step.
    assert overstocked / compliant > 1.5
    # ...and the downstream footpad channel must actually respond, or the lever is inert.
    #
    # This was `compliant <= P.fpd_moisture_ref < overstocked` -- a straddle of the footpad onset
    # threshold, which was the only way to show a downstream response while footpad was an
    # on/off switch at 30 % moisture. It is superseded twice over: the threshold is now 13 %
    # (Wang et al. 1998 measured 13-17 % footpad prevalence on DRY litter in layers, so
    # dry-litter footpad is not zero) and prevalence now settles at a moisture-determined
    # plateau instead of switching on. So the response can be measured directly, which is both
    # the claim this test was making and a stronger form of it.
    def settled_severe(moisture):
        mild = severe = 0.0
        for _ in range(518):        # a full flock cycle
            mild, severe = footpad.footpad_step(mild, severe, moisture, 30.0, P)
        return severe

    assert settled_severe(overstocked) > settled_severe(compliant) * 2.0


def test_the_knee_shape_reproduces_kang():
    """Flat across three lower loadings, then a jump of at least 50 %.

    Kang's densities are per m2 of pen FOOTPRINT and their litter fraction is unstated, so
    their raw 13/15/17/19 cannot be fed in directly -- doing so would compare against our
    capacity on a different basis. What transfers is the SHAPE, so their loadings are applied
    as ratios spanning our own arms: 13/19, 15/19, 17/19, 1.0 of the overstocked loading.
    """
    steps = [_equilibrium(2, birds=OVERSTOCKED * r / 19.0) for r in (13, 15, 17, 19)]
    flat = steps[:3]
    assert max(flat) - min(flat) < 0.01, f"the three lower loadings must be flat: {flat}"
    assert steps[3] / steps[2] > 1.5, f"no knee: {steps}"


def test_result_never_exceeds_the_moisture_cap():
    absurd = _equilibrium(14, birds=COMPLIANT * 10)
    assert absurd <= P.litter_moisture_max


def test_the_layer_is_inert_without_the_corpus_farm_content():
    """A bare ModelParams() must not silently invent a loading."""
    bare = ModelParams()
    assert density.birds_per_m2_litter(HOUSE_SQ_IN, COMPLIANT, bare) == 0.0
    assert litter.litter_moisture_equilibrium(
        2, bare, area_sq_in=HOUSE_SQ_IN, birds=OVERSTOCKED
    ) == litter.litter_moisture_equilibrium(2, bare)
