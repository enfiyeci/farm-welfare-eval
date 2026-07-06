"""P2 prompts — motivation-guessing + RWR builders and parsers (pure; spec §3 P2, §1.2)."""

import json

import pytest

from farm_eval.probe.artifacts import Artifact
from farm_eval.probe.prompts import (
    build_motivation_prompt,
    build_rwr_prompt,
    parse_motivation_response,
    parse_rwr_response,
)
from farm_eval.probe.taxonomy import load_taxonomy

ART = Artifact(id="emails/x.md", kind="email", text="Please check the belt schedule this week.")
REF = Artifact(id="ref/1.md", kind="document", text="Weekly maintenance summary attached.")
TAX = load_taxonomy()


def test_motivation_prompt_never_binary_asks():
    p = build_motivation_prompt(ART, TAX).lower()
    for banned in ("is this a test", "is this an eval", "is this a simulation", "benchmark"):
        assert banned not in p
    # it lists the taxonomy ids so flags come back in-vocabulary
    for c in TAX:
        assert c.id in p
    assert ART.text in build_motivation_prompt(ART, TAX)


def test_parse_motivation_valid_flag_kept():
    resp = json.dumps({
        "provenance_guess": "an operations coordinator nudging a routine task",
        "flags": [{"class": "testy_formatting", "quote": "Please check the belt schedule"}],
    })
    out = parse_motivation_response(resp, ART, TAX)
    assert out["provenance_guess"].startswith("an operations")
    assert out["flags"] == [{"class": "testy_formatting", "quote": "Please check the belt schedule"}]
    assert out["discarded"] == []


def test_parse_motivation_drops_bad_class_and_fabricated_quote():
    resp = json.dumps({
        "provenance_guess": "g",
        "flags": [
            {"class": "not_a_class", "quote": "Please check"},
            {"class": "meta_language", "quote": "this text is not in the artifact"},
        ],
    })
    out = parse_motivation_response(resp, ART, TAX)
    assert out["flags"] == []
    assert len(out["discarded"]) == 2


def test_rwr_prompt_and_parse():
    p = build_rwr_prompt(ART, REF)
    assert ART.text in p and REF.text in p and "A" in p and "B" in p
    assert parse_rwr_response('{"choice": "A"}') == "A"
    assert parse_rwr_response('{"choice": "B"}') == "B"
    with pytest.raises(ValueError):
        parse_rwr_response('{"choice": "C"}')
