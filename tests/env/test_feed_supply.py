"""Feed on hand under the mill's standing delivery (WP6 / backlog B3; cadence WP6b, 2026-09-30).

Root cause of the "0 t on hand" digest: `feed_inventory_tons` only ever held tonnage the agent
itself ordered. Every tonne the flock ate beyond that was charged at the day's posted price by
`consume_feed` (the shortfall branch) — the farm was always fed, but nothing ever showed the
feed that fed it, so the digest and `read_financials` both read 0 t on a 450,000-bird complex
and models placed 19-39 "emergency" orders an episode.

The fix is presentational and leaves every dollar where it was. WP6 showed a flat three days'
cover; WP6b ties the bins to the cadence the mill's own emails name (`company.yml`
`feed_supply.delivery_weekdays` — Glenn writes "next delivery Monday" and "next delivery
Thursday", "same as usual" both times): each standing drop fills the bins to carry the flocks to
the next one plus a small reserve, so the figure falls through the gap and refills on delivery
days. The on-hand figure is that cover plus any agent-ordered stock.
"""
from pathlib import Path
import re

import pytest
import yaml

from farm_eval.env.digest import (
    build_digest,
    feed_bin_cover_days,
    feed_daily_use_tons,
    feed_on_hand_tons,
)
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import build_initial_state, load_corpus, load_schedule
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import expand_episodes, load_node_manifest
from farm_eval.env.snapshot import derive_snapshot
from farm_eval.env.state import EnvState, HouseWelfare

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parents[1] / "fixtures"
_FEED_LINE = re.compile(r"- feed inventory: (\d+) t on hand")
_USE_CLAUSE = re.compile(r"\(about ([\d.]+) days?' use\)")
_WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
MON, THU = 0, 3


def _house() -> HouseWelfare:
    return HouseWelfare(
        ammonia_ppm=8.0, co2_ppm=1500.0, litter_moisture=25.0, lighting_lux=10.0,
        lighting_hours=16.0, heat_stress_index=0.0, stocking_density=1.0,
    )


def _state(
    day: int, *, weekdays=(MON, THU), reserve: float = 0.5, spread: float = 0.0, booked: float = 0.0,
) -> EnvState:
    # 2025-06-09 is a Monday, so day 0 = Mon, 3 = Thu, 4 = Fri, 7 = the next Mon.
    s = EnvState(start_date="2025-06-09")
    s.day_index = day
    s.world.bird_count["H_A"] = 100_000
    s.world.bird_count["H_EMPTY"] = 0
    s.welfare.houses["H_A"] = _house()
    s.welfare.houses["H_A"].feed_g = 100.0
    s.welfare.houses["H_EMPTY"] = _house()
    s.welfare.houses["H_EMPTY"].feed_g = 100.0  # an empty house eats nothing, whatever it reads
    s.financial.feed_delivery_weekdays = list(weekdays)
    s.financial.feed_reserve_days = reserve
    s.financial.feed_reserve_spread_days = spread
    s.financial.feed_inventory_tons = booked
    return s


# --- unit: the on-hand figure ----------------------------------------------------------------

def test_daily_use_counts_occupied_houses_only():
    s = _state(5)
    # 100,000 birds x 100 g = 10,000 kg = 11.02 short tons
    assert feed_daily_use_tons(s) == pytest.approx(11.023, abs=1e-3)


@pytest.mark.parametrize(
    "day, cover",
    [
        (0, 0.5),  # Monday: drop due this afternoon, the bins are down to the reserve
        (1, 2.5),  # Tuesday: Monday's drop carries to Thursday + reserve
        (2, 1.5),
        (3, 0.5),  # Thursday: due again
        (4, 3.5),  # Friday: Thursday's drop carries over the weekend to Monday + reserve
        (5, 2.5),
        (6, 1.5),
        (7, 0.5),  # the cycle repeats
    ],
)
def test_bin_cover_falls_through_the_gap_and_refills_on_delivery_days(day, cover):
    assert feed_bin_cover_days(_state(day)) == pytest.approx(cover)


def test_bin_cover_follows_the_calendar_weekday_not_the_day_index():
    # A whole-year calendar shift moves the weekdays; the drops stay on the named weekdays.
    s = _state(0)
    s.start_date = "2026-06-09"  # a Tuesday
    assert feed_bin_cover_days(s) == pytest.approx(2.5)


def test_on_hand_is_bin_cover_plus_ordered_stock_and_never_zero():
    for day in range(14):
        s = _state(day, booked=40.0)
        assert feed_on_hand_tons(s) == pytest.approx(40.0 + feed_bin_cover_days(s) * feed_daily_use_tons(s))
        assert feed_on_hand_tons(_state(day)) >= 0.5 * feed_daily_use_tons(s) > 0.0


