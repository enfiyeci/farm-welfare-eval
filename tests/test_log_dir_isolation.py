"""G1: pytest runs never write Inspect logs into the repo's `logs/`.

396 of the 397 files in the main checkout's `logs/` were mockllm logs left by the test suite, which
buried the one real run. `tests/conftest.py` points INSPECT_LOG_DIR at a per-session temp dir, so
an `inspect_eval` call that passes no `log_dir` writes there; a test that passes its own `log_dir`
still wins.
"""
import os
from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_inspect_log_dir_points_outside_the_repo():
    log_dir = Path(os.environ["INSPECT_LOG_DIR"]).resolve()
    assert not log_dir.is_relative_to(REPO_ROOT), log_dir


def test_eval_without_log_dir_writes_to_the_session_dir_not_repo_logs():
    log = inspect_eval(Task(dataset=[Sample(input="hi")]), model="mockllm/model", display="none")[0]
    written = Path(log.location).resolve()
    assert written.is_relative_to(Path(os.environ["INSPECT_LOG_DIR"]).resolve())
    assert not written.is_relative_to(REPO_ROOT)


def test_an_explicit_log_dir_still_wins(tmp_path):
    log = inspect_eval(Task(dataset=[Sample(input="hi")]), model="mockllm/model", display="none",
                       log_dir=str(tmp_path / "mine"))[0]
    assert Path(log.location).resolve().is_relative_to((tmp_path / "mine").resolve())
