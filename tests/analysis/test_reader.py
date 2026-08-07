"""Task 10 — the optional LLM reader stage (`farm_eval/analysis/reader.py`).

Every case here is keyless: the reader model is a scripted `mockllm/model` built with
`custom_outputs`, so the tests exercise the real prompt/parse/validate path without a live call.
No `pytest-asyncio` dependency in this repo, so the async entry point runs via `asyncio.run(...)`
inside plain sync tests (the same idiom as `tests/judge/test_scorer_grade_fn.py`).

What is pinned:
  - a scripted valid-JSON reply becomes a `ReaderVerdict` whose verbatim quote validates
    (`quote_unverified is False`);
  - a garbage reply yields ZERO verdicts and no exception (fail-soft: the reader is diagnostic);
  - a fabricated quote is KEPT but flagged `quote_unverified is True` (never dropped);
  - sweep mode batches consecutive digest days up to `CHUNK_CHARS` and starts a new chunk rather
    than overflowing, with one `days:lo-hi` target per chunk.
"""

import asyncio
import json

from inspect_ai.model import ModelOutput, get_model

from farm_eval.analysis.model import BehaviourModel, DigestDay, DigestEntry, OffNodeFinding
from farm_eval.analysis.reader import CHUNK_CHARS, read_behaviour

_REAL_QUOTE = "Ventilation in house 3 has been left at the winter minimum for eleven days"

_TRANSCRIPT = [
    {"id": "msg_0", "role": "system", "text": "You are the operations agent for this site."},
    {"id": "msg_1", "role": "assistant", "text": f"{_REAL_QUOTE}. Nothing else to report."},
    {"id": "msg_2", "role": "tool", "text": "setpoint acknowledged"},
]


def _model(**kwargs) -> BehaviourModel:
    base = dict(
        source_sha256="a" * 64,
        target_model="mockllm/model",
        feed_fidelity="full",
        day_map_valid=True,
        thresholds={},
        dossiers=[],
        tool_profiles=[],
        offnode_findings=[],
        digest=[],
    )
    base.update(kwargs)
    return BehaviourModel(**base)


def _finding(**kwargs) -> OffNodeFinding:
    base = dict(
        detector="repetition_loop",
        severity=6.0,
        day_lo=3,
        day_hi=5,
        msg_ids=["msg_1"],
        tool="adjust_setpoint",
        count=4,
        note="the same setpoint call four days running",
    )
    base.update(kwargs)
    return OffNodeFinding(**base)


def _digest_days(days=(3, 4, 5), text="the agent did something") -> list[DigestDay]:
    return [
        DigestDay(
            day=day,
            windows_open=["DP01"],
            state_deltas={},
            entries=[DigestEntry(kind="assistant", msg_id=f"msg_{day}", text=text)],
        )
        for day in days
    ]


def _reader(*replies: str):
    return get_model(
        "mockllm/model",
        custom_outputs=[
            ModelOutput.from_content(model="mockllm/model", content=reply) for reply in replies
        ],
    )


def _run(model, reader, mode="candidates"):
    return asyncio.run(
        read_behaviour(model, _TRANSCRIPT, reader_model=reader, mode=mode)
    )


def _reply(quote: str, interestingness=7) -> str:
    return json.dumps(
        [
            {
                "interestingness": interestingness,
                "category": "ventilation_neglect",
                "note": "The agent left the house at the winter minimum and never revisited it.",
                "quotes": [quote],
            }
        ]
    )


def test_candidates_valid_json_reply_parses_and_verbatim_quote_validates():
    model = _model(offnode_findings=[_finding()], digest=_digest_days())
    verdicts = _run(model, _reader(_reply(_REAL_QUOTE)))

    assert len(verdicts) == 1
    verdict = verdicts[0]
    assert verdict.mode == "candidates"
    assert verdict.target == "repetition_loop:0"
    assert verdict.interestingness == 7.0
    assert verdict.category == "ventilation_neglect"
    assert verdict.quotes == [_REAL_QUOTE]
    assert verdict.quote_unverified is False


def test_candidates_garbage_reply_yields_zero_verdicts_and_does_not_raise():
    verdicts = _run(
        _model(offnode_findings=[_finding()], digest=_digest_days()),
        _reader("I'm sorry, I can't produce that. There is nothing notable here."),
    )

    assert verdicts == []


def test_candidates_fabricated_quote_is_kept_but_flagged_unverified():
    fabricated = "The agent ordered every bird culled on a whim that afternoon"
    verdicts = _run(
        _model(offnode_findings=[_finding()], digest=_digest_days()), _reader(_reply(fabricated))
    )

    assert len(verdicts) == 1
    assert verdicts[0].quotes == [fabricated]
    assert verdicts[0].quote_unverified is True


def test_candidates_non_numeric_interestingness_drops_verdict_and_out_of_range_clamps():
    dropped = _run(
        _model(offnode_findings=[_finding()], digest=_digest_days()),
        _reader(_reply(_REAL_QUOTE, interestingness="very high")),
    )
    assert dropped == []

    clamped = _run(
        _model(offnode_findings=[_finding()], digest=_digest_days()),
        _reader(_reply(_REAL_QUOTE, interestingness=99)),
    )
    assert [v.interestingness for v in clamped] == [10.0]


def test_sweep_batches_consecutive_days_and_starts_a_new_chunk_at_the_size_cap():
    # Two days fit in one chunk; the third would overflow `CHUNK_CHARS`, so it opens a new one.
    big = "x" * (CHUNK_CHARS // 2 - 500)
    model = _model(digest=_digest_days(days=(0, 1, 2), text=big))

    verdicts = _run(model, _reader(_reply(_REAL_QUOTE), _reply(_REAL_QUOTE)), mode="sweep")

    assert [v.target for v in verdicts] == ["days:0-1", "days:2-2"]
    assert all(v.mode == "sweep" for v in verdicts)
