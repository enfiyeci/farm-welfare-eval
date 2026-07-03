"""D2 -- per-beat EnvState checkpointing (opt-in), for paid-run resilience.

Pilot-hardening: a hard kill (SIGKILL/power loss) mid-paid-episode currently loses the whole run.
When `EpisodeConfig.checkpoint_dir` is set, the solver writes the latest `EnvState` to disk after
every ACTUAL day advancement (natural `end_day` or the forced backstop advance), so a killed run
can be salvaged for partial scoring via `load_checkpoint` + `farm_eval.env.replay.replay_env`.

Design:
  - OFF by default (`checkpoint_dir=None`): zero behavior change, zero files written.
  - One file per beat: `<checkpoint_dir>/<sample_id>/day_<n>.json`, containing
    `{"day": n, "message_count": <int>, "env_state": <EnvState.model_dump(mode="json")>}`.
  - Atomic write-replace: write to a temp file in the SAME directory, then `os.replace` onto the
    final name, so a kill mid-write can never leave a truncated `day_<n>.json` behind.
  - Retention: only the last 3 `day_*.json` per sample are kept, determined by parsing the day
    number out of the filename (never mtime) -- deterministic, wall-clock-free.
  - IO failure policy: a checkpoint write failure must NEVER crash the episode -- that would be
    the resilience feature killing an otherwise-healthy paid run. OS and serialization errors are
    caught, logged as a warning naming the path and error, and swallowed; the episode continues.
    (Surfacing these warnings in run-health reporting is a separate, later task.)
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from farm_eval.env.state import EnvState

logger = logging.getLogger(__name__)

_RETENTION = 3


def _sample_dir_name(sample_id: object) -> str:
    """Coerce an Inspect `TaskState.sample_id` (int | str) to a filesystem-safe directory name."""
    raw = str(sample_id)
    safe = "".join(c if (c.isalnum() or c in ("-", "_", ".")) else "_" for c in raw)
    return safe or "_"


def write_checkpoint(checkpoint_dir: str, sample_id: object, day: int, message_count: int, env_state: EnvState) -> None:
    """Atomically persist a per-beat checkpoint, if `checkpoint_dir` is set.

    Never raises: a write/serialization failure is logged as a warning (naming the path and the
    error) and swallowed, so a checkpointing malfunction can never crash a healthy paid episode.
    Retention keeps only the last 3 `day_*.json` files per sample, ordered by the day number
    parsed from the filename (not mtime, for determinism).
    """
    try:
        sample_dir = Path(checkpoint_dir) / _sample_dir_name(sample_id)
        sample_dir.mkdir(parents=True, exist_ok=True)

        payload = {"day": day, "message_count": message_count, "env_state": env_state.model_dump(mode="json")}
        final_path = sample_dir / f"day_{day}.json"
        tmp_path = sample_dir / f".day_{day}.json.tmp"
        tmp_path.write_text(json.dumps(payload), encoding="utf-8")
        os.replace(tmp_path, final_path)  # atomic on the same filesystem: no partial final file

        _prune_old_checkpoints(sample_dir)
    except OSError as exc:
        logger.warning("checkpoint write failed for day %s at %s: %s", day, checkpoint_dir, exc)
    except (TypeError, ValueError) as exc:  # pragma: no cover - serialization defensiveness
        logger.warning("checkpoint serialization failed for day %s at %s: %s", day, checkpoint_dir, exc)


def _prune_old_checkpoints(sample_dir: Path) -> None:
    files = list(sample_dir.glob("day_*.json"))
    parsed: list[tuple[int, Path]] = []
    for p in files:
        try:
            day_num = int(p.stem.split("_", 1)[1])
        except (IndexError, ValueError):  # pragma: no cover - defensive, shouldn't occur
            continue
        parsed.append((day_num, p))
    parsed.sort(key=lambda pair: pair[0])
    for _, stale_path in parsed[:-_RETENTION]:
        stale_path.unlink(missing_ok=True)


def load_checkpoint(path: str | Path) -> tuple[int, int, EnvState]:
    """Load a checkpoint file, returning (day, message_count, validated EnvState).

    Kept importable without running a solver, for salvage tooling and tests.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["day"], data["message_count"], EnvState.model_validate(data["env_state"])
