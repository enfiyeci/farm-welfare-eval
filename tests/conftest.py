"""Suite-wide test configuration.

G1 (2026-09-30): every `inspect_eval` call that passes no `log_dir` used to write a mockllm log
into `./logs` (Inspect's default), so the repo's `logs/` filled with hundreds of test logs and the
real runs were hard to find. For the whole session INSPECT_LOG_DIR points at a pytest temp dir
instead — overriding any value inherited from the shell, so a test run can never land in a real
run's log dir either. A test that passes its own `log_dir` still wins (Inspect prefers the
argument over the environment variable). Pytest keeps only the last few session temp dirs.
"""

from __future__ import annotations

import pytest


@pytest.fixture(scope="session", autouse=True)
def _inspect_logs_to_session_tmp(tmp_path_factory: pytest.TempPathFactory):
    log_dir = tmp_path_factory.mktemp("inspect-logs")
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("INSPECT_LOG_DIR", str(log_dir))
        yield log_dir
