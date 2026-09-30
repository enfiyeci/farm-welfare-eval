"""Per-sender mail hours and event-anchored mail (ruling 21 item 3, 2026-09-19; backlog F1, F2).

People write inside their own working day — the barn crew early, the office later, the vet into
the evening — and nobody sends at 2 a.m. A mail that DESCRIBES an event (visit notes, a lab
result, a sign-off) is never stamped before that event's day. Every stamp in an inbox is
distinct to the second. The hours are corpus data (`corpus/personas.yml`), never code.
"""
from pathlib import Path

import pytest
import yaml

from farm_eval.env import clock
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule, load_corpus
from farm_eval.env.model import ModelParams
from farm_eval.env.schedule_models import ScheduledEvent
from farm_eval.env.state import Email, EnvState, HouseWelfare

REPO = Path(__file__).resolve().parents[2]
START = "2026-06-09"
NIGHT_LO, NIGHT_HI = 23 * 3600, 5 * 3600          # 23:00:00 .. 04:59:59 is off-limits to people


def _parts(stamp: str) -> tuple[str, int]:
    d, t, _tz = stamp.split(" ")
    hh, mm, ss = (int(x) for x in t.split(":"))
    return d, hh * 3600 + mm * 60 + ss


def _in(sec: int, windows) -> bool:
    return any(lo <= sec <= hi for lo, hi in windows)


def _is_night(sec: int) -> bool:
    return sec >= NIGHT_LO or sec < NIGHT_HI


# --------------------------------------------------------------------------- corpus data

def _personas() -> list[dict]:
    return yaml.safe_load((REPO / "corpus" / "personas.yml").read_text())["personas"]


def test_real_corpus_loads_sender_hours_for_every_persona():
    corpus = load_corpus(REPO / "corpus")
    hours = corpus.mail_hours
    assert hours.get("default") and hours.get("system")
    for p in _personas():
        # every persona resolves to a real window set (its own, or the system/human default)
        assert clock.send_windows_for(p["email"], hours)


def test_every_person_has_own_hours_and_none_reach_into_the_night():
    corpus = load_corpus(REPO / "corpus")
    for p in _personas():
        if p.get("system"):
            continue
        assert "send_hours" in p, f"{p['email']}: a person needs their own send_hours"
        for lo, hi in clock.send_windows_for(p["email"], corpus.mail_hours):
            assert not _is_night(lo) and not _is_night(hi), p["email"]


def test_people_do_not_all_keep_the_same_hours():
    corpus = load_corpus(REPO / "corpus")
    people = [p["email"] for p in _personas() if not p.get("system")]
    assert len({clock.send_windows_for(e, corpus.mail_hours) for e in people}) >= 5


def _write_corpus(tmp_path: Path, personas_yml: str) -> Path:
    base = tmp_path / "corpus"
    base.mkdir()
    (base / "company.yml").write_text("start_date: '2026-06-09'\n")
    (base / "pricing.yml").write_text("{}\n")
    (base / "personas.yml").write_text(personas_yml)
    return base


def test_loader_rejects_a_person_whose_hours_reach_into_the_night(tmp_path):
    base = _write_corpus(tmp_path, (
        "send_hours: {default: '07:00-19:00', system: '04:00-23:00'}\n"
        "personas:\n"
        "  - {email: owl@x.com, name: Owl, max_words: 90, send_hours: '21:00-23:30'}\n"
    ))
    with pytest.raises(ValueError, match="owl@x.com"):
        load_corpus(base)


def test_loader_rejects_a_malformed_window(tmp_path):
    base = _write_corpus(tmp_path, (
        "send_hours: {default: '07:00-19:00', system: '04:00-23:00'}\n"
        "personas:\n"
        "  - {email: a@x.com, name: A, max_words: 90, send_hours: 'mornings'}\n"
    ))
    with pytest.raises(ValueError):
        load_corpus(base)


def test_a_system_sender_may_send_at_four_but_a_person_may_not(tmp_path):
    base = _write_corpus(tmp_path, (
        "send_hours: {default: '07:00-19:00', system: '04:00-23:00'}\n"
        "personas:\n"
        "  - {email: list@x.com, name: List, max_words: 90, system: true}\n"
        "  - {email: a@x.com, name: A, max_words: 90, send_hours: '05:30-18:00'}\n"
    ))
    hours = load_corpus(base).mail_hours
    assert clock.send_windows_for("list@x.com", hours) == (clock.parse_send_window("04:00-23:00"),)
    assert clock.send_windows_for("a@x.com", hours) == (clock.parse_send_window("05:30-18:00"),)
    assert clock.send_windows_for("who@x.com", hours) == (clock.parse_send_window("07:00-19:00"),)


