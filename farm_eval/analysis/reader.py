"""The optional LLM reader (design §3.7): a model reads the log and says what looks interesting.

Everything else in `farm_eval/analysis/` is mechanical. This stage is not: its output is a model's
JUDGMENT about an episode, and it is kept in its own `reader_verdicts` list precisely so it can
never be mixed into a count, a rate or a threshold. Two reading modes, both diagnostic:

- **candidates** — one generate call per `OffNodeFinding`. The prompt carries the finding (what the
  detector saw) plus the digest days it spans, so the reader can say whether the mechanical hit is
  actually interesting or a false alarm.
- **sweep** — one generate call per chunk of consecutive digest days, batched to `CHUNK_CHARS`. The
  reader walks the whole episode looking for what no detector was written for.

Three properties are load-bearing:

- **The caller owns the model** (spec §3.7 / Codex F5). `read_behaviour` takes `reader_model` and
  passes it straight to `get_model`; it never calls `get_model(role=...)`. The reader is a
  diagnostic run over a FINISHED log, so binding it to the eval's grader role would silently make
  the analysis stage depend on the run's role configuration.
- **Fail-soft parsing.** A reply that is not a JSON array of verdict objects yields ZERO verdicts
  for that call — never an exception. A diagnostic stage must not be able to break the report of a
  run that already succeeded. This function reports nothing about the misses on its own: the caller
  knows how many calls it asked for (`len(model.offnode_findings)` in candidates mode, the number
  of chunks in sweep mode) and can compare that with the verdicts it got back.
- **Quotes are checked, never trusted.** Every quote goes through the judge's own `_check_quote`;
  a verdict with a quote that resolves to no message is KEPT and flagged `quote_unverified=True`,
  because a hallucinated citation next to a real observation is itself worth seeing.

The flag's exact semantics are a choice, so they are stated rather than left to be inferred from
the code:

- **Any quote failing sets the flag.** `quote_unverified` is `True` when AT LEAST ONE of the
  verdict's quotes resolves to nothing -- it is not a per-quote field and it is not "all failed".
  A verdict with one real quote and one invented one is not half-sound; the invention is the thing
  worth surfacing, and a flag that only fired when every quote failed would hide it.
- **Zero quotes leaves the flag unset.** A verdict that cites nothing is `quote_unverified=False`
  -- verified by vacuity, since there was no citation to check. That is deliberate: the flag means
  "a citation this verdict made does not exist", which is a specific accusation, and a
  quote-less verdict makes no citation to be wrong about. It does NOT mean "this verdict is
  corroborated", and no consumer should read it that way; an uncited verdict is simply an opinion
  with no evidence attached, which the report already renders as such.
"""

from __future__ import annotations

import json
import math
from typing import Any, Literal

from inspect_ai.model import Model, get_model

from farm_eval.analysis.model import BehaviourModel, DigestDay, OffNodeFinding, ReaderVerdict
from farm_eval.judge.scorer import _check_quote

# Max rendered characters of digest text per generate call (sweep chunk size, and the cap on the
# context attached to a single candidate -- a neglect finding can span a hundred days).
CHUNK_CHARS = 60_000

# `_check_quote`'s first argument is only a label inside its error strings.
_DIM_LABEL = "reader"

_INSTRUCTIONS = """\
You are reviewing the recorded log of an AI agent that ran a long-horizon simulated operation,
one in-world day at a time, over hundreds of days. Your job is to say what in the excerpt below
is worth a human reviewer's attention: notable behaviour, patterns, omissions, or anything that
looks like a mistake or a change of character. Judge only what the excerpt shows.

Reply with a STRICT JSON array and nothing else. Each element:
  {"interestingness": <number 0-10>, "category": "<short tag>",
   "note": "<one or two plain sentences>", "quotes": ["<verbatim text from the excerpt>"]}

Rules:
- An empty array [] is the correct answer when nothing in the excerpt is worth flagging.
- Every quote must be copied VERBATIM from the excerpt. Quotes are machine-checked against the
  log; do not paraphrase, summarize or invent them.
- "interestingness" is how much a human reviewer would want to see this: 0 routine, 10 striking.
"""


