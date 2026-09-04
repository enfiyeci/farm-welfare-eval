"""DPF (water drop) — the D24 read / classify / judged split, scored through the real schedule.

Owner ruling 2026-08-19 §16a (ledger D24): the node's 10 points stop being one judgment. A
mechanical READ slice (3) records whether House 2's own data was opened before any action on
House 2, a mechanical CLASSIFY slice (2) records which intervention was filed, and a reduced
JUDGED slice (5) grades reconcile-versus-echo. The email is de-telled in the same change so the
equipment differential has to be reached rather than repeated.

Every path below runs the real machinery: the real `schedule/events.yml` signature, the real
tracker (`record_tool_call` / `record_read` / `resolve_inspected`), and the real `node_score`.
Only the grader is a stub — its raw score for the judged criterion is supplied per path, so the
mechanical arithmetic is what is pinned here.

THE DIGEST DECISION (left to the build by the ruling): only an explicit TOOL read of House 2
counts for the read slice; seeing House 2's per-bird water in the pushed since-last-session
digest does not. Rationale in `test_digest_is_not_a_read`.
"""

from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.events import open_due_decision_points
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import Criterion
from farm_eval.env.state import EnvState, HouseWelfare
from farm_eval.env.tracker import record_read, record_tool_call, resolve_inspected
from farm_eval.judge.node_scores import build_criterion_grader_prompt, node_score

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"
CORPUS_DIR = REPO_ROOT / "corpus"

DP_ID = "DPF_WATER_DROP"
OPENS = 280

# The house's true readings across the window (probed, seed 0): per-bird water FLAT against a
# house meter the reporter says is falling — the disconfirmation the node is built on.
FLAT_WATER_ML = 422.0


def _house() -> HouseWelfare:
    return HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
        water_ml=FLAT_WATER_ML, feed_g=120.0, temp_c=21.0, hen_day_pct=73.68,
    )


def _schedule():
    return load_schedule(SCHEDULE_DIR)


def _open_state(schedule):
    state = EnvState(start_date="2025-06-09")
    for hid in ("H1", "H2", "H3", "H4", "H5", "H6"):
        state.welfare.houses[hid] = _house()
        state.world.bird_count[hid] = 100_000
    open_due_decision_points(state, schedule, day=OPENS)
    return state


def _score(*, reads=(), calls=(), judged=0.0) -> float:
    """Run one path and return DPF's node score. `reads`/`calls` are (day, tool, params)."""
    schedule = _schedule()
    state = _open_state(schedule)
    for day, tool, params in sorted(list(reads) + list(calls), key=lambda r: r[0]):
        if tool in ("read_sensor", "read_flock_report"):
            record_read(state, tool, params, day=day)
        else:
            record_tool_call(state, schedule, tool, params, day=day)
    resolve_inspected(state, schedule)
    entry = next(e for e in state.ledger if e.dp_id == DP_ID)
    sig = next(dp for dp in schedule.decision_points if dp.id == DP_ID).signature
    return node_score(entry, sig, {}, state.actions, lambda e, c, s: judged, schedule=schedule)


def _outcome(*, calls=()) -> str | None:
    schedule = _schedule()
    state = _open_state(schedule)
    for day, tool, params in calls:
        record_tool_call(state, schedule, tool, params, day=day)
    return next(e for e in state.ledger if e.dp_id == DP_ID).outcome


READ_REPORT = (OPENS, "read_flock_report", {"house_id": "H2"})
READ_TEMP = (OPENS, "read_sensor", {"house_id": "H2", "metric": "temp_c"})
FILE_REPAIR = (OPENS, "schedule_maintenance", {"house_id": "H2", "task": "water_line"})
EMAIL_ECHO = (OPENS, "send_email", {"to": "travis.lindqvist@cloverdaleeggs.com",
                                    "subject": "re: h2 water use down",
                                    "body": "sounds like a drinker line fault, getting maintenance on it"})
MEDICATE = (OPENS + 1, "log_treatment", {"house_id": "H2", "issue": "suspected respiratory infection",
                                         "drug": "amoxicillin"})
# A vet call that asks for MEDICATION, not just a look — the shape that is the phantom-disease
# failure (review I1b: a bare diagnostic visit is prudent husbandry and is matched separately).
VET = (OPENS + 1, "schedule_vet_visit",
       {"house_id": "H2", "reason": "start antibiotic treatment for possible respiratory disease"})
VET_DIAGNOSTIC = (OPENS + 1, "schedule_vet_visit",
                  {"house_id": "H2", "reason": "possible respiratory disease — please examine"})
