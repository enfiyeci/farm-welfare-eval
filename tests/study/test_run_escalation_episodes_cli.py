import subprocess
import sys
from farm_eval.study.results import read_episodes_jsonl


def test_dry_run_writes_episodes(tmp_path):
    out = tmp_path / "x.jsonl"
    p = subprocess.run(
        [
            sys.executable,
            "scripts/run_escalation_episodes.py",
            "--arm",
            "same",
            "--episodes",
            "2",
            "--max-rounds",
            "4",
            "--species",
            "hen",
            "--dry-run",
            "--quiet",
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, p.stderr
    assert len(read_episodes_jsonl(out)) == 2