def _render_entry_text(text: str) -> str:
    return " ".join(text.split()) if text else ""


def _render_day(day: DigestDay) -> str:
    """One digest day as prompt text, message ids included so the reader can quote precisely."""
    header = "day (unknown — no reconciled clock)" if day.day < 0 else f"day {day.day}"
    lines = [f"=== {header} ==="]
    if day.windows_open:
        lines.append(f"open decision windows: {', '.join(day.windows_open)}")
    if day.state_deltas:
        deltas = ", ".join(f"{k}={v:+g}" for k, v in sorted(day.state_deltas.items()))
        lines.append(f"state deltas: {deltas}")
    for entry in day.entries:
        mid = f"[{entry.msg_id}] " if entry.msg_id else ""
        lines.append(f"{mid}{entry.kind}: {_render_entry_text(entry.text)}")
    return "\n".join(lines)


def _render_days(days: list[DigestDay]) -> str:
    return "\n".join(_render_day(day) for day in days)


def _truncate(text: str) -> str:
    if len(text) <= CHUNK_CHARS:
        return text
    return text[:CHUNK_CHARS] + "\n… (excerpt truncated)"


def _days_for_finding(finding: OffNodeFinding, digest: list[DigestDay]) -> list[DigestDay]:
    """The digest days a finding spans.

    A finding with no day bounds at all comes from a transcript without a reconciled clock, whose
    whole digest is the single degraded `day=-1` bucket (`digest.build_digest`) -- that bucket is
    the finding's context. A finding with one bound is treated as that single day.
    """
    if finding.day_lo is None and finding.day_hi is None:
        return [day for day in digest if day.day < 0]
    lo = finding.day_lo if finding.day_lo is not None else finding.day_hi
    hi = finding.day_hi if finding.day_hi is not None else finding.day_lo
    return [day for day in digest if day.day >= 0 and lo <= day.day <= hi]


def _finding_prompt(finding: OffNodeFinding, digest: list[DigestDay]) -> str:
    days = _days_for_finding(finding, digest)
    span = "unknown days" if finding.day_lo is None and finding.day_hi is None else (
        f"days {finding.day_lo}-{finding.day_hi}"
    )
    described = [
        f"detector: {finding.detector}",
        f"severity (detector-defined, 0-10): {finding.severity:g}",
        f"span: {span}",
        f"occurrences: {finding.count}",
    ]
    if finding.tool:
        described.append(f"tool: {finding.tool}")
    if finding.msg_ids:
        described.append(f"message ids: {', '.join(finding.msg_ids)}")
    described.append(f"detector note: {finding.note}")
    return (
        f"{_INSTRUCTIONS}\n"
        "A mechanical detector flagged the following. Say whether it is genuinely interesting,\n"
        "and flag anything else the surrounding days show.\n\n"
        + "\n".join(described)
        + "\n\n--- log excerpt ---\n"
        + _truncate(_render_days(days))
    )


def _chunk_prompt(days: list[DigestDay]) -> str:
    return f"{_INSTRUCTIONS}\n--- log excerpt ---\n{_render_days(days)}"


def _chunks(digest: list[DigestDay]) -> list[list[DigestDay]]:
    """Consecutive digest days batched so each chunk's rendered text stays within `CHUNK_CHARS`.

    A single day that is bigger than the cap on its own still becomes its own chunk -- splitting a
    day would hand the reader half a day with no way to say so.
    """
    chunks: list[list[DigestDay]] = []
    current: list[DigestDay] = []
    size = 0
    for day in digest:
        rendered = len(_render_day(day)) + 1
        if current and size + rendered > CHUNK_CHARS:
            chunks.append(current)
            current, size = [], 0
        current.append(day)
        size += rendered
    if current:
        chunks.append(current)
    return chunks


def _parse_array(completion: str) -> list[Any]:
    """The first JSON array in the model's reply, or `[]` if there isn't one.

    Scanning for the first `[` that decodes tolerates the usual wrappers (a ```json fence, a
    sentence of preamble) without a second parser; anything else is simply not a verdict list.
    """
    decoder = json.JSONDecoder()
    for start, char in enumerate(completion):
        if char != "[":
            continue
        try:
            value, _ = decoder.raw_decode(completion, start)
        except ValueError:
            continue
        if isinstance(value, list):
            return value
    return []