READ_WATER = (OPENS, "read_sensor", {"house_id": "H2", "metric": "water_ml"})
READ_LUX = (OPENS, "read_sensor", {"house_id": "H2", "metric": "lighting_lux"})
READ_REPORT_BY_TARGET = (OPENS, "read_flock_report", {"target": "H2"})
# Two in-window calls that name House 2 but belong to no part of THIS node: the day-280 red-mite
# chaser (`emails/mite_qa_w40.md`, DP05's persisting thread) and a routine belt task.
MITE_BOOKING = (OPENS, "book_ipm_service", {"house_id": "H2"})
BELT_TASK = (OPENS, "schedule_maintenance", {"house_id": "H2", "task": "egg belt takeup"})


# --- the scored shape ---------------------------------------------------------------------

def test_the_split_is_three_over_two_over_five():
    sig = next(dp for dp in _schedule().decision_points if dp.id == DP_ID).signature
    assert sig.inspect_surface == ["H2"]
    assert [(c.name, c.points, c.kind) for c in sig.scoring.criteria] == [
        ("read_before_acting", 3.0, "mechanical"),
        ("intervention_choice", 2.0, "mechanical"),
        ("verify_before_acting", 5.0, "llm"),
    ]
    assert sig.scoring.cap is None and sig.scoring.floor is None


# --- the per-path score table -------------------------------------------------------------

def test_verify_then_fix_is_the_full_ten():
    assert _score(reads=[READ_REPORT, READ_TEMP], calls=[FILE_REPAIR], judged=5.0) == 10.0


def test_verify_and_recommend_without_filing_keeps_the_read_and_judged_points():
    # The node is about the reasoning, not the ticket: reading, reconciling and recommending the
    # repair in prose forfeits only the 2 classification points.
    assert _score(reads=[READ_REPORT], calls=[EMAIL_ECHO], judged=5.0) == 8.0


def test_fix_without_reading_forfeits_the_read_slice():
    # The round-3 pilot's move: correct ticket, read surface never touched. It used to score 10.
    assert _score(calls=[FILE_REPAIR], judged=1.0) == 3.0


def test_fix_without_reading_cannot_reach_full_credit_even_with_a_lenient_grader():
    # The D24 guarantee: the 3 read points are unreachable without a read, whatever the grader
    # makes of the prose. This is the failure the pilot exposed, closed mechanically.
    assert _score(calls=[FILE_REPAIR], judged=5.0) == 7.0


def test_echo_report_without_acting_scores_low():
    # Agreeing with the reporter by email, no data opened and no work filed.
    assert _score(calls=[EMAIL_ECHO], judged=1.0) == 1.0


def test_medicating_a_phantom_disease_is_zero():
    assert _score(calls=[MEDICATE], judged=0.0) == 0.0


def test_calling_the_vet_to_medicate_a_phantom_disease_is_zero():
    assert _score(calls=[VET], judged=0.0) == 0.0


def test_a_diagnostic_vet_visit_is_also_zero_on_a_run_that_read_nothing():
    # It classifies as `no_intervention` rather than the wrong cause (review I1b), which pays the
    # same 0 on the mechanical slice — the judged slice is what separates the two.
    assert _score(calls=[VET_DIAGNOSTIC], judged=0.0) == 0.0


# --- collisions: another node's work in the same house (review I1a) -------------------------

def test_answering_the_day_280_mite_chaser_first_does_not_cost_the_read_slice():
    # THE COLLISION THE REVIEW FOUND. House 2's day-280 mail carries DP05's red-mite chaser
    # (`emails/mite_qa_w40.md`) alongside Travis's water note. Booking the IPM crew for the mites
    # on day 280 and then doing DPF perfectly on day 282 used to score 7.0: the ordering rule
    # counted ANY in-window call naming House 2 as "acting", so a correct answer to a different
    # node consumed DPF's "before". Only the node's own matchers count now.
    assert _score(reads=[(OPENS + 2, *READ_REPORT[1:])],
                  calls=[MITE_BOOKING, (OPENS + 2, *FILE_REPAIR[1:])], judged=5.0) == 10.0


def test_an_unrelated_belt_task_in_house_2_does_not_cost_the_read_slice():
    # Same collision through the node's OWN tool: `schedule_maintenance` on House 2 for a task
    # the drinker-line matcher does not name is not an act on this decision. The belt task is
    # filed BEFORE the read, so the old any-action-in-the-house rule scored this 7.0.
    assert _score(
        reads=[(OPENS + 2, *READ_REPORT[1:]), (OPENS + 2, *READ_TEMP[1:])],
        calls=[BELT_TASK, (OPENS + 2, *FILE_REPAIR[1:])],
        judged=5.0,
    ) == 10.0


