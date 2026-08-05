import subprocess

from scripts.run_phase1 import main
from farm_eval.study.results import read_jsonl


def test_dry_run_writes_results_without_calling_a_real_model(tmp_path, monkeypatch):
    out = tmp_path / "surface.jsonl"
    code = main(["--dry-run", "--out", str(out),
                 "--limit-cells", "2", "--gains", "0.08"])
    assert code == 0
    results = read_jsonl(out)
    assert len(results) == 2
    assert all(r.gain == 0.08 for r in results)


def test_exits_nonzero_when_output_path_is_a_directory(tmp_path):
    assert main(["--dry-run", "--out", str(tmp_path)]) != 0


def test_dry_run_never_invokes_the_real_cli(tmp_path, monkeypatch):
    """Guards the `if args.dry_run` branch itself: if it were ever flipped or
    dropped, --dry-run would silently shell out to the real Codex CLI. subprocess.run
    is the only place CodexProvider reaches the outside world, so making it explode
    is a direct test of "the real CLI was never invoked", not an indirect proxy."""
    def _forbidden(*args, **kwargs):
        raise AssertionError("real CLI invoked")

    monkeypatch.setattr(subprocess, "run", _forbidden)
    out = tmp_path / "surface.jsonl"
    code = main(["--dry-run", "--out", str(out), "--limit-cells", "1", "--gains", "0.08"])
    assert code == 0
    assert len(read_jsonl(out)) == 1
