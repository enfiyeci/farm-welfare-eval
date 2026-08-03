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

from farm_eval.env.loader import load_corpus, params_for
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


def test_a_production_constructed_env_has_a_live_density_reference():
    """The whole point: an env built the way a real run builds it is NOT inert."""
    env = make_env()
    assert env.params.density_ref_sq_in == 144.0
    assert env.params.litter_area_frac == 0.41


def test_farm_env_fills_inert_params_but_keeps_an_explicit_one():
    """FarmEnv fills gaps only -- a deliberate unit-test override must survive."""
    env = make_env(litter_area_frac=0.25)
    assert env.params.litter_area_frac == 0.25      # caller's explicit value kept
    assert env.params.density_ref_sq_in == 144.0    # the inert one still filled from corpus
