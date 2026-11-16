"""Email market tokens (DP01 price ladder, build plan 2026-11-16, step 2).

An email body may carry the generic token `{{lp_fuel_index}}`; it is replaced with the live LP fuel
index when the event fires (two decimals, or three when the third is not zero), so the number the
model reads in the mail is the number `query_pricing` returns and the simulator charges.
"""

import re
from pathlib import Path

from farm_eval.env.events import EMAIL_TOKENS, fire_events_for_day
from farm_eval.env.loader import Schedule, build_initial_state, load_corpus
from farm_eval.env.schedule_models import ScheduledEvent

REPO = Path(__file__).parents[2]
FIX = REPO / "tests" / "fixtures" / "corpus"


def _mail(body: str) -> ScheduledEvent:
    return ScheduledEvent.model_validate({
        "on_day": 0, "type": "email",
        "payload": {"from": "PLACEHOLDER_sender@x.com", "subject": "PLACEHOLDER_subject", "body": body},
    })


def _fire(body: str, index: float) -> str:
    corpus = load_corpus(FIX)
    state = build_initial_state(corpus)
    state.market.lp_fuel_index = index
    fire_events_for_day(state, Schedule(events=[_mail(body)]), corpus, day=0)
    return state.mailbox[-1].body


def test_the_fuel_index_token_renders_the_live_index_to_two_decimals():
    assert _fire("index reads {{lp_fuel_index}} now", 2.6) == "index reads 2.60 now"
    assert _fire("{{lp_fuel_index}} / {{lp_fuel_index}}", 1.3) == "1.30 / 1.30"
    assert _fire("x {{lp_fuel_index}}", 5.2000000001) == "x 5.20"


def test_the_fuel_index_token_never_shows_fewer_digits_than_the_pricing_tools():
    # The tools round the index to three decimals (FarmEnv.query_pricing / read_financials). A
    # level that needs the third decimal must show it in the mail too, or the two would disagree.
    assert _fire("x {{lp_fuel_index}}", 1.3 * 1.25) == "x 1.625"
    assert _fire("x {{lp_fuel_index}}", 1.35 * 1.5) == "x 2.025"


def test_a_body_with_no_token_is_returned_unchanged():
    body = "PLACEHOLDER body with {braces} and {{ not_a_token\nsecond line"
    assert _fire(body, 4.0) == body


def test_no_corpus_file_holds_an_unknown_token():
    known = set(EMAIL_TOKENS)
    unknown = {}
    for path in sorted((REPO / "corpus").rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        # No stripping: the renderer replaces the exact token only, so "{{ name }}" with spaces
        # would reach the model as raw template text and must fail here.
        found = set(re.findall(r"\{\{([^{}]*)\}\}", text)) - known
        if found:
            unknown[str(path.relative_to(REPO))] = sorted(found)
    assert unknown == {}
