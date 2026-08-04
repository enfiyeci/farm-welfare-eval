"""Shadow store: rebuild `EnvState` by replaying Inspect `StoreEvent` JSON patches.

Why this exists (spec §"Env-state snapshots"): the emitter must NOT read the live
`EpisodeStore`. Inspect dispatches hook events through an async queue, so by the time an event
is handled the live store may already hold a LATER day's state. Instead the emitter keeps its
own copy of the store data and applies each `StoreEvent`'s changes **in event order** -- which
is exactly what a post-hoc replay over a recorded `.eval` log does, so live and replay share
one reconstruction path by construction.

`seed()` is REQUIRED before `apply()`: real streams do NOT begin with a root `add`. The initial
`EnvState` exists before store-event recording starts, so the first recorded changes are already
nested (e.g. `replace /EpisodeStore:env_state/mailbox/0/unread`). The seed is the day-0 EnvState
built deterministically through the env core -- without it there is nothing for those pointers to
resolve against.

The patch engine is a minimal RFC 6901 pointer resolver plus the three ops Inspect's store diff
actually emits (`add`/`replace`/`remove`). `move`/`copy`/`test` are rejected loudly rather than
silently ignored: a silently dropped change means every later snapshot is quietly wrong, which is
the one failure mode a spectator feed must never have. For the same reason every malformed or
unresolvable pointer raises -- a partially applied `apply()` leaves the shadow inconsistent, so
callers must treat the error as fatal for the run, not recoverable.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from inspect_ai._util.json import JsonChange

from farm_eval.env.state import EnvState

# The Inspect store namespaces every StoreModel field as "<ClassName>:<field>" (see
# `StoreModel._ns_name`), so `EpisodeStore.env_state` is this flat key at the store root.
ENV_STATE_KEY = "EpisodeStore:env_state"

_SUPPORTED_OPS = ("add", "replace", "remove")


def _parse_pointer(path: str) -> list[str]:
    """Decode an RFC 6901 JSON pointer into its reference tokens."""
    if path == "":
        raise ValueError(
            "shadow store cannot apply a change to the whole document (empty JSON pointer)"
        )
    if not path.startswith("/"):
        raise ValueError(f"malformed JSON pointer (must start with '/'): {path!r}")
    # "~1" -> "/" first, then "~0" -> "~", so "~01" decodes to the literal "~1" (RFC 6901 §4).
    return [token.replace("~1", "/").replace("~0", "~") for token in path[1:].split("/")]


def _list_index(target: list[Any], token: str, *, allow_append: bool) -> int:
    if token == "-":
        if not allow_append:
            raise ValueError("JSON pointer '-' is only valid as the target of an 'add'")
        return len(target)
    try:
        index = int(token)
    except ValueError:
        raise ValueError(f"non-integer index into a list in JSON pointer: {token!r}") from None
    limit = len(target) if allow_append else len(target) - 1
    if index < 0 or index > limit:
        raise ValueError(f"list index out of range in JSON pointer: {token!r}")
    return index


def _descend(container: Any, token: str, path: str) -> Any:
    if isinstance(container, dict):
        if token not in container:
            raise ValueError(f"JSON pointer {path!r} traverses a missing key: {token!r}")
        return container[token]
    if isinstance(container, list):
        return container[_list_index(container, token, allow_append=False)]
    raise ValueError(f"JSON pointer {path!r} traverses a non-container at {token!r}")


class ShadowStore:
    """A replayed copy of the Inspect store data for one sample."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._seeded = False

    def seed(self, env_state_dump: dict) -> None:
        """Install the day-0 `EnvState` (an `EnvState.model_dump(mode="json")`) as the base.

        Deep-copied so later patches never mutate the caller's dict (the emitter builds this
        once through the env core and may hold on to it).
        """
        self._data = {ENV_STATE_KEY: deepcopy(env_state_dump)}
        self._seeded = True

    def apply(self, changes: list[JsonChange]) -> None:
        """Apply one `StoreEvent`'s changes, in order, to the shadow data."""
        if not self._seeded:
            raise ValueError(
                "ShadowStore.apply() called before seed(): store-event changes are nested "
                "pointers into an EnvState that must already exist -- call seed(env_state_dump) "
                "with the day-0 EnvState first"
            )
        for change in changes:
            self._apply_one(change)

    def _apply_one(self, change: JsonChange) -> None:
        if change.op not in _SUPPORTED_OPS:
            raise ValueError(
                f"shadow store cannot honor JSON-Patch op {change.op!r} "
                f"(supported: {', '.join(_SUPPORTED_OPS)}) at path {change.path!r}"
            )
        tokens = _parse_pointer(change.path)
        container: Any = self._data
        for token in tokens[:-1]:
            container = _descend(container, token, change.path)
        token = tokens[-1]
        # Values come from the log/diff; copy so no two slots ever alias one object.
        value = deepcopy(change.value)

        if isinstance(container, list):
            index = _list_index(container, token, allow_append=change.op == "add")
            if change.op == "add":
                container.insert(index, value)
            elif change.op == "replace":
                container[index] = value
            else:
                container.pop(index)
        elif isinstance(container, dict):
            if change.op == "remove":
                if token not in container:
                    raise ValueError(f"JSON pointer {change.path!r} removes a missing key")
                del container[token]
            elif change.op == "replace" and token not in container:
                raise ValueError(f"JSON pointer {change.path!r} replaces a missing key")
            else:
                container[token] = value
        else:
            raise ValueError(
                f"JSON pointer {change.path!r} targets a non-container at {token!r}"
            )

    def env_state(self) -> EnvState | None:
        """The reconstructed `EnvState`, or None when the store holds no state yet.

        Validation is deliberately un-caught: a patch stream that no longer parses as an
        EnvState is a broken reconstruction, and the feed must fail loudly rather than emit
        snapshots from half-valid data.
        """
        raw = self._data.get(ENV_STATE_KEY)
        if raw is None:
            return None
        return EnvState.model_validate(raw)

    def raw(self) -> dict:
        """The live shadow data (not a copy) -- other store keys live here too."""
        return self._data
