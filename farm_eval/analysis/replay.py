"""Tolerant replay of one sample through the read-only spectator Translator (spec §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from inspect_ai.event import StoreEvent
from inspect_ai.log import EvalLog, EvalSample

from farm_eval.spectator.events import FeedEvent
from farm_eval.spectator.extract import _check_reconstruction, _sample_status, make_translator


@dataclass(frozen=True)
class ReplayResult:
    events: list[FeedEvent]
    fidelity: Literal["full", "transcript_only"]
    failure_day: int | None
    #: Why fidelity is not `full` when no store patch actually failed -- today, only the
    #: final-state mismatch below. `None` when fidelity is full, or when `failure_day` already
    #: says what went wrong.
    fidelity_reason: str | None = None


def replay_feed(log: EvalLog, sample: EvalSample) -> ReplayResult:
    """Replay one sample's events into feed events, degrading rather than raising.

    Two things can go wrong with the state reconstruction, and `full` fidelity means neither did:

    - **A store patch no longer applies** (the loop below). The translator latches state derivation
      off and keeps translating the transcript stream, and the day it stopped is recorded.
    - **The replayed final state does not equal the state the run itself recorded** (the check
      after the loop). Every patch applied, so nothing looked wrong -- but the resulting state
      series describes a different episode than the one that ran, which is worse than having no
      series at all, because it is state-shaped and wrong.

    The second check is the spectator's own (`_check_reconstruction`, imported read-only, the same
    private-import precedent as `_sample_status`), so the two tools agree on what a faithful replay
    is. Where they differ is the response: the spectator raises, because it exists to produce a
    trustworthy feed; this wrapper exists to stay analysable over OLD logs, so it degrades to
    `transcript_only` and records `fidelity_reason` -- the reader is told the state disagreed
    rather than being told, misleadingly, that the feed stopped.
    """
    translator = make_translator(log.eval, sample.uuid or str(sample.id))
    events: list[FeedEvent] = []
    failure_day: int | None = None
    for event in sample.events or []:
        try:
            events += translator.handle(event)
        except Exception:
            # Only a StoreEvent can break the shadow reconstruction; the translator has
            # latched state derivation off and keeps translating the transcript stream.
            # Anything else is a real bug and must not be swallowed.
            if not isinstance(event, StoreEvent):
                raise
            if failure_day is None:
                failure_day = translator.day
    events += translator.finish(_sample_status(log, sample))

    fidelity_reason: str | None = None
    if failure_day is None:
        try:
            _check_reconstruction(translator, sample)
        except Exception as error:
            fidelity_reason = (
                "Every store patch applied, but the replayed environment state does not match the "
                "final state the run recorded, so the state series describes a different episode "
                f"than the one that ran ({error or type(error).__name__})."
            )

    fidelity: Literal["full", "transcript_only"]
    fidelity = "full" if failure_day is None and fidelity_reason is None else "transcript_only"
    return ReplayResult(
        events=events,
        fidelity=fidelity,
        failure_day=failure_day,
        fidelity_reason=fidelity_reason,
    )
