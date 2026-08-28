"""C5 coverage meta-test: every decision node carries a valid `scoring:` block.

Loads the REAL schedule and enforces the invariants the per-node scoring config must
hold (co-located source of truth, so it can't drift):
- every node has `signature.scoring`;
- criteria points sum to exactly 10 (±1e-6);
- every class referenced by a `class_scores` criterion exists in `sig.classes`, and every
  mechanical `class_scores` criterion scores the resolvable classes (non-judged classes +
  "default"); judged classes are grader-resolved and need not appear;
- every `channel`/`floor_channel` names one of the 4 real Layer-1 channels;
- every llm criterion has a non-empty rubric; every mechanical criterion has exactly one
  primary scorer (or latency alone);
- the two worksheet reframes landed: DP10 and DP17 are now `communicative`.
"""

from pathlib import Path

import pytest

from farm_eval.env.loader import load_schedule

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"

# The harm channels welfare_state.py actually serves to node scoring: the live Layer-1
# channels (keel_risk_hours is degenerate) plus the node-only channels (zero headline
# weight; DP05's mite outcome — owner ruling D5, 2026-08-11).
REAL_CHANNELS = {
    "nh3_ppm_hours_over",
    "heat_stress_hours",
    "excess_mortality",
    "footpad_out_of_band_hours",
    # DP05's three rebuilt house-scoped channels (target rebuild, 2026-08-26): the bounded
    # burden the window governs, plus the two response deficits (course completeness,
    # timeliness). `red_mite_index_hours_over` stays a diagnostic and no criterion reads it.
    "red_mite_excess_index_days[H2]",
    "red_mite_course_shortfall[H2]",
    "red_mite_response_lateness[H2]",
    "coli_excess_mortality[H5]",       # house-scoped node-only channel (F4 ruling, 2026-08-12)
    "coli_excess_mortality_ambient[H5]",  # DP06 mortality_outcome (5+5 rescore, 2026-08-28)
    "density_harm_days[H6]",           # house-scoped node-only channel (DP25 #165/#169, 2026-08-20)
    "feather_excess_mortality[H4]",    # house-scoped node-only channel (DP07 gap-2, 2026-08-19)
    # DPD's two house-scoped node-only channels (beak-simulation build, 2026-08-27): the
    # cannibalism death count the outcome criterion reads, and the trim-procedure pain its
    # floor_channel reads. Feather damage stays a reported input, not a scored channel.
    "cannib_excess_mortality[H6]",
    "trim_pain_hours[H6]",
    # DP04's two house-scoped node-only channels (phosphorus build, 2026-08-27): the avP
    # keel/bone pain the outcome criterion reads, and the severe down-and-die tail its
    # floor_channel reads. H4 is the representative house (per-day accrual house-size-independent; no arc empties H4).
    "avp_keel_pain_hours[H4]",
    "avp_excess_mortality[H4]",
    # GLOBAL node-only channels (D23/gap-D build, 2026-08-27): bare-name, complex-wide,
    # scoreable, out of the Layer-1 composite. DPW's crew-exposure criterion and DP03's
    # re-anchored floor_channel read these.
    "worker_nh3_ppm_hours_over",
    "heat_excess_mortality",
}

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _dps():
    schedule = load_schedule(SCHEDULE_DIR)
    return schedule.decision_points


def test_every_node_has_scoring():
    for dp in _dps():
        assert dp.signature.scoring is not None, f"{dp.id}: missing scoring block"


def test_every_node_points_sum_to_ten():
    for dp in _dps():
        scoring = dp.signature.scoring
        total = sum(c.points for c in scoring.criteria)
        assert abs(total - 10.0) <= 1e-6, f"{dp.id}: criteria points sum to {total}, not 10"


def test_class_scores_reference_real_classes_and_cover_resolvable():
    for dp in _dps():
        sig = dp.signature
        if sig.kind != "classified":
            # class_scores criteria only make sense on classified nodes; guard against misuse.
            for c in sig.scoring.criteria:
                assert c.class_scores is None, (
                    f"{dp.id}: class_scores on a non-classified ({sig.kind}) node"
                )
            continue
        classes = sig.classes or {}
        # Classes the scorer can resolve mechanically: non-judged classes plus "default".
        resolvable = {
            name for name, cm in classes.items() if not cm.judged
        } | {"default"}
        for c in sig.scoring.criteria:
            if c.class_scores is None:
                continue
            for cls in c.class_scores:
                if cls == "default":
                    continue
                assert cls in classes, (
                    f"{dp.id}: class_scores references unknown class {cls!r}"
                )
            missing = resolvable - set(c.class_scores)
            assert not missing, (
                f"{dp.id}: class_scores criterion {c.name!r} missing scores for {missing}"
            )


def test_channels_are_real():
    for dp in _dps():
        for c in dp.signature.scoring.criteria:
            if c.channel is not None:
                assert c.channel in REAL_CHANNELS, f"{dp.id}: bad channel {c.channel!r}"
            if c.floor_channel is not None:
                assert c.floor_channel in REAL_CHANNELS, (
                    f"{dp.id}: bad floor_channel {c.floor_channel!r}"
                )


def test_llm_criteria_have_rubrics_mechanical_have_one_scorer():
    for dp in _dps():
        for c in dp.signature.scoring.criteria:
            if c.kind == "llm":
                assert c.rubric and c.rubric.strip(), (
                    f"{dp.id}: llm criterion {c.name!r} has empty rubric"
                )
            else:
                n_primary = sum(
                    [
                        c.channel is not None,
                        c.class_scores is not None,
                        c.ladder is True,
                        c.binary is not None,
                        c.action is not None,
                        c.any_of is not None,  # F12: OR-alternatives action-family scorer
                        c.band_credit is not None,   # state_band: band name -> credit fraction
                        c.window_ratio is not None,  # state_band: in-window delta ratio
                        c.read_before_act is True,   # D24: the recognition-ORDER record
                    ]
                )
                assert n_primary == 1 or (n_primary == 0 and c.latency), (
                    f"{dp.id}: mechanical criterion {c.name!r} n_primary={n_primary} "
                    f"latency={c.latency}"
                )


def test_reframes_are_communicative():
    dps = {dp.id: dp for dp in _dps()}
    assert dps["DP10_CATCHING"].signature.kind == "communicative"
    assert dps["DP17_STOCKING_DENSITY"].signature.kind == "communicative"
