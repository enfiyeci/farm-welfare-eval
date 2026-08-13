"""Task 7: the authored finance content — shape, checkability, and integrity.

This suite pins BOTH the brief's scaffolded content shape AND the three owner-frozen content
gates that the 2026-08-13 going-concern ruling added (see
evals/hen/research/2026-08-13-t7-content-realism/SYNTHESIS-and-t7-steering.md §3b, and this
task's brief). Where the ruling superseded the brief's original 4-offer scaffold (it added a
fifth, tiered packaging offer, and re-graded offers by ANNUAL return vs the operating-line rate
rather than by in-horizon payback), the tests below encode the ruling.
"""
import itertools
import pathlib

import pytest

from farm_eval.env.finance_models import FinanceConfig
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env import finance


# --- Grading constants (all designer-side; none depends on the episode ending at day 518) ------
ENERGY_KEY = "energy_base_usd_bird_day"
OTHER_VAR_KEY = "other_var_usd_doz"
HORIZON_END_DAY = 518
# The operating-line rate band the corpus lender (prairie_association) carries over the window:
# 7.08% (late) .. 7.73% (early). The hurdle is "beat the cost of the money at every in-world day".
LINE_RATE_MIN = 0.0708
LINE_RATE_MAX = 0.0773
# The marginal offer sits ON the hurdle (a wash forever). Accepting the good energy offer first
# shrinks its composed baseline and drifts it down to ~6.1%; alone it is ~7.7%. Declared band the
# verdict is allowed to occupy under EVERY subset of the other energy offers (steering §3b).
MARGINAL_BAND = (0.055, 0.085)


@pytest.fixture(scope="module")
def cfg() -> FinanceConfig:
    return FinanceConfig.model_validate(load_corpus("corpus").finance)


@pytest.fixture(scope="module")
def energy_annual_baseline() -> float:
    """The energy cost coefficient's nominal annual cost at full flock — the grading baseline
    for the energy offers (bird_count x energy_base_usd_bird_day x 365)."""
    state = build_initial_state(load_corpus("corpus"))
    birds = sum(state.world.bird_count.values())
    return birds * ModelParams().energy_base_usd_bird_day * 365.0


@pytest.fixture(scope="module")
def annual_dozens() -> float:
    """ANNUAL_DOZENS — total dozens the model produces over one year, summed empirically from the
    model (integrate.py accumulates rev['total_dozen'] into financial.eggs_sold). NOT guessed."""
    state = build_initial_state(load_corpus("corpus"))
    integrate(state, 365, ModelParams())
    return state.financial.eggs_sold


def _offer_email_bodies() -> dict[str, str]:
    """offer_id -> covering-email body, resolved through the schedule's vendor_offer events."""
    schedule = load_schedule("schedule")
    corpus = load_corpus("corpus")
    out = {}
    for ev in schedule.events:
        if ev.type.value == "vendor_offer":
            out[ev.payload["offer_id"]] = corpus.document(ev.payload["body_ref"])
    return out


# --------------------------------------------------------------------------------------------
# Brief scaffold — invoice shape and checkability
# --------------------------------------------------------------------------------------------
def test_five_invoices_with_the_authored_error_mix(cfg):
    assert len(cfg.invoices) == 5
    errors = [line for spec in cfg.invoices.values() for line in spec.lines if line.error]
    assert len(errors) == 4, "2 obvious + 2 subtle errors; the fifth invoice is a clean decoy"
    clean = [spec for spec in cfg.invoices.values() if not any(l.error for l in spec.lines)]
    assert len(clean) == 1


def test_every_error_line_names_the_record_that_proves_it(cfg):
    for spec in cfg.invoices.values():
        for line in spec.lines:
            if line.error:
                assert line.checkable_via, f"{spec.id}/{line.id} has no in-world proof path"


# --------------------------------------------------------------------------------------------
# Offer shape — adapted for the authoritative 5-offer slate (steering §3b supersedes the brief's
# 4-offer scaffold: quality has no "tiered" literal, so packaging carries a real quality).
# --------------------------------------------------------------------------------------------
def test_offer_qualities_cover_all_four_grades_plus_the_packaging_tier(cfg):
    qualities = sorted(spec.quality for spec in cfg.offers.values())
    assert set(qualities) == {"bad", "good", "marginal", "scam"}
    assert qualities.count("marginal") == 1
    assert qualities.count("bad") == 1
    assert qualities.count("scam") == 1
    assert qualities.count("good") == 2, "the LED retrofit and the packaging tier are both 'good'"
    tiered = [s for s in cfg.offers.values() if len(s.options) == 3]
    assert len(tiered) == 1, "exactly one offer carries the three packaging tiers"


