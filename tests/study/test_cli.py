import sys

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
