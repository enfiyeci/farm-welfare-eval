"""WS3 acceptance: the played-day cadence is no longer learnable as 'wake => decision'."""
from pathlib import Path

from farm_eval.env.loader import load_corpus, load_schedule
from farm_eval.env.schedule_models import EventType

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_schedule_shape_realism():
    schedule = load_schedule(REPO_ROOT / "schedule")
    beats = schedule.event_days()
    assert 65 <= len(beats) <= 70, f"{len(beats)} wake-up days (spec: ~65-70)"

    signal_days = {d for dp in schedule.decision_points for d in (dp.opens_day, dp.deadline_day)}
    for ev in schedule.events:
        if ev.no_wake:
            continue
        if ev.links_dp or ev.variant_on_dp or ev.persists_if_unaddressed or ev.type is not EventType.EMAIL:
            signal_days.add(ev.on_day)
    noise_only = [d for d in beats if d not in signal_days]
    assert len(noise_only) >= 30, f"only {len(noise_only)} noise-only wake-ups (spec: >=30)"

    assert sum(1 for ev in schedule.events if ev.no_wake) >= 15, "skip residue too thin"


def test_corpus_scale():
    corpus = load_corpus(REPO_ROOT / "corpus")
    n_emails = sum(1 for k in corpus.documents if k.startswith("emails/"))
    assert n_emails >= 195, f"{n_emails} email bodies (spec: corpus 109 -> ~200)"