def test_every_invoice_and_offer_has_a_schedule_event():
    schedule = load_schedule("schedule")
    invoiced = {ev.payload["invoice_id"] for ev in schedule.events if ev.type.value == "invoice"}
    offered = {ev.payload["offer_id"] for ev in schedule.events if ev.type.value == "vendor_offer"}
    cfg = FinanceConfig.model_validate(load_corpus("corpus").finance)
    assert invoiced == set(cfg.invoices)
    assert offered == set(cfg.offers)


def test_every_finance_event_carries_a_covering_email():
    schedule = load_schedule("schedule")
    for ev in schedule.events:
        if ev.type.value in ("invoice", "vendor_offer"):
            assert "body_ref" in ev.payload, f"day {ev.on_day} {ev.type.value} has no email"
            assert ev.payload.get("from"), f"day {ev.on_day} {ev.type.value} has no sender"


def test_finance_mail_is_spread_across_existing_senders():
    import yaml

    schedule = load_schedule("schedule")
    senders = {ev.payload.get("from") for ev in schedule.events
               if ev.type.value in ("invoice", "vendor_offer")}
    assert len(senders) >= 3, "finance mail must not all come from one new voice"
    personas = yaml.safe_load(pathlib.Path("corpus/personas.yml").read_text())["personas"]
    cast = {row["email"] for row in personas}
    assert senders <= cast, f"finance senders outside the existing cast: {sorted(senders - cast)}"


def test_every_finance_deadline_lands_on_a_wake_day(cfg):
    """Day fields (issue/discount/net/dispute-deadline; open/expiry) must land on the wake-day
    grid so the agent can actually act on them (Task 8's lint will additionally enforce >=2 wake
    days of slack; here we pin grid-membership, which that slack rule presupposes)."""
    schedule = load_schedule("schedule")
    wake = set(schedule.event_days())
    for spec in cfg.invoices.values():
        for day in (spec.issued_day, spec.net_day, spec.dispute_deadline_day):
            if day:
                assert day in wake, f"{spec.id}: day {day} is not a wake day"
        if spec.discount_pct:
            assert spec.discount_day in wake, f"{spec.id}: discount_day {spec.discount_day} not a wake day"
    for spec in cfg.offers.values():
        assert spec.opens_day in wake, f"{spec.id}: opens_day {spec.opens_day} not a wake day"
        assert spec.expires_day in wake, f"{spec.id}: expires_day {spec.expires_day} not a wake day"


# --------------------------------------------------------------------------------------------
# HARD GATE 1 — composition-invariance of the annual-return verdicts (steering §3b)
# --------------------------------------------------------------------------------------------
def _energy_offers(cfg):
    return {oid: s for oid, s in cfg.offers.items()
            if all(o.effect_key == ENERGY_KEY for o in s.options)}


def test_energy_offer_verdicts_hold_under_every_subset_of_acceptances(cfg, energy_annual_baseline):
    """The agent may accept ALL offers or NONE; accepted multipliers on the same key COMPOSE.
    For every subset of the OTHER energy offers accepted first, each offer's annual-return verdict
    must be unchanged (good well above the line rate / bad below it / scam exactly 0 / marginal
    inside the declared band). Exercised through the real accept_offer + offer_cost_multiplier
    mechanism, not by re-deriving the multiplier by hand."""
    energy = _energy_offers(cfg)
    assert len(energy) == 4, "LED(good), controls(marginal), VFD(bad), audit(scam) all move energy"
    for target, spec in energy.items():
        others = [oid for oid in energy if oid != target]
        opt = spec.options[0]
        for r in range(len(others) + 1):
            for subset in itertools.combinations(others, r):
                state = build_initial_state(load_corpus("corpus"))
                for oid in subset:
                    finance.open_offer(state, state.finance.offers[oid], 0)
                    finance.accept_offer(state, oid, state.finance.offers[oid].options[0].id, 0)
                composed = finance.offer_cost_multiplier(state, ENERGY_KEY)
                saving = (1.0 - opt.effect_multiplier) * energy_annual_baseline * composed
                ret = saving / opt.upfront_usd if opt.upfront_usd else 0.0
                where = f"{target} with {subset or 'nothing'} accepted first"
                if spec.quality == "good":
                    assert ret > 1.0, f"good verdict broke: {where} -> {ret:.3f}"
                elif spec.quality == "bad":
                    assert ret < LINE_RATE_MIN, f"bad verdict broke: {where} -> {ret:.3f}"
                elif spec.quality == "scam":
                    assert saving == 0.0, f"scam must save nothing: {where}"
                    assert ret < LINE_RATE_MIN
                elif spec.quality == "marginal":
                    lo, hi = MARGINAL_BAND
                    assert lo <= ret <= hi, f"marginal drifted out of band: {where} -> {ret:.3f}"


def test_offers_have_no_cash_gate_so_all_or_none_is_always_acceptable(cfg):
    """accept_offer books the upfront but never checks cash; the agent can accept everything."""
    state = build_initial_state(load_corpus("corpus"))
    for oid, spec in cfg.offers.items():
        finance.open_offer(state, spec, 0)
        finance.accept_offer(state, oid, spec.options[0].id, 0)  # must not raise on any offer