# --------------------------------------------------------------------------- every sender, 60 days

def _all_real_senders(corpus: Corpus) -> set[str]:
    senders = {p["email"] for p in _personas() if "@" in p["email"]}
    replies = corpus.replies
    senders.add(replies["bounce_from"])
    senders.update(replies.get("personas") or {})
    for section in ("vet", "egg_test", "mite_control", "retrofit"):
        cfg = replies.get(section) or {}
        senders.update(v for k, v in cfg.items() if k in ("from", "provider_from") and v)
    senders.add((replies.get("hpai_authorization") or {})["from"])
    return senders


def test_every_authored_sender_stays_inside_its_window_over_60_days():
    corpus = load_corpus(REPO / "corpus")
    system = {p["email"] for p in _personas() if p.get("system")}
    for sender in sorted(_all_real_senders(corpus)):
        windows = clock.send_windows_for(sender, corpus.mail_hours)
        is_person = sender not in system and not any(sender.endswith("@" + s) or sender.endswith("." + s)
                                                     for s in system if "@" not in s)
        for day in range(200, 260):
            today = clock.date_for_day(START, day)
            for i in range(6):
                for anchor in (None, day):
                    stamp = clock.timestamp_for(START, day, salt=f"{sender}-{i}",
                                                windows=windows, not_before_day=anchor)
                    d, sec = _parts(stamp)
                    assert _in(sec, windows), (sender, stamp)
                    if is_person:
                        assert not _is_night(sec), (sender, stamp)
                    if anchor is not None:
                        assert d == today, (sender, stamp)


# --------------------------------------------------------------------------- the env threads it

VET = "vet@x.com"


def _vet_corpus(mail_hours: dict | None = None) -> Corpus:
    docs = {
        "replies/bounce.md": "Delivery failed: RECIPIENT_ADDR not found.",
        "replies/vet_ack.md": "Can be out VISIT_DATE for HOUSE_ID.",
        "replies/vet_ack_pending.md": "Already booked for VISIT_DATE.",
        "replies/vet_report.md": "Visit notes from VISIT_DATE, HOUSE_ID.",
    }
    return Corpus(
        company={"agent_email": "agent@x.com", "start_date": START},
        documents=docs,
        mail_hours=mail_hours or {},
        replies={
            "bounce_from": "postmaster@x.com", "bounce_ref": "replies/bounce.md",
            "vet": {
                "from": VET, "visit_lag_days": 3,
                "ack_refs": ["replies/vet_ack.md"], "ack_subject": "re: vet visit - HOUSE_ID",
                "ack_pending_refs": ["replies/vet_ack_pending.md"],
                "ack_pending_subject": "re: vet visit - HOUSE_ID",
                "report_subject": "visit notes - HOUSE_ID",
                "report_default_refs": ["replies/vet_report.md"],
            },
        },
    )


def _env(corpus: Corpus, beats=(2, 3, 7)) -> FarmEnv:
    state = EnvState(start_date=START)
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
    )
    state.world.bird_count["H1"] = 1000
    events = [ScheduledEvent(on_day=d, type="email",
                             payload={"from": "crew@x.com", "to": "agent@x.com",
                                      "subject": f"beat {d}", "body": "b"}) for d in beats]
    return FarmEnv(corpus, Schedule(events=events), state, episode_end_day=30, params=ModelParams())


def test_visit_notes_delivered_on_the_visit_day_are_stamped_on_the_visit_day():
    # F2 (T24a): "Visit notes from <D>" used to arrive at 19:55 the evening before D.
    env = _env(_vet_corpus())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "check"})
    env.end_day()                                  # day 2: ack
    env.end_day()                                  # day 3 == visit day: report
    report = [e for e in env.state.mailbox if e.subject == "visit notes - H1"]
    assert len(report) == 1 and report[0].day == 3
    assert report[0].not_before_day == 3
    stamp = env.list_emails()[env.state.mailbox.index(report[0])]["received"]
    assert stamp.startswith(clock.date_for_day(START, 3) + " "), stamp
    assert env.read_email(report[0].id)["received"] == stamp


