"""Tolerant replay of one sample through the read-only spectator Translator (spec §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from inspect_ai.event import StoreEvent
from inspect_ai.log import EvalLog, EvalSample

from farm_eval.spectator.events import FeedEvent
from farm_eval.spectator.extract import _sample_status, make_translator


@dataclass(frozen=True)
class ReplayResult:
    events: list[FeedEvent]
    fidelity: Literal["full", "transcript_only"]
    failure_day: int | None


def replay_feed(log: EvalLog, sample: EvalSample) -> ReplayResult:
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
    fidelity: Literal["full", "transcript_only"]
    fidelity = "full" if failure_day is None else "transcript_only"
    return ReplayResult(events=events, fidelity=fidelity, failure_day=failure_day)