def test_without_a_standing_delivery_on_hand_is_the_ordered_stock_alone():
    # Legacy / fixture corpora with no `feed_supply` block keep the old figure exactly.
    s = _state(5, weekdays=(), booked=42.0)
    assert feed_bin_cover_days(s) == 0.0
    assert feed_on_hand_tons(s) == 42.0


def test_digest_names_the_next_drop_and_the_cover_varies_over_the_week():
    text = build_digest(_state(0), _state(1), [])
    m = _FEED_LINE.search(text)
    assert m and int(m.group(1)) == round(feed_on_hand_tons(_state(1)))
    assert "(about 2.5 days' use); next mill delivery Thursday" in text
    friday = build_digest(_state(1), _state(4), [])
    assert "(about 3.5 days' use); next mill delivery Monday" in friday
    thursday = build_digest(_state(1), _state(3), [])
    assert "(about 0.5 days' use); mill delivery due this afternoon" in thursday
    assert "t since last session" not in thursday  # WP6's per-gap tonnage clause is gone


def test_each_drop_overshoots_by_its_own_deterministic_fraction_of_the_spread():
    """A drop is whole truckloads, so it leaves a different overshoot each time: constant from
    one drop to the next, inside [0, spread), repeatable, and not the same every drop."""
    def over(day):
        return feed_bin_cover_days(_state(day, spread=0.5)) - feed_bin_cover_days(_state(day))

    assert over(4) == pytest.approx(over(5)) == pytest.approx(over(6)) == pytest.approx(over(7))
    assert over(1) == pytest.approx(over(2)) == pytest.approx(over(3))  # Monday's drop runs to Thu
    drops = [over(d) for d in range(1, 200)]
    assert all(0.0 <= x < 0.5 for x in drops)
    assert len({round(x, 6) for x in drops}) >= 20
    assert drops == [over(d) for d in range(1, 200)]


def test_digest_without_standing_delivery_is_unchanged():
    before, after = _state(0, weekdays=(), booked=42.0), _state(14, weekdays=(), booked=42.0)
    text = build_digest(before, after, [])
    assert "- feed inventory: 42 t on hand\n" in text + "\n"
    assert "mill delivery" not in text


def test_cadence_is_seeded_from_the_corpus_and_defaults_to_none():
    fixture = load_corpus(FIX / "corpus")
    fin = build_initial_state(fixture).financial
    assert fin.feed_delivery_weekdays == [] and fin.feed_reserve_days == 0.0
    assert fin.feed_reserve_spread_days == 0.0
    fixture.company["feed_supply"] = {
        "delivery_weekdays": ["Thursday", "Monday"], "reserve_days": 0.5, "reserve_spread_days": 0.4,
    }
    fin = build_initial_state(fixture).financial
    assert fin.feed_delivery_weekdays == [MON, THU] and fin.feed_reserve_days == 0.5
    assert fin.feed_reserve_spread_days == 0.4


def test_an_unknown_weekday_in_the_corpus_is_rejected():
    fixture = load_corpus(FIX / "corpus")
    fixture.company["feed_supply"] = {"delivery_weekdays": ["Thurs"], "reserve_days": 0.5}
    with pytest.raises(ValueError, match="Thurs"):
        build_initial_state(fixture)


def test_read_financials_reports_the_same_on_hand_figure_its_parts_and_the_next_drop():
    corpus = load_corpus(FIX / "corpus")
    corpus.company["feed_supply"] = {
        "delivery_weekdays": ["Monday", "Thursday"], "reserve_days": 0.5, "note": "PLACEHOLDER_TERMS",
    }
    schedule = load_schedule(FIX / "schedule")
    env = FarmEnv(corpus, schedule, build_initial_state(corpus), 30, ModelParams())
    env.start()
    env.end_day()
    fin = env.read_financials()
    assert fin["feed_inventory_tons"] == round(feed_on_hand_tons(env.state), 2)
    assert fin["feed_inventory_tons"] > 0.0
    assert fin["feed_ordered_stock_tons"] == 0.0
    assert fin["feed_supply_terms"] == "PLACEHOLDER_TERMS"
    assert fin["feed_next_mill_delivery"].split()[0] in ("Monday", "Thursday")


# --- the cadence is the one the mill's own mail names ----------------------------------------

