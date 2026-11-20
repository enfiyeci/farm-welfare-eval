import subprocess

import pytest

import scripts.run_phase1 as cli
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


def test_results_already_written_survive_a_mid_sweep_provider_failure(
        tmp_path, monkeypatch):
    """I1: the real sweep is 384 calls; buffering every result until the end means a
    failure at call 383 loses everything. Each finished cell must already be on disk
    when a later call dies."""
    calls = {"n": 0}
    real_responder = cli._fake_responder

    def flaky(prompt):
        calls["n"] += 1
        if calls["n"] > 8:  # first cell = 4 rungs x 2 replicates = 8 calls
            raise RuntimeError("provider died mid-sweep")
        return real_responder(prompt)

    monkeypatch.setattr(cli, "_fake_responder", flaky)
    out = tmp_path / "surface.jsonl"
    with pytest.raises(RuntimeError, match="died mid-sweep"):
        main(["--dry-run", "--out", str(out), "--limit-cells", "2",
              "--gains", "0.08"])
    assert len(read_jsonl(out)) == 1


def test_rejects_non_positive_gains(tmp_path):
    """I4: '--gains -0.5' renders 'improve unit cycle profit by -50.0%', making
    declining financially superior — the instrument inverted, not degraded."""
    out = tmp_path / "surface.jsonl"
    for bad in ("-0.5", "0"):
        assert main(["--dry-run", "--out", str(out), "--gains", bad]) != 0
        assert not out.exists()


def test_rejects_limit_cells_below_one(tmp_path):
    """I5: '--limit-cells 0' wrote an empty dataset and exited 0."""
    out = tmp_path / "surface.jsonl"
    assert main(["--dry-run", "--out", str(out), "--limit-cells", "0"]) != 0
    assert not out.exists()


def test_rejects_non_finite_gains(tmp_path):
    """Adversarial A1: nan and inf slip past `g <= 0` (nan compares False to
    everything) and would render a 'nan%' financial offer."""
    out = tmp_path / "surface.jsonl"
    for bad in ("nan", "inf"):
        assert main(["--dry-run", "--out", str(out), "--gains", bad]) != 0
        assert not out.exists()


def test_rejects_an_explicitly_empty_gains_list(tmp_path):
    """Straight-review P2: '--gains' with no values (e.g. a shell-expanded empty
    variable) must not silently become the full preregistered ladder and launch
    a full live sweep nobody asked for."""
    out = tmp_path / "surface.jsonl"
    assert main(["--dry-run", "--out", str(out), "--gains"]) != 0
    assert not out.exists()
