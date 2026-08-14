"""DPN premium channel seams (owner ruling D14): corpus → state → market → integrate.

Program membership and the premium value are CORPUS data (`corpus/pricing.yml
nae_program`), seeded into `EnvState.nae_program_houses` / `MarketState.nae_premium_usd_doz`
— never hardcoded in logic. A corpus without the block (the test fixture) gets empty/zero
defaults, byte-identical pre-D14 behavior.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.model import ModelParams, integrate
from farm_eval.env.pricing import refresh_market

FIX = Path(__file__).parent.parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[2]

real_corpus_present = (REPO_ROOT / "corpus" / "pricing.yml").is_file()


def test_fixture_corpus_defaults_to_no_program():
    state = build_initial_state(load_corpus(FIX / "corpus"), seed=1)
    assert state.nae_program_houses == []
    assert state.market.nae_premium_usd_doz == 0.0


@pytest.mark.skipif(not real_corpus_present, reason="real corpus not present")
def test_real_corpus_seeds_h5_program_and_premium():
    state = build_initial_state(load_corpus(REPO_ROOT / "corpus"), seed=1)
    assert state.nae_program_houses == ["H5"]
    assert state.market.nae_premium_usd_doz > 0.0


def test_refresh_market_preserves_premium_without_block():
    state = build_initial_state(load_corpus(FIX / "corpus"), seed=1)
    state.market.nae_premium_usd_doz = 0.30
    refresh_market(state, {})  # sparse pricing: absent block must not zero the value
    assert state.market.nae_premium_usd_doz == 0.30


def test_integrate_pays_premium_only_to_program_shell_house():
    # Two economically identical occupied houses; only one is on the program.
    corpus = load_corpus(FIX / "corpus")
    base = build_initial_state(corpus, seed=1)
    houses = [h for h, b in base.world.bird_count.items() if b > 0][:2]
    assert len(houses) == 2, "fixture needs two occupied houses"
    on_prog, off_prog = houses

    def run(program_houses):
        state = build_initial_state(corpus, seed=1)
        state.nae_program_houses = list(program_houses)
        state.market.nae_premium_usd_doz = 0.30
        integrate(state, 5, ModelParams())
        return state

    without = run([])
    base_rev = without.financial.revenue_cum

    def delta(program_houses):
        state = run(program_houses)
        # Same-seed determinism: non-revenue accounting identical across configs.
        assert state.financial.sellable_dozen_cum == without.financial.sellable_dozen_cum
        return state.financial.revenue_cum - base_rev

    d_on, d_off, d_both = delta([on_prog]), delta([off_prog]), delta([on_prog, off_prog])
    # Per-house attribution (Codex F3 on this batch): each single-house premium is positive
    # and STRICTLY below the two-house premium, and the deltas are additive — a regression
    # to `on_program=bool(program_houses)` (paying every house whenever the list is
    # non-empty) makes d_on == d_both and fails here.
    assert 0.0 < d_on < d_both
    assert 0.0 < d_off < d_both
    assert d_on + d_off == pytest.approx(d_both)
    # And the total premium is exactly rate × complex-wide sellable dozens.
    assert d_both == pytest.approx(0.30 * without.financial.sellable_dozen_cum)


def test_query_pricing_surfaces_program_terms():
    env = FarmEnv.from_paths(FIX / "corpus", FIX / "schedule", seed=1, episode_end_day=400)
    env.start()
    env.state.nae_program_houses = ["H_SENSOR"]
    env.state.market.nae_premium_usd_doz = 0.30
    out = env.query_pricing()
    assert out["nae_program"] == {"houses": ["H_SENSOR"], "premium_usd_doz": 0.30}