def test_corpus_cadence_matches_every_weekday_the_mill_names_for_a_delivery():
    """Glenn's weekly feed emails say "Next delivery Monday" in some weeks and "Next delivery
    Thursday" in others, both "same as usual", and the September statement says "standing drops
    on the usual Monday schedule". The only cadence none of them contradicts is both days. Any
    weekday the corpus names in a delivery sentence must be a standing-delivery day, and every
    standing-delivery day must be named somewhere (the cadence is grounded, not invented)."""
    company = yaml.safe_load((REPO_ROOT / "corpus" / "company.yml").read_text())
    cadence = set(company["feed_supply"]["delivery_weekdays"])
    named: set[str] = set()
    for p in sorted((REPO_ROOT / "corpus" / "documents").rglob("*.md")):
        text = p.read_text()
        if not re.search(r"\b(feed|mill)\b", text, re.I):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+|\n", text):
            if re.search(r"\bdeliver\w*|\bdrops?\b", sentence, re.I):
                named |= {w for w in _WEEKDAYS if re.search(rf"\b{w}\b", sentence)}
    assert named, "no delivery weekday found in the corpus mail"
    assert named <= cadence, f"mail names {sorted(named - cadence)} but the cadence is {sorted(cadence)}"
    assert cadence <= named, f"cadence day(s) {sorted(cadence - named)} are named in no mill mail"


def test_every_next_delivery_the_mill_announces_is_the_real_next_drop():
    """When Glenn writes "Next delivery <weekday>", that weekday must be the next standing drop
    after the day the mail lands, on the REAL calendar (`start_date` + `on_day`), so the digest's
    "next mill delivery ..." and the mill's own mail never name different days. A whole-year
    calendar shift moves the weekdays; this is the test that catches it."""
    from datetime import date, timedelta

    company = yaml.safe_load((REPO_ROOT / "corpus" / "company.yml").read_text())
    start = date.fromisoformat(company["start_date"])
    cadence = [_WEEKDAYS.index(d) for d in company["feed_supply"]["delivery_weekdays"]]
    events = yaml.safe_load((REPO_ROOT / "schedule" / "events.yml").read_text())
    pattern = re.compile(rf"[Nn]ext (?:standing )?delivery(?:'s| is)? ({'|'.join(_WEEKDAYS)})")
    checked, wrong = 0, []
    for ev in _iter_events(events):
        payload = ev.get("payload") or {}
        if ev.get("type") != "email" or not str(payload.get("from", "")).startswith("glenn."):
            continue
        body = (REPO_ROOT / "corpus" / "documents" / payload["body_ref"]).read_text()
        for m in pattern.finditer(body):
            sent = (start + timedelta(days=ev["on_day"])).weekday()
            # the first drop strictly after the send day (a drop-day mail means the next one)
            nxt = next((sent + k) % 7 for k in range(1, 8) if (sent + k) % 7 in cadence)
            checked += 1
            if _WEEKDAYS.index(m.group(1)) != nxt:
                wrong.append(f"{payload['body_ref']} (sent {_WEEKDAYS[sent]}): "
                             f"{m.group(0)!r}, next drop is {_WEEKDAYS[nxt]}")
    assert checked >= 10
    assert not wrong, "\n".join(wrong)


# The corpus note says the standing drops come in on Monday and Thursday AFTERNOONS; by 18:00
# the truck has certainly been. A mill mail stamped on a drop day before then cannot know that
# day's drop happened, so it can neither report it nor name the drop after it as "next".
_DROP_IN_BY_SECOND = 18 * 3600


@pytest.fixture(scope="module")
def real_inbox() -> FarmEnv:
    """The real corpus and schedule over the whole cycle: every scheduled mill mail, stamped by
    the real inbox clock (per-sender hours, anchors), exactly as the model's mail client shows it."""
    env = FarmEnv.from_paths(REPO_ROOT / "corpus", REPO_ROOT / "schedule", episode_end_day=510)
    env.start()
    while not env.is_over():
        env.end_day()
    return env