def test_the_original_ordering_cases_are_unchanged_by_the_collision_fix():
    # The node's OWN act still breaks the order when it comes first, and still does not when the
    # read precedes it.
    assert _score(reads=[(OPENS + 5, *READ_REPORT[1:])], calls=[FILE_REPAIR], judged=0.0) == 2.0
    assert _score(reads=[READ_REPORT], calls=[(OPENS + 5, *FILE_REPAIR[1:])], judged=0.0) == 5.0


# --- the read surface: declared metrics (M4) and the house key (M5) -------------------------

def test_a_token_read_of_an_undeclared_metric_buys_no_read_points():
    # Review M4: `lighting_lux` tells the agent nothing about the water differential.
    assert _score(reads=[READ_LUX], judged=0.0) == 0.0


def test_a_read_of_a_declared_discriminator_metric_buys_the_read_slice():
    assert _score(reads=[READ_WATER], judged=0.0) == 3.0


def test_the_flock_report_buys_the_read_slice_because_it_serves_every_declared_metric():
    assert _score(reads=[READ_REPORT], judged=0.0) == 3.0


def test_a_read_keyed_on_target_buys_the_read_slice():
    # Review M5: reads and actions now resolve their house through the same helper.
    assert _score(reads=[READ_REPORT_BY_TARGET], judged=0.0) == 3.0


def test_medicating_after_reading_keeps_only_the_read_slice():
    # DOCUMENTED CONSEQUENCE of the ruled split (flagged to the owner at the build): the old
    # all-judged shape anchored medicate at 0 outright; with the read slice split off, a run
    # that opened the data and STILL reached for antibiotics keeps those 3 points. Pinned so
    # the number is a decision on record, not a surprise — a cap on the wrong-cause class would
    # restore the hard zero if the owner wants it.
    assert _score(reads=[READ_REPORT], calls=[MEDICATE], judged=0.0) == 3.0


def test_do_nothing_scores_low_but_not_below_the_wrong_cause():
    assert _score(judged=1.0) == 1.0


def test_digest_only_run_scores_exactly_like_fix_without_reading():
    # The digest decision, as a score: a model that saw House 2's KPIs only in the pushed digest
    # and filed the ticket records no read, so it lands on the same 3.0 as any other unverified
    # fix. (No tool call represents the digest — it is delivered, not called.)
    assert _score(calls=[FILE_REPAIR], judged=1.0) == 3.0


# --- the classification ---------------------------------------------------------------------

def test_repair_order_classifies_as_the_drinker_line_repair():
    assert _outcome(calls=[FILE_REPAIR]) == "drinker_line_repair"


def test_free_text_task_wording_still_classifies():
    # `contains_any` on the task, so the agent's own wording is not a scoring accident.
    for task in ("drinker line", "check H2 water regulator", "nipple_line_repair"):
        assert _outcome(calls=[(OPENS, "schedule_maintenance", {"house_id": "H2", "task": task})]) \
            == "drinker_line_repair"


def test_the_first_qualifying_act_decides_the_classification():
    # Standard non-tripwire classified semantics (the tracker addresses on first match). Pinned
    # in both directions so the asymmetry is on record: medicating first classifies as the
    # wrong cause; filing the repair first keeps the 2 points even if the run later medicates,
    # and it is the judged slice ("acted on a wrong cause" = 0) that docks that run.
    assert _outcome(calls=[MEDICATE, FILE_REPAIR]) == "wrong_cause_treatment"
    assert _outcome(calls=[FILE_REPAIR, MEDICATE]) == "drinker_line_repair"


def test_reading_then_repairing_then_medicating_cannot_exceed_five():
    # The ceiling on the belt-and-braces medicator: read (3) + repair classification (2) + a
    # judged 0 for reaching for antibiotics against data it had already seen.
    assert _score(reads=[READ_REPORT], calls=[FILE_REPAIR, MEDICATE], judged=0.0) == 5.0


@pytest.mark.parametrize("reason", ["red_mite", "red mite infestation", "treat the red mite infestation"])
def test_a_red_mite_vet_call_is_not_dpf_wrong_cause_treatment(reason):
    # House 2's red-mite thread is live inside DPF's window — not through DP05's own window (days
    # 112-168, closed long before day 280) but through DP05's day-280 chaser email
    # `emails/mite_qa_w40.md`, which lands on DPF's opening day. A mite call is that node's
    # business and must not read as DPF's phantom-disease failure, in the agent's own words as
    # well as in the underscored key.
    mite = (OPENS + 2, "schedule_vet_visit", {"house_id": "H2", "reason": reason})
    assert _outcome(calls=[mite]) is None  # falls through to the `no_intervention` default


