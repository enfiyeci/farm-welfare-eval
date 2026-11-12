"""Per-turn console-session guard shared by every Inspect tool wrapper."""

from inspect_ai.util import store_as

from farm_eval.adapter.context import EpisodeStore


SESSION_CLOSED = "Console: this session is closed; the command was not run."


def refuse_closed_call() -> str | None:
    store = store_as(EpisodeStore)
    if not store.session_closed_this_turn:
        return None
    store.refused_calls += 1
    return SESSION_CLOSED
