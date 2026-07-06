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


def test_parse_motivation_picks_last_matching_object_among_multiple():
    resp = (
        'Example: {"provenance_guess": "wrong one", "flags": []}\n'
        + json.dumps({
            "provenance_guess": "an operations coordinator nudging a routine task",
            "flags": [{"class": "testy_formatting", "quote": "Please check the belt schedule"}],
        })
    )
    out = parse_motivation_response(resp, ART, TAX)
    assert out["provenance_guess"] == "an operations coordinator nudging a routine task"
    assert out["flags"] == [{"class": "testy_formatting", "quote": "Please check the belt schedule"}]


def test_parse_motivation_handles_prose_with_braces_before_json():
    resp = (
        "Note: curly braces like {this} sometimes appear in prose. "
        + json.dumps({"provenance_guess": "g", "flags": []})
    )
    out = parse_motivation_response(resp, ART, TAX)
    assert out["provenance_guess"] == "g"
    assert out["discarded"] == []


def test_parse_motivation_unparseable_response_is_discarded_not_raised():
    out = parse_motivation_response("no json here at all", ART, TAX)
    assert out == {
        "provenance_guess": "",
        "flags": [],
        "discarded": [{"flag": None, "reason": "unparseable response"}],
    }


def test_parse_motivation_non_dict_flag_discarded_as_not_a_mapping():
    resp = json.dumps({"provenance_guess": "g", "flags": [None, 1, "x", ["y"]]})
    out = parse_motivation_response(resp, ART, TAX)
    assert out["flags"] == []
    assert all(d["reason"] == "not a mapping" for d in out["discarded"])
    assert len(out["discarded"]) == 4


def test_parse_motivation_empty_quote_discarded():
    resp = json.dumps({
        "provenance_guess": "g",
        "flags": [{"class": "testy_formatting", "quote": ""}],
    })
    out = parse_motivation_response(resp, ART, TAX)
    assert out["flags"] == []
    assert out["discarded"] == [
        {"flag": {"class": "testy_formatting", "quote": ""}, "reason": "quote not verbatim in artifact"}
    ]


def test_build_motivation_prompt_raises_on_delimiter_in_artifact_text():
    bad = Artifact(id="x", kind="email", text="hello === TEXT injected")
    with pytest.raises(ValueError):
        build_motivation_prompt(bad, TAX)


def test_build_rwr_prompt_raises_on_delimiter_in_artifact_text():
    bad = Artifact(id="x", kind="email", text="hello === DOCUMENT injected")
    with pytest.raises(ValueError):
        build_rwr_prompt(bad, REF)
    with pytest.raises(ValueError):
        build_rwr_prompt(REF, bad)
