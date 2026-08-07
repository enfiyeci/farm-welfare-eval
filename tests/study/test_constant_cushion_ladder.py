"""The constant-cushion runner (2026-08-06 spec §2/§6)."""
import subprocess

import pytest

from farm_eval.study.results import read_jsonl


def test_dry_run_writes_results_without_calling_a_real_model(tmp_path, monkeypatch):
    from scripts.run_constant_cushion_ladder import main

    def _forbidden(*args, **kwargs):
        raise AssertionError("real CLI invoked")

    monkeypatch.setattr(subprocess, "run", _forbidden)
    out = tmp_path / "cushion.jsonl"
    code = main(["--dry-run", "--out", str(out)])
    assert code == 0
    results = read_jsonl(out)
    assert len(results) == 2  # one CellResult per species
    # Hens run the full 7-rung ladder; the 2.5x density cap drops the two
    # deadliest shrimp rungs (they would need +287% / +811% placement).
    by_species = {r.cell.species.value: len(r.rung_records) for r in results}
    assert by_species == {"hen": 7, "shrimp": 5}
    for r in results:
        for rr in r.rung_records:
            assert len(rr.decisions) == 3  # spec: 3 replicates, majority rule


def test_every_rung_carries_the_target_cushion(tmp_path):
    """The whole point of the run: the cushion must be identical on every rung,
    so it can no longer co-vary with mortality."""
    from scripts.run_constant_cushion_ladder import rungs_for_cell
    from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
    from farm_eval.study.economics import survival_cushion_pp
    from farm_eval.study.offer import build_offer

    for species in Species:
        cell = Cell(species=species, scale=Scale.LARGE,
                    standard=StandardBand.BEYOND, economics=Economics.EQUALIZED)
        rungs = rungs_for_cell(cell, target_cushion=6.0)
        assert rungs, species
        for rung in rungs:
            offer = build_offer(cell, rung, 0.0)
            assert survival_cushion_pp(offer) == pytest.approx(6.0)


def test_rejects_non_positive_cushion(tmp_path):
    from scripts.run_constant_cushion_ladder import main
    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out), "--target-cushion", "0"]) != 0


def test_exits_nonzero_when_output_path_is_a_directory(tmp_path):
    from scripts.run_constant_cushion_ladder import main
    assert main(["--dry-run", "--out", str(tmp_path)]) != 0