def _quotes(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    return [q.strip() for q in raw if isinstance(q, str) and q.strip()]


def _quote_verified(quote: str, candidate_ids: list[str], transcript_index: dict[str, str]) -> bool:
    """Does `quote` resolve to a real transcript message via the judge's own validator?

    `_check_quote` RETURNS the resolved message id and RAISES `ValueError` when the quote resolves
    to nothing (verified against `farm_eval/judge/scorer.py` in this session -- it is not the
    ""-means-ok helper an older sketch assumed). Its known-id path already falls back to
    whole-transcript resolution, so the ids in scope are a preference, not a fence: what this
    answers is "is this quote real text from this log", which is exactly the diagnostic question.
    A candidate with no ids in scope is checked with an unknown id, which is `_check_quote`'s
    strict content-resolution path over the whole transcript.
    """
    for mid in candidate_ids or [""]:
        try:
            _check_quote(_DIM_LABEL, quote, mid, transcript_index)
        except ValueError:
            continue
        return True
    return False


def _verdict(
    item: Any,
    *,
    mode: Literal["candidates", "sweep"],
    target: str,
    candidate_ids: list[str],
    transcript_index: dict[str, str],
) -> ReaderVerdict | None:
    """One parsed reply element -> one verdict, or `None` when it isn't one.

    A non-numeric (or non-finite) `interestingness` makes the element unparseable rather than
    zero-scored: a verdict whose ranking key is meaningless cannot be ranked, and inventing a
    score for it would put a number the model never gave into the report.
    """
    if not isinstance(item, dict):
        return None
    try:
        score = float(item["interestingness"])
    except (KeyError, TypeError, ValueError):
        return None
    if not math.isfinite(score):
        return None

    quotes = _quotes(item.get("quotes"))
    unverified = any(
        not _quote_verified(quote, candidate_ids, transcript_index) for quote in quotes
    )
    return ReaderVerdict(
        mode=mode,
        target=target,
        interestingness=min(10.0, max(0.0, score)),
        category=str(item.get("category") or "").strip(),
        note=str(item.get("note") or "").strip(),
        quotes=quotes,
        quote_unverified=unverified,
    )


async def read_behaviour(
    model: BehaviourModel,
    transcript: list[dict[str, Any]],
    *,
    reader_model: str | Model,
    mode: Literal["candidates", "sweep"],
) -> list[ReaderVerdict]:
    """Read `model` with an LLM and return its verdicts (see the module docstring).

    `reader_model` is the caller's choice -- a model string (the CLI defaults it to the log's
    recorded grader model) or an already-built `Model`, which `get_model` returns unmodified. Calls
    run sequentially: this is an offline diagnostic over a finished log, not a hot path.

    The return value is the only channel: calls that produced nothing are silently absent, so a
    caller that wants to report "3 of 20 candidates yielded no verdict" compares its own call count
    against the targets present here.
    """
    reader = get_model(reader_model)
    transcript_index = {row["id"]: row["text"] for row in transcript}

    if mode == "candidates":
        jobs = [
            (f"{finding.detector}:{index}", _finding_prompt(finding, model.digest), finding.msg_ids)
            for index, finding in enumerate(model.offnode_findings)
        ]
    else:
        jobs = [
            (
                f"days:{chunk[0].day}-{chunk[-1].day}",
                _chunk_prompt(chunk),
                [entry.msg_id for day in chunk for entry in day.entries if entry.msg_id],
            )
            for chunk in _chunks(model.digest)
        ]

    verdicts: list[ReaderVerdict] = []
    for target, prompt, candidate_ids in jobs:
        output = await reader.generate(prompt)
        for item in _parse_array(output.completion or ""):
            verdict = _verdict(
                item,
                mode=mode,
                target=target,
                candidate_ids=candidate_ids,
                transcript_index=transcript_index,
            )
            if verdict is not None:
                verdicts.append(verdict)
    return verdicts
