"""Bacterial-picture vet report (D10 / DP06 revival, 2026-08-12).

DP06's cure is the DP21-precedent two-step: notice the rising H5 mortality -> call the
vet -> the vet's visit notes name the treatable bacterial picture (colibacillosis /
E. coli) and recommend the antibiotic course -> log_treatment cures it. This test pins
the knowledge surface: a vet call naming a colibacillosis / E. coli / bacterial-peritonitis
concern draws the bacterial report (not the generic one), and it recommends without
ever asserting the operator treated (the truthfulness rule). The class keys are
bacterial-SPECIFIC (never generic "respiratory"/"mortality") so the H3 HPAI arc can
never be mislabeled as this treatable bacterial cause.
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


def _advance_to_report(env, reason):
    env.apply_action("schedule_vet_visit", {"house_id": "H5", "reason": reason})
    # Walk to the first report (visit lag + a couple wake-ups).
    reports = []
    for _ in range(30):
        env.end_day()
        reports = [e for e in _vet_mail(env) if e.subject.startswith("visit notes")]
        if reports:
            break
    assert reports, "no vet report delivered"
    return reports[0].body


# The general report echoes the reason into REASON_TEXT, so the CONDITION NAME alone
# can't distinguish the bacterial report — assert on body-distinctive content (the lab
# workup + amoxicillin recommendation), which the general body never carries.
def test_colibacillosis_reason_draws_the_bacterial_report():
    body = _advance_to_report(_env(), "colibacillosis").lower()
    assert "amoxicillin" in body and "lab" in body


def test_bacterial_peritonitis_reason_draws_the_bacterial_report():
    body = _advance_to_report(_env(), "bacterial peritonitis suspected").lower()
    assert "amoxicillin" in body


def test_bacterial_report_recommends_antibiotics_without_asserting_treatment():
    body = _advance_to_report(_env(), "e_coli picture").lower()
    # Names the treatable course...
    assert "amoxicillin" in body
    # ...but never claims the operator already treated (truthfulness rule).
    for claim in ("you treated", "you have treated", "since you dosed", "after you started"):
        assert claim not in body


def test_unrelated_reason_still_gets_general_report():
    # A vet call about something else must not be mislabeled bacterial (no amoxicillin
    # recommendation, no lab workup) — it falls to the generic report.
    body = _advance_to_report(_env(), "routine welfare check").lower()
    assert "amoxicillin" not in body
