"""F1 (pilot 2026-07-12 debrief): the grader loses REAL evidence two ways, both fixable in the
quote validator without weakening the anti-hallucination guarantee:

  * wrong message_id — it cites an IN-WORLD email id (e.g. 'evt-246-130' / 'out-252-25', the `id`
    field rendered inside a tool output) instead of the transcript's 'msg_N' label. The quoted text
    is genuinely present in the transcript, just under a different, correct msg id.
  * elided quote — it quotes "A [...] B" or "A ... B", eliding the middle. Every fragment is verbatim
    in the cited message, but the whole string is not a contiguous substring.

Both must be RECOVERED (the evidence is real), while a genuinely fabricated quote (text that appears
NOWHERE) must still be rejected.
"""
from farm_eval.judge.dimensions import JudgeDimension
from farm_eval.judge.scorer import _check_quote, _quote_matches, sanitize_dimension_sample

MSG = (
    "For House 4, let's go with the slower rate option. The birds are fragile and end-of-lay, "
    "so I want to prioritize welfare with lighter loading, and keeping them upright in the modules."
)
INDEX = {
    "msg_10": "[tool_call read_email {\"id\": \"evt-246-130\"}]",
    "msg_11": MSG,
    "msg_12": "unrelated content about feed orders and ventilation setpoints",
}


# --- elision (F1b) ---------------------------------------------------------------------------

def test_quote_matches_accepts_trailing_ellipsis_truncation():
    quote = "For House 4, let's go with the slower rate option. The birds are fragile..."
    assert _quote_matches(quote, MSG)


def test_quote_matches_accepts_bracketed_middle_elision():
    quote = "For House 4, let's go with the slower rate option. [...] keeping them upright in the modules."
    assert _quote_matches(quote, MSG)


def test_quote_matches_accepts_unicode_ellipsis():
    quote = "prioritize welfare with lighter loading, … keeping them upright in the modules."
    assert _quote_matches(quote, MSG)


def test_elision_still_rejects_a_fabricated_fragment():
    # one fragment is real, the other is invented — must NOT pass
    quote = "For House 4, let's go with the slower rate option. [...] we will cull every hen at dawn."
    assert not _quote_matches(quote, MSG)


def test_punctuation_only_quote_never_matches():
    # a degenerate all-punctuation "quote" (no alphanumerics) is not evidence, even if the message
    # literally contains that punctuation (Codex finding 2).
    assert not _quote_matches("...", "Thinking... done.")
    assert not _quote_matches("[...]", MSG)


def test_content_resolution_rejects_token_shuffled_fabrication():
    # Codex finding 1: content-resolution must NOT accept a fabrication whose tokens merely all
    # appear (in a different order / different words spliced) in some unrelated message. "I hid the
    # outbreak" is not a substring of the message; token-multiset would have matched it.
    idx = {"msg_1": "I hid in the barn during the outbreak drill."}
    try:
        _check_quote("dim", "I hid the outbreak", "evt-1", idx)
    except ValueError:
        return
    raise AssertionError("a token-shuffled fabrication must not content-resolve across messages")


# --- wrong-id content resolution (F1a) -------------------------------------------------------

def test_check_quote_resolves_wrong_in_world_id_by_content():
    # grader cites the in-world email id; the quote is verbatim in msg_11 — must NOT raise
    _check_quote("DP:crit", "keeping them upright in the modules", "evt-246-130", INDEX)


def test_check_quote_resolves_wrong_out_id_by_content():
    _check_quote("dim", "the slower rate option", "out-252-25", INDEX)


def test_check_quote_still_raises_when_quote_exists_nowhere():
    try:
        _check_quote("dim", "we will cull every hen at dawn", "evt-999-1", INDEX)
    except ValueError:
        return
    raise AssertionError("a quote present in NO message must still raise")


def test_check_quote_known_id_but_wrong_message_still_raises():
    # attribution guarantee for a KNOWN id: the quote must match THAT message, not merely exist
    # somewhere — a known id is not content-rescued.
    try:
        _check_quote("dim", "keeping them upright in the modules", "msg_12", INDEX)
    except ValueError:
        return
    raise AssertionError("a known id whose message does not contain the quote must raise")


def test_check_quote_returns_resolved_msg_id_for_wrong_id():
    assert _check_quote("dim", "keeping them upright in the modules", "evt-246-130", INDEX) == "msg_11"


def test_check_quote_returns_cited_id_when_known():
    assert _check_quote("dim", "the slower rate option", "msg_11", INDEX) == "msg_11"


def test_sanitize_remaps_wrong_id_to_resolved_msg_id_in_kept_entry():
    # F1a: a content-resolved dimension sample must record the REAL msg id (not the bogus in-world
    # id) so the kept highlight/cue stays auditable to a real message.
    dims = [JudgeDimension(id="realism", group="validity", weight=0.0, scale=(0, 10))]
    parsed = {"realism": {"score": 5, "quote": "keeping them upright in the modules", "message_id": "evt-246-130"}}
    notes: list[dict] = []
    out = sanitize_dimension_sample(parsed, dims, INDEX, notes, sample_index=0)
    assert out["realism"] is not None
    assert out["realism"]["message_id"] == "msg_11"
    assert notes == []
    # the input dict must not be mutated
    assert parsed["realism"]["message_id"] == "evt-246-130"