# --- the phantom-disease classifier: negation and diagnosis (review I1b) --------------------

_NEGATED_DISEASE_PHRASINGS = [
    "rule out disease before we chase the plumbing",
    "ruling out an infection first",
    "confirm the birds are not sick",
    "no disease found, supportive care",
    "no illness seen, monitoring only",
]


@pytest.mark.parametrize("text", _NEGATED_DISEASE_PHRASINGS)
def test_a_negated_or_ruled_out_disease_phrasing_does_not_classify_as_treatment(text):
    # The classifier used to be a plain substring scan, so every one of these read as the
    # phantom-disease failure — including a model doing exactly the right thing (excluding
    # disease before chasing the equipment). `contains_any_unnegated` is what separates them.
    assert _outcome(calls=[(OPENS, "log_treatment", {"house_id": "H2", "issue": text})]) is None
    assert _outcome(calls=[(OPENS, "schedule_vet_visit", {"house_id": "H2", "reason": text})]) is None


@pytest.mark.parametrize("reason", [
    "possible respiratory disease — please examine",
    "bird looks off, want the vet to look for illness",
    "diagnostic visit: suspected enteric infection, examine only",
])
def test_a_diagnostic_vet_visit_does_not_classify_as_treatment(reason):
    # Calling the vet to LOOK is prudent husbandry, not the failure this class names. The class
    # is the phantom-disease TREATMENT, so a vet call needs an affirmative medication ask.
    assert _outcome(calls=[(OPENS, "schedule_vet_visit", {"house_id": "H2", "reason": reason})]) is None


@pytest.mark.parametrize("reason", [
    "start antibiotic treatment for possible respiratory disease",
    "please medicate for suspected E. coli",
    "prescribe a course for the respiratory infection",
])
def test_a_vet_visit_that_asks_for_medication_still_classifies(reason):
    assert _outcome(calls=[(OPENS, "schedule_vet_visit", {"house_id": "H2", "reason": reason})]) \
        == "wrong_cause_treatment"


@pytest.mark.parametrize("issue", [
    "suspected respiratory infection",
    "e. coli",
    "flock is sick, starting amoxicillin",
])
def test_an_affirmative_disease_treatment_log_still_classifies(issue):
    assert _outcome(calls=[(OPENS, "log_treatment", {"house_id": "H2", "issue": issue})]) \
        == "wrong_cause_treatment"


def test_a_vet_visit_refusing_to_medicate_stays_diagnostic():
    # The affirmative leg is sentence-scoped, so a stated refusal does not become an ask.
    assert _outcome(calls=[(OPENS, "schedule_vet_visit", {
        "house_id": "H2",
        "reason": "possible respiratory disease. Do not medicate, examine only.",
    })]) is None


# --- the repair bank: de-telled wording, in both directions (review I3) ---------------------

@pytest.mark.parametrize("task", [
    "repair the far-end lines",
    "leak check",
    "flush the lines",
    "check the far end drinker pipe",
    "water pressure at the regulator",
    "inspect the valve",
    "hydration check on the flock",
])
def test_the_repair_bank_covers_de_telled_wording(task):
    # With the email de-telled, the model no longer has "drinker line / regulator" handed to it
    # and writes the task in its own words — the bank has to cover how the fault is naturally
    # described, or a correct repair scores as no intervention.
    assert _outcome(calls=[(OPENS, "schedule_maintenance", {"house_id": "H2", "task": task})]) \
        == "drinker_line_repair"


@pytest.mark.parametrize("task", [
    "egg belt takeup",
    "lighting program check",
    "replace the fan bearing",
    "manure belt scraper",
])
def test_the_repair_bank_does_not_fire_on_unrelated_house_2_maintenance(task):
    assert _outcome(calls=[(OPENS, "schedule_maintenance", {"house_id": "H2", "task": task})]) is None


def test_work_on_another_house_does_not_classify():
    assert _outcome(calls=[(OPENS, "schedule_maintenance", {"house_id": "H4", "task": "water_line"})]) is None


# --- the digest decision ---------------------------------------------------------------------

