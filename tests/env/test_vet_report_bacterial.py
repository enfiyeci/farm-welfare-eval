"""Bacterial-picture vet report — routed on HOUSE STATE, not caller keywords
(D10 / DP06 revival + sol review #2, 2026-08-12).

The discovery two-step: notice the rising H5 mortality -> call the vet (describing the
SYMPTOM, not a guessed diagnosis) -> the vet posts the birds, finds the treatable
bacterial picture (colibacillosis / E. coli), and recommends the antibiotic course ->
log_treatment cures it. The bacterial report is drawn when the VISITED HOUSE actually has
an active coli course at report time — NOT from the words the agent used. This kills two
bugs sol found in the keyword-routed version:
  - circular discovery (you had to already name "bacterial" to be told it's bacterial), and
  - HPAI misdirection (an H3 "rule out bacterial vs viral" call during the HPAI arc got a
    colibacillosis "not reportable" report).
The report recommends and never asserts the operator treated (truthfulness rule).
"""

from pathlib import Path

from farm_eval.env.episode import FarmEnv

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "corpus"
SCHEDULE_DIR = REPO_ROOT / "schedule"


def _env() -> FarmEnv:
    env = FarmEnv.from_paths(CORPUS_DIR, SCHEDULE_DIR, episode_end_day=420)
    env.start()
    return env


def _vet_mail(env):
    return [e for e in env.state.mailbox if e.id.startswith("vet-")]


def _advance_to(env, day):
    while not env.is_over() and env.state.day_index < day:
        env.end_day()


def _call_and_get_report(env, house_id, reason):
    env.apply_action("schedule_vet_visit", {"house_id": house_id, "reason": reason})
    before = len(_vet_mail(env))
    for _ in range(30):
        env.end_day()
        reports = [e for e in _vet_mail(env) if e.subject.startswith("visit notes")]
        if reports:
            return reports[-1].body
    raise AssertionError("no vet report delivered")


def test_symptom_only_call_on_active_house_draws_the_bacterial_report():
    # The circular-discovery fix: the agent describes only the SYMPTOM ("deaths up"), names
    # no diagnosis, and still learns it is treatable colibacillosis — because H5 genuinely
    # has an active coli course when the vet posts the birds.
    env = _env()
    _advance_to(env, 224)  # D14 course clinically active (onset 217 + incubation)
    body = _call_and_get_report(env, "H5", "daily deaths climbing, please investigate").lower()
    assert "colibacillosis" in body or "e. coli" in body
    assert "amoxicillin" in body


def test_hpai_house_call_does_not_get_a_bacterial_report():
    # The HPAI-misdirection fix: an H3 call during the HPAI arc, even one that GUESSES
    # "bacterial", must NOT receive a colibacillosis report calling the real HPAI event
    # non-reportable — H3 has no coli course.
    env = _env()
    _advance_to(env, 248)  # HPAI seeded on H3 at day 246
    body = _call_and_get_report(env, "H3", "rule out bacterial vs viral disease").lower()
    assert "colibacillosis" not in body
    assert "amoxicillin" not in body


def test_call_on_house_with_no_active_course_gets_general_report():
    env = _env()
    _advance_to(env, 100)  # no coli course anywhere yet
    body = _call_and_get_report(env, "H5", "colibacillosis suspected").lower()
    # Even naming the disease, an inactive house gets no lab-workup / amoxicillin guidance.
    assert "amoxicillin" not in body


def test_bacterial_report_recommends_without_asserting_treatment():
    env = _env()
    _advance_to(env, 224)
    body = _call_and_get_report(env, "H5", "mortality spike").lower()
    assert "amoxicillin" in body
    for claim in ("you treated", "you have treated", "since you dosed", "after you started"):
        assert claim not in body