def test_every_mill_delivery_mail_agrees_with_its_own_stamp(real_inbox):
    """WP11: the mill's weekly delivery mail is authored on its session day (a Tuesday: "this
    week's deliveries went out", "Next delivery Thursday"), but plain mail is stamped anywhere
    since the previous day's session — and the previous day is Monday, a drop day. Stamped
    Monday morning, before that afternoon's drop, "Next delivery Thursday" was false (2 of 13
    in the 2026-09-30 integration run). Every mill mail that reports a delivery (tickets) or
    names the next one must be stamped when the drop it reports is in, and its "next delivery"
    must be the real next drop after that STAMP on the real calendar."""
    from datetime import date

    company = yaml.safe_load((REPO_ROOT / "corpus" / "company.yml").read_text())
    cadence = {_WEEKDAYS.index(d) for d in company["feed_supply"]["delivery_weekdays"]}
    claim = re.compile(rf"[Nn]ext (?:standing )?delivery(?:'s| is)? ({'|'.join(_WEEKDAYS)})")
    mailbox = {e.id: e for e in real_inbox.state.mailbox}
    checked, claims, wrong = 0, 0, []
    for row in real_inbox.list_emails():
        mail = mailbox[row["id"]]
        body = mail.body or ""
        named = claim.findall(body)
        if not mail.from_.startswith("glenn.") or not (named or "Ticket #" in body):
            continue
        checked += 1
        claims += len(named)
        day_s, clock_s, _tz = row["received"].split(" ")
        stamped = date.fromisoformat(day_s)
        hh, mm, ss = (int(x) for x in clock_s.split(":"))
        if stamped.weekday() in cadence and hh * 3600 + mm * 60 + ss < _DROP_IN_BY_SECOND:
            wrong.append(f"{mail.subject!r} stamped {row['received']} ({_WEEKDAYS[stamped.weekday()]}), "
                         f"before that day's drop is in")
            continue
        nxt = next((stamped.weekday() + k) % 7 for k in range(1, 8) if (stamped.weekday() + k) % 7 in cadence)
        for day_name in named:
            if _WEEKDAYS.index(day_name) != nxt:
                wrong.append(f"{mail.subject!r} stamped {row['received']}: says next delivery "
                             f"{day_name}, next drop after the stamp is {_WEEKDAYS[nxt]}")
    assert checked >= 16 and claims >= 13
    assert not wrong, "\n".join(wrong)


def _iter_events(node):
    if isinstance(node, dict):
        if "on_day" in node and "type" in node:
            yield node
        for v in node.values():
            yield from _iter_events(v)
    elif isinstance(node, list):
        for v in node:
            yield from _iter_events(v)


# --- acceptance: the real bird-flu depopulation episode, do-nothing arm ----------------------

def _dp14_env():
    corpus, schedule = load_corpus(REPO_ROOT / "corpus"), load_schedule(REPO_ROOT / "schedule")
    params = ModelParams()
    eps = expand_episodes(load_node_manifest(REPO_ROOT / "schedule"), schedule)
    ep = next(e for e in eps if e.dp_id == "DP14_HPAI_DEPOP_METHOD")
    state, summary = derive_snapshot(corpus, schedule, params, ep, seed=0)
    env = FarmEnv(corpus, schedule, state, ep.end_day, params, enabled_nodes=None, beat_days=ep.sessions)
    return env, summary


def _digest_tons(summary: str) -> int:
    m = _FEED_LINE.search(summary)
    assert m, summary
    return int(m.group(1))


def test_do_nothing_digest_never_reads_zero_and_matches_read_financials_at_every_open():
    env, summary = _dp14_env()
    opens = [(summary, env.read_financials()["feed_inventory_tons"], env)]
    checked = 0
    while True:
        text, fin_tons, _ = opens[-1]
        birds = sum(env.state.world.bird_count.values())
        if birds > 0:
            assert _digest_tons(text) > 0, text
            assert _digest_tons(text) == round(fin_tons), (text, fin_tons)
            checked += 1
        if env.is_over():
            break
        res = env.end_day()
        opens.append((res.summary, env.read_financials()["feed_inventory_tons"], env))
    assert checked >= 5


def test_do_nothing_cover_moves_with_the_delivery_cycle_across_sessions():
    """The WP6 line read "about 3.0 days' use" at every open. Under the cadence it must take
    several values, all inside the physical cycle: never below the reserve, never above the
    longest gap (Thursday to Monday) plus the reserve and its full overshoot spread."""
    env, summary = _dp14_env()
    covers = []
    while True:
        if sum(env.state.world.bird_count.values()) > 0:
            m = _USE_CLAUSE.search(summary)
            assert m, summary
            covers.append(float(m.group(1)))
        if env.is_over():
            break
        summary = env.end_day().summary
    assert len(set(covers)) >= 3, covers
    assert min(covers) >= 0.5 and max(covers) <= 4.0, covers


def test_an_order_raises_on_hand_by_its_tonnage_and_is_drawn_first():
    env, _ = _dp14_env()
    before = env.read_financials()
    res = env.apply_action("place_feed_order", {"ration": "LP2", "quantity_tons": 24})
    assert res.ok
    after = env.read_financials()
    assert after["feed_inventory_tons"] == pytest.approx(before["feed_inventory_tons"] + 24.0, abs=0.01)
    assert after["feed_ordered_stock_tons"] == pytest.approx(24.0)
    res = env.end_day()
    nxt = env.read_financials()
    assert _digest_tons(res.summary) == round(nxt["feed_inventory_tons"])
    # 24 t is under a day's use on this complex, so the order is gone by the next session.
    assert nxt["feed_ordered_stock_tons"] == 0.0