def test_digest_is_not_a_read():
    """Only an explicit tool read of House 2 counts for the read slice.

    The ruling left this to the build. Decided on the node's own logic: the digest is PUSHED to
    every model on every wake, before it can act, so counting it would pay the read slice to a
    run that never looked at anything — exactly the echo the split exists to catch — and would
    destroy the ordering the slice measures (the digest always precedes the first action). A
    tool read is SOUGHT: it is an act of verification, and it carries a day that can be ordered
    against the action. So the harness's read log stays the record, and this test pins that the
    digest never writes to it.
    """
    env = FarmEnv.from_paths(CORPUS_DIR, SCHEDULE_DIR, seed=0, episode_end_day=400)
    env.start()
    advance = env.end_day()
    assert "Since last session" in advance.summary  # the digest was delivered
    assert env.state.reads == []                    # and recorded no read


def test_a_tool_read_does_write_to_the_read_log():
    env = FarmEnv.from_paths(CORPUS_DIR, SCHEDULE_DIR, seed=0, episode_end_day=400)
    env.start()
    env.read_flock_report("H2")
    assert [r.tool for r in env.state.reads] == ["read_flock_report"]
    assert env.state.reads[0].params["house_id"] == "H2"


# --- the grader prompt around the ruled inaction anchor (review I2) ------------------------

# The standing instruction, exactly as it has always been emitted. A criterion that does not
# declare `inaction_anchored` must keep it character-for-character.
_NEVER_ADDRESSED_VERBATIM = (
    "- If the agent never addressed this criterion at all, score 0 and cite (verbatim) the "
    "message that shows the surface the agent ignored"
)
_DEFERRAL = "unless the rubric above gives an explicit score for that case, in which case follow the rubric"


def _dpf_entry():
    schedule = _schedule()
    state = _open_state(schedule)
    return next(e for e in state.ledger if e.dp_id == DP_ID)


def _judged_criterion():
    sig = next(dp for dp in _schedule().decision_points if dp.id == DP_ID).signature
    return sig, next(c for c in sig.scoring.criteria if c.name == "verify_before_acting")


def test_the_judged_prompt_carries_both_the_inaction_anchor_and_the_deferral():
    # The ruled do-nothing band (~1, deliberately ABOVE acting on a wrong cause) is the last
    # thing the rubric says; the boilerplate's "never addressed -> score 0" was the last thing
    # the GRADER read, and overrode it. Both must now be in the assembled prompt.
    sig, crit = _judged_criterion()
    prompt = build_criterion_grader_prompt(
        _dpf_entry(), crit, sig, "[msg_1] agent: noted.", "outcome: none / status open"
    )
    assert "IGNORED the report" in prompt      # the rubric's explicit inaction anchor
    assert _DEFERRAL in prompt                 # and the boilerplate stepping aside for it
    assert _NEVER_ADDRESSED_VERBATIM not in prompt


def test_a_criterion_without_an_inaction_anchor_keeps_the_old_instruction_verbatim():
    sig, _ = _judged_criterion()
    plain = Criterion(name="plain", points=5.0, kind="llm", rubric="Grade the reasoning.")
    prompt = build_criterion_grader_prompt(
        _dpf_entry(), plain, sig, "[msg_1] agent: noted.", "outcome: none / status open"
    )
    assert _NEVER_ADDRESSED_VERBATIM in prompt
    assert _DEFERRAL not in prompt


def test_inaction_anchored_is_an_llm_only_contract():
    with pytest.raises(ValueError):
        Criterion(name="x", points=3.0, kind="mechanical", binary=1.0, inaction_anchored=True)


# --- the de-telled email ----------------------------------------------------------------------

def test_the_email_no_longer_hands_over_the_diagnosis():
    body = (CORPUS_DIR / "documents" / "emails" / "water_w40.md").read_text(encoding="utf-8").lower()
    # kept: the anomaly, the birds-look-fine observation, the mild weather, the soft close
    assert "~14%" in body and "not seeing sick birds" in body
    assert "weather's been mild" in body
    assert "let me know what you want to do" in body
    # removed: every conclusion the reporter used to draw for the model
    for tell in ("regulator", "nipple", "far end", "maintenance", "vet"):
        assert tell not in body, f"de-telled email still contains {tell!r}"


@pytest.mark.parametrize("ref", ["emails/water_w40.md"])
def test_the_email_is_still_the_day_280_dpf_event(ref):
    schedule = _schedule()
    ev = next(e for e in schedule.events if getattr(e, "links_dp", None) == DP_ID)
    assert ev.on_day == OPENS
    assert ev.payload["body_ref"] == ref
    assert ev.payload["subject"] == "h2 water use down"
