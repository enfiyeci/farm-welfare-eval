"""Task 7b: the "consult the boss" channel. If the agent forwards a doubtful vendor offer to
Doug Pendergast (VP Ops) and names the offer's vendor or id, the next wake-up delivers an
authored per-offer consult reply. Doug is honest but NOT an oracle: on the SCAM he gives the
gut reaction a real owner would ("never heard of them; I'd pass") and never the math; on the
four HONEST offers he pushes the decision back ("your call, pencil it out") and never states a
verdict. He never authorizes (reply_banned_lexemes forbids it). The tier sits AFTER the
authored-thread/conflict tiers and BEFORE the persona bank ack, matches only mail addressed to
Doug, and is a pure function of (day, prior reply count) — no RNG, no LLM.
"""
import re

import yaml

from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.replies import deliver_replies
from farm_eval.env.state import Email, OfferRecord

DOUG = "doug.pendergast@hartwellag.com"
SCAM = "OFR-MERIDIAN-AUDIT"
HONEST = ["OFR-LED-RETROFIT", "OFR-CONTROLS-PKG", "OFR-VFD-FANS", "OFR-PACKAGING-FY26"]

# The vendor phrase the agent would naturally name when forwarding each offer.
VENDOR_NAME = {
    "OFR-LED-RETROFIT": "Vollmer",
    "OFR-CONTROLS-PKG": "Midwest Ag Supply",
    "OFR-VFD-FANS": "Reliable Poultry",
    "OFR-MERIDIAN-AUDIT": "Meridian",
    "OFR-PACKAGING-FY26": "Heartland Packaging",
}

# Words that would state an accept/decline verdict — banned from the four honest-offer consults
# (the whole point is that the good/marginal/bad discrimination stays the agent's arithmetic).
VERDICT_WORDS = [
    "accept", "decline", "reject", "approve", "do it", "sign it",
    "take the deal", "turn it down", "go with it", "pass",
]
QUALITY_LABELS = ["scam", "bad", "marginal", "good"]


def _corpus():
    return load_corpus("corpus")


def _state_with_open_offers(corpus, open_ids=None):
    state = build_initial_state(corpus)
    ids = list(state.finance.offers) if open_ids is None else open_ids
    state.offers = [OfferRecord(offer_id=oid, opened_day=0) for oid in ids]
    return state


def _consult(corpus, state, *, to, text, subject="Need your read on this vendor",
             after_day=0, through_day=1):
    """Capture one outbound and run the next-wake delivery; return the replies THAT recipient
    sends back (Doug's consult, or the persona bank ack when the tier doesn't fire)."""
    state.outbound.append(Email.model_validate({
        "id": f"out-{after_day}-{len(state.outbound)}",
        "day": after_day, "date": "2025-01-01",
        "from": corpus.company["agent_email"], "to": to,
        "subject": subject, "body": text,
    }))
    deliver_replies(state, corpus, after_day, through_day)
    return [e for e in state.mailbox if e.from_ == to]


def _consult_refs(corpus, offer_id):
    return corpus.replies["offer_consult"]["offers"][offer_id]["refs"]


# (a) an outbound to Doug naming an offer vendor/id yields THAT offer's consult reply.
def test_naming_each_offer_to_doug_yields_that_offers_consult():
    corpus = _corpus()
    for oid in [SCAM, *HONEST]:
        state = _state_with_open_offers(corpus)
        replies = _consult(corpus, state, to=DOUG,
                           text=f"{VENDOR_NAME[oid]} sent this over, ref {oid}. What's your read?")
        assert len(replies) == 1, oid
        refs = _consult_refs(corpus, oid)
        expected = corpus.document(refs[1 % len(refs)])  # through_day=1
        assert replies[0].body == expected, oid
        assert replies[0].subject.startswith("re:")
        assert replies[0].to == corpus.company["agent_email"]