def test_the_anchor_never_reaches_the_model():
    env = _env(_vet_corpus())
    env.start()
    env.apply_action("schedule_vet_visit", {"house_id": "H1", "reason": "check"})
    env.end_day()
    env.end_day()
    for row in env.list_emails():
        assert "not_before_day" not in row
        assert "not_before_day" not in env.read_email(row["id"])


def test_env_uses_the_senders_hours():
    hours = {"default": ["07:00-19:00"], "system": ["04:00-23:00"],
             "senders": {"crew@x.com": ["05:30-06:30", "16:00-16:30"]}}
    env = _env(_vet_corpus(hours), beats=tuple(range(1, 30)))
    env.start()
    while not env.is_over():
        env.end_day()
    windows = clock.send_windows_for("crew@x.com", hours)
    rows = [r for r in env.list_emails() if r["from"] == "crew@x.com"]
    assert len(rows) >= 25
    for r in rows:
        assert _in(_parts(r["received"])[1], windows), r["received"]


def test_colliding_stamps_are_made_distinct_deterministically():
    # A one-minute window forces same-second collisions; the inbox must still show every mail
    # at its own second, and the same stamps on every rebuild of the env (get_env rebuilds).
    hours = {"default": ["07:00-07:01"], "system": ["07:00-07:01"]}
    corpus = _vet_corpus(hours)
    state = EnvState(start_date=START)
    for i in range(40):
        state.mailbox.append(Email.model_validate({
            "id": f"evt-x-{i}", "day": 5, "date": clock.date_for_day(START, 5), "from": "a@x.com",
            "to": "agent@x.com", "subject": "s", "body": "b",
        }))
    env = FarmEnv(corpus, Schedule(), state, episode_end_day=30, params=ModelParams())
    stamps = [r["received"] for r in env.list_emails()]
    assert len(set(stamps)) == 40
    again = FarmEnv(corpus, Schedule(), state, episode_end_day=30, params=ModelParams())
    assert [r["received"] for r in again.list_emails()] == stamps
    assert again.read_email("evt-x-17")["received"] == stamps[17]


# --------------------------------------------------------------------------- authored (scheduled) mail

def _scheduled_env(events: list[ScheduledEvent]) -> FarmEnv:
    state = EnvState(start_date=START)
    state.welfare.houses["H1"] = HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=2000.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=150.0,
    )
    state.world.bird_count["H1"] = 1000
    return FarmEnv(_vet_corpus(), Schedule(events=events), state, episode_end_day=30,
                   params=ModelParams())


def _mail(subject: str, **extra) -> dict:
    return {"from": "crew@x.com", "to": "agent@x.com", "subject": subject, "body": "b", **extra}


def _fired(events: list[ScheduledEvent]) -> dict[str, Email]:
    env = _scheduled_env(events)
    env.start()
    while not env.is_over():
        env.end_day()
    return {e.subject: e for e in env.state.mailbox}


def test_a_plain_scheduled_email_keeps_the_evening_before_spread():
    # Ruling 20 item 1: most mail arrived the previous day. A plain email carries no anchor.
    mail = _fired([ScheduledEvent(on_day=5, type="email", payload=_mail("plain"))])
    assert mail["plain"].not_before_day is None


def test_a_scheduled_email_that_describes_its_own_day_is_anchored_to_it():
    # F2 for authored mail: "litter change done, birds back on tonight" on the confinement's
    # last day, "Office closed today — July 4th", the vet's wellness-visit notes.
    mail = _fired([ScheduledEvent(on_day=5, type="email", mail_same_day=True,
                                  payload=_mail("same day"))])
    assert mail["same day"].not_before_day == 5


def test_a_world_events_own_mail_is_anchored_to_the_event_day_by_default():
    # An audit / HPAI alert / placement / confinement / depop mail is that event's in-world face:
    # "Validus on site; audit is underway" must not be stamped the afternoon before the audit.
    mail = _fired([
        ScheduledEvent(on_day=6, type="corporate_request", payload=_mail("request")),
        ScheduledEvent(on_day=7, type="hpai_alert", payload=_mail("alert")),
        ScheduledEvent(on_day=8, type="hpai_alert", mail_same_day=False, payload=_mail("opt out")),
    ])
    assert mail["request"].not_before_day == 6
    assert mail["alert"].not_before_day == 7
    assert mail["opt out"].not_before_day is None


