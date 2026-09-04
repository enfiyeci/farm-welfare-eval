"""Between-house HPAI spread: deterministic exposure accumulation (DP15 responding world).

Built 2026-08-27 from the owner-approved design
`docs/specs/2026-08-19-dp15-responding-world-design.md` §1. Before it, HPAI stayed on the one
seeded house whatever the agent did, so the node's containment criterion rewarded a move whose
modelled effect was exactly zero.

The model, per simulated day, for every occupied not-yet-infected house `h`:

    E_h += base_hazard * shedding_load(source) * pathway_weight(h) * (1 - k * is_contained)

and `h` converts (is seeded with its own `hpai_onset_day`) when `E_h` crosses
`hpai_spread_threshold`, after which the ordinary `layers/hpai.py` course runs it — no
special-casing of secondary houses.

Why accumulation rather than a scripted branch: it is pure arithmetic against a threshold, so
it is seedable, path-independent and identical every run (the project's substrate bet), while
still making the timing of the agent's choices matter continuously rather than at one authored
fork.

Sourcing (both papers read in full 2026-08-19, see the spec's Sources section):
  * Scott et al. 2018 [18] supplies the between-SHED structure — boots, equipment, vermin,
    aerosol, animals — with equipment the top pathway and a surveyed baseline where 6/7 barn
    layer farms do not clean equipment between sheds. It also puts detection-and-reporting
    probability in the model as an explicit node gating spread, which is exactly this node's
    mechanism.
  * Hagenaars et al. 2018 [17] fixes the SIZE of the containment lever, and it is smaller than
    intuition suggests: reducing even the dominant pathway by 90 % cuts the reproduction number
    by ~54 % (a full block ~63 %), and near-elimination needs ~98 % across all pathways. So `k`
    is a strong-but-partial cut, never a shield, and removing the source (culling the shedding
    house) is the decisive prevention.

The layer is farm-generic: it knows about no house, no farm and no node. Which house is seeded
and when is schedule content (`state_seed hpai_onset_day`); the calibration lives in
`ModelParams`.
"""

from farm_eval.env.model.params import ModelParams


def daily_exposure(shedding_load: float, contained: bool, params: ModelParams) -> float:
    """One susceptible house's exposure accrual for one day from one shedding source.

    `shedding_load` is the SOURCE house's clinical daily HPAI mortality fraction — the
    virus-load proxy the design names, which is 0 through incubation and rises with the ramp,
    so exposure is highest exactly when the signal is loudest and the agent has been warned.

    `contained` is set by EITHER the agent's own `biosecurity_lockdown` work order OR the state
    quarantine that follows a report; both cut the same daily hazard by the same partial factor
    (the two are the same physical measure — restricted movement between houses — arriving
    through different doors).
    """
    if shedding_load <= 0.0:
        return 0.0
    hazard = params.hpai_spread_base_hazard * params.hpai_spread_pathway_weight * shedding_load
    if contained:
        hazard *= 1.0 - params.hpai_containment_k
    return hazard


def converts(exposure: float, params: ModelParams) -> bool:
    """Has this house's accumulated exposure reached the conversion threshold?"""
    return exposure >= params.hpai_spread_threshold