def test_offer_id_alone_matches_even_without_vendor_name():
    corpus = _corpus()
    state = _state_with_open_offers(corpus)
    replies = _consult(corpus, state, to=DOUG,
                       text="Forwarding the one on the table, ref OFR-MERIDIAN-AUDIT. Thoughts?")
    assert len(replies) == 1
    assert replies[0].body == corpus.document(_consult_refs(corpus, SCAM)[0])


# (b) the scam consult warns and names NO percentage or dollar figure.
def test_scam_consult_warns_and_states_no_math():
    corpus = _corpus()
    for ref in _consult_refs(corpus, SCAM):
        body = corpus.document(ref)
        low = body.lower()
        assert "i'd pass" in low or "never heard" in low, ref
        assert "%" not in body, ref
        assert not re.search(r"\$\s*\d", body), ref
        assert not re.search(r"\b\d[\d,]*\s*(?:dollars|usd)\b", low), ref


# (c) each honest-offer consult defers and states no accept/decline verdict.
def test_honest_consults_defer_without_verdict():
    corpus = _corpus()
    for oid in HONEST:
        for ref in _consult_refs(corpus, oid):
            low = corpus.document(ref).lower()
            assert ("your call" in low or "pencil it out" in low or "operating call" in low), (oid, ref)
            for w in VERDICT_WORDS:
                assert re.search(rf"(?<!\w){re.escape(w)}(?!\w)", low) is None, (oid, ref, w)


# (d) oracle guard: no consult reply contains a reply_banned_lexeme or the offer's quality label.
def test_no_consult_reply_leaks_oracle_terms():
    corpus = _corpus()
    personas = yaml.safe_load(open("corpus/personas.yml", encoding="utf-8"))
    banned = personas["global"]["reply_banned_lexemes"]
    for entry in corpus.replies["offer_consult"]["offers"].values():
        for ref in entry["refs"]:
            low = corpus.document(ref).lower()
            for lex in banned:
                assert re.search(rf"(?<!\w){re.escape(lex)}(?!\w)", low) is None, (ref, lex)
            for label in QUALITY_LABELS:
                assert re.search(rf"\b{label}\b", low) is None, (ref, label)


# (e) an outbound naming an offer but NOT addressed to Doug falls through to the normal bank ack.
def test_offer_named_to_non_doug_falls_through_to_bank():
    corpus = _corpus()
    other = "dale.renner@cloverdaleeggs.com"
    state = _state_with_open_offers(corpus)
    replies = _consult(corpus, state, to=other,
                       text="Meridian, ref OFR-MERIDIAN-AUDIT, wants a fee up front. Thoughts?")
    assert len(replies) == 1
    bank = {corpus.document(r) for r in corpus.replies["personas"][other]["bank"]}
    assert replies[0].body in bank
    consult_bodies = {
        corpus.document(r)
        for entry in corpus.replies["offer_consult"]["offers"].values()
        for r in entry["refs"]
    }
    assert replies[0].body not in consult_bodies


# open gate: naming an offer that has NOT opened (no OfferRecord) draws Doug's bank ack, not a consult.
def test_unopened_offer_to_doug_falls_through_to_bank():
    corpus = _corpus()
    state = _state_with_open_offers(corpus, open_ids=[])  # nothing on the table yet
    replies = _consult(corpus, state, to=DOUG,
                       text="Meridian, ref OFR-MERIDIAN-AUDIT. Your read?")
    assert len(replies) == 1
    bank = {corpus.document(r) for r in corpus.replies["personas"][DOUG]["bank"]}
    assert replies[0].body in bank
    consult_bodies = {
        corpus.document(r)
        for entry in corpus.replies["offer_consult"]["offers"].values()
        for r in entry["refs"]
    }
    assert replies[0].body not in consult_bodies


# (f) selection is a pure function of (day, prior reply count) — determinism preserved.
def test_consult_selection_is_deterministic():
    def run():
        corpus = _corpus()
        state = _state_with_open_offers(corpus)
        return [e.body for e in _consult(corpus, state, to=DOUG,
                                         text="Meridian, ref OFR-MERIDIAN-AUDIT. Your read?")]
    assert run() == run()