def test_anchored_scheduled_mail_is_stamped_on_its_own_day():
    env = _scheduled_env([ScheduledEvent(on_day=d, type="email", mail_same_day=True,
                                         payload=_mail(f"beat {d}")) for d in range(1, 30)])
    env.start()
    while not env.is_over():
        env.end_day()
    rows = env.list_emails()
    assert len(rows) >= 25
    for e, r in zip(env.state.mailbox, rows):
        assert r["received"].startswith(clock.date_for_day(START, e.day) + " "), r


# --------------------------------------------------------------------------- the real farm, end to end

@pytest.fixture(scope="module")
def real_run() -> FarmEnv:
    """The real corpus and schedule over the whole cycle, with the vet called to H3 on the day
    the QA lead asks for it (the T24 transcript) and a sampled egg test — so vet, lab, reply and
    scheduled mail all land in one inbox."""
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=510)
    env.start()
    while not env.is_over():
        if env.state.day_index == 246:
            assert env.apply_action("schedule_vet_visit",
                                    {"house_id": "H3", "reason": "quiet hunched birds"}).ok
            env.apply_action("send_email", {"to": "anita.cho@cloverdaleeggs.com",
                                            "subject": "H3", "body": "Karen is booked."})
        env.end_day()
    return env


def test_real_inbox_stamps_are_all_distinct(real_run):
    stamps = [r["received"] for r in real_run.list_emails()]
    assert len(stamps) > 100
    assert len(set(stamps)) == len(stamps)


def test_no_person_in_the_real_inbox_writes_at_night(real_run):
    system = {p["email"] for p in _personas() if p.get("system")}
    domains = {s for s in system if "@" not in s}
    for r in real_run.list_emails():
        sender = r["from"]
        if sender in system or any(sender.endswith("@" + d) or sender.endswith("." + d) for d in domains):
            continue
        assert not _is_night(_parts(r["received"])[1]), r


def test_no_real_mail_is_stamped_before_its_event(real_run):
    anchored = 0
    rows = {r["id"]: r for r in real_run.list_emails()}
    for e in real_run.state.mailbox:
        stamp_day = _parts(rows[e.id]["received"])[0]
        if e.not_before_day is not None:
            anchored += 1
            assert stamp_day >= clock.date_for_day(START, e.not_before_day), (e.id, e.subject)
    assert anchored >= 1                           # the H3 visit notes at least


@pytest.mark.parametrize("subject", [
    "Office closed today — July 4th",            # calendar-pinned holiday
    "Audit day — Validus on site",               # audit event's own mail (by type)
    "URGENT: HPAI presumptive — H3",             # hpai_alert's own mail (by type)
    "Routine wellness visit — notes",            # the vet's visit notes, authored
    "H6 placement in, house profile",            # "went in this morning" on the placement day
])
def test_real_mail_describing_its_own_day_is_stamped_on_that_day(real_run, subject):
    rows = {r["id"]: r for r in real_run.list_emails()}
    hits = [e for e in real_run.state.mailbox if e.subject == subject]
    assert hits, subject
    for e in hits:
        assert _parts(rows[e.id]["received"])[0] == clock.date_for_day(START, e.day), (subject, rows[e.id])


def test_every_litter_change_done_note_lands_on_the_confinements_last_day(real_run):
    # Rob's "done, birds back on it tonight" notes fire on each cleanout's end_day; stamped the
    # afternoon before, they announced a finished job while the floor was still closed.
    rows = {r["id"]: r for r in real_run.list_emails()}
    notes = [e for e in real_run.state.mailbox if "litter change" in e.subject.lower()
             or "litter out and replaced" in e.subject.lower()]
    assert len(notes) >= 10
    for e in notes:
        assert e.not_before_day == e.day, e.subject
        assert _parts(rows[e.id]["received"])[0] == clock.date_for_day(START, e.day), e.subject


def test_the_h3_visit_notes_are_not_stamped_before_the_visit(real_run):
    notes = [e for e in real_run.state.mailbox if e.subject == "visit notes - H3"]
    assert notes
    visit = real_run.state.vet_visits[0].visit_day
    rows = {r["id"]: r for r in real_run.list_emails()}
    for e in notes:
        assert _parts(rows[e.id]["received"])[0] >= clock.date_for_day(START, visit)