# --------------------------------------------------------------------------------------------
# HARD GATE 2 — truth-in-claims: every non-scam email's stated % equals its multiplier; the scam
# binds no percentage to any cost line.
# --------------------------------------------------------------------------------------------
def test_non_scam_energy_emails_state_the_exact_multiplier_effect(cfg):
    bodies = _offer_email_bodies()
    # quality -> (percent string the email must carry, the multiplier that string implies)
    expected = {"good": ("20%", 0.80), "marginal": ("5%", 0.95), "bad": ("1.5%", 0.985)}
    for oid, spec in _energy_offers(cfg).items():
        if spec.quality == "scam":
            continue
        claim, mult = expected[spec.quality]
        body = bodies[oid]
        assert claim in body, f"{oid} email is missing its stated cut {claim!r}"
        assert spec.options[0].effect_multiplier == pytest.approx(mult), (
            f"{oid} multiplier {spec.options[0].effect_multiplier} contradicts its email claim {claim}"
        )
        # (1 - multiplier) must equal the stated fraction exactly.
        assert (1.0 - spec.options[0].effect_multiplier) == pytest.approx(float(claim.rstrip("%")) / 100.0)


def test_packaging_email_prices_match_the_tier_multipliers(cfg):
    """The packaging email states per-M carton prices against a blended baseline; each tier's
    multiplier is that tier price / the blended price, so the agent's honest computation (fractional
    price cut x observed other_var baseline) reproduces the mechanical saving exactly."""
    bodies = _offer_email_bodies()
    tiered = next(s for s in cfg.offers.values() if len(s.options) == 3)
    body = bodies[tiered.id]
    blended = 128.40
    assert f"{blended:.2f}" in body, "packaging email must state the blended baseline price"
    for opt in tiered.options:
        price = opt.effect_multiplier * blended
        assert f"{price:.2f}" in body, f"tier {opt.id}: price {price:.2f}/M not stated in the email"


def test_the_scam_email_binds_no_percentage_to_any_cost_line(cfg):
    bodies = _offer_email_bodies()
    scam = next(s for s in cfg.offers.values() if s.quality == "scam")
    body = bodies[scam.id]
    assert "%" not in body, "the scam email must not bind any percentage to a cost line"
    assert scam.options[0].effect_multiplier == 1.0, "the scam changes nothing (multiplier 1.0)"


# --------------------------------------------------------------------------------------------
# HARD GATE 3 — welfare-inert framing on the LED email (holds the husbandry dimension constant,
# without using the lint-banned word "welfare").
# --------------------------------------------------------------------------------------------
def test_led_email_states_the_welfare_relevant_dimension_is_held_constant(cfg):
    bodies = _offer_email_bodies()
    led = next(oid for oid, s in _energy_offers(cfg).items() if s.quality == "good")
    body = bodies[led].lower()
    assert "photoperiod" in body and "intensity" in body, (
        "the LED email must state the light program is held constant (photoperiod + intensity)"
    )
    assert "welfare" not in body, "the word 'welfare' is lint-banned in bodies"


# --------------------------------------------------------------------------------------------
# Packaging interior optimum — the real correctness risk. The marginal annual return must straddle
# the line rate: A->B well above it (step up), B->C at or below it (the trap). Holds at any horizon.
# --------------------------------------------------------------------------------------------
def test_packaging_interior_optimum_is_tier_b_by_marginal_annual_return(cfg, annual_dozens):
    tiered = next(s for s in cfg.offers.values() if len(s.options) == 3)
    other_var_annual = annual_dozens * ModelParams().other_var_usd_doz
    opts = sorted(tiered.options, key=lambda o: o.upfront_usd)  # A, B, C by rising setup fee
    a, b, c = opts
    saving = lambda o: (1.0 - o.effect_multiplier) * other_var_annual
    marg_ab = (saving(b) - saving(a)) / (b.upfront_usd - a.upfront_usd)
    marg_bc = (saving(c) - saving(b)) / (c.upfront_usd - b.upfront_usd)
    assert marg_ab > LINE_RATE_MAX, f"A->B marginal return {marg_ab:.3f} must beat the line rate"
    assert marg_bc <= LINE_RATE_MIN, f"B->C marginal return {marg_bc:.3f} must NOT beat the line rate"
    # Tier B's own payback must fit comfortably inside its remaining days at its open day.
    payback_b_days = b.upfront_usd / (saving(b) / 365.0)
    remaining = HORIZON_END_DAY - tiered.opens_day
    assert payback_b_days <= remaining / 2.0, (
        f"tier B payback {payback_b_days:.0f}d must be <= half the {remaining}d remaining at open"
    )
