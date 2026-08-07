"""The delegated/agentic runner (2026-08-06 delegated-agentic spec §2/§8)."""
import subprocess

import pytest

from farm_eval.study.results import read_jsonl


def test_stated_dry_run_matches_the_constant_cushion_shape(tmp_path, monkeypatch):
    from scripts.run_delegated_ladder import main

    def _forbidden(*args, **kwargs):
        raise AssertionError("real CLI invoked")

    monkeypatch.setattr(subprocess, "run", _forbidden)
    out = tmp_path / "delegated.jsonl"
    assert main(["--interface", "stated", "--dry-run", "--out", str(out)]) == 0
    results = read_jsonl(out)
    by_species = {r.cell.species.value: len(r.rung_records) for r in results}
    assert by_species == {"hen": 7, "shrimp": 5}
    for r in results:
        for rr in r.rung_records:
            assert len(rr.decisions) == 3
            assert rr.agentic is None            # stated arm records no workspace


def test_tool_dry_run_writes_agentic_records(tmp_path, monkeypatch):
    from scripts.run_delegated_ladder import main

    def _forbidden(*args, **kwargs):
        raise AssertionError("real CLI invoked")

    monkeypatch.setattr(subprocess, "run", _forbidden)
    out = tmp_path / "tool.jsonl"
    assert main(["--interface", "tool", "--dry-run", "--out", str(out)]) == 0
    results = read_jsonl(out)
    by_species = {r.cell.species.value: len(r.rung_records) for r in results}
    assert by_species == {"hen": 7, "shrimp": 5}
    for r in results:
        for rr in r.rung_records:
            assert rr.agentic is not None and len(rr.agentic) == 3
            assert all(rec.tool_ran for rec in rr.agentic)
            assert rr.density_step is not None


def test_interface_is_required(tmp_path):
    from scripts.run_delegated_ladder import main

    with pytest.raises(SystemExit):
        main(["--dry-run", "--out", str(tmp_path / "x.jsonl")])


def test_rejects_directory_output(tmp_path):
    from scripts.run_delegated_ladder import main

    assert main(["--interface", "stated", "--dry-run", "--out", str(tmp_path)]) != 0


def test_rejects_non_finite_or_non_positive_cushion(tmp_path):
    from scripts.run_delegated_ladder import main

    out = tmp_path / "x.jsonl"
    for bad in ("nan", "inf", "0"):
        assert main(["--interface", "stated", "--dry-run", "--out", str(out),
                     "--target-cushion", bad]) != 0


def test_recorded_gain_is_each_cells_own_ladder_maximum(tmp_path):
    from scripts.run_constant_cushion_ladder import rungs_for_cell
    from scripts.run_delegated_ladder import main
    from farm_eval.study.cells import Cell, Economics, Scale, StandardBand
    from farm_eval.study.economics import gain_for
    from farm_eval.study.offer import build_offer

    out = tmp_path / "tool.jsonl"
    assert main(["--interface", "tool", "--dry-run", "--out", str(out)]) == 0
    for r in read_jsonl(out):
        cell = Cell(species=r.cell.species, scale=Scale.LARGE,
                    standard=StandardBand.BEYOND, economics=Economics.EQUALIZED)
        expected = max(gain_for(build_offer(cell, rung, 0.0))
                       for rung in rungs_for_cell(cell, 6.0))
        assert r.gain == pytest.approx(expected)
