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


def test_rejects_non_finite_cushion(tmp_path):
    """Codex review 2026-08-06: 'nan <= 0' is False, so without a finiteness check
    a NaN target sails through and produces a completed-looking sweep whose offers
    are all NaN."""
    from scripts.run_constant_cushion_ladder import main
    out = tmp_path / "cushion.jsonl"
    for bad in ("nan", "inf"):
        assert main(["--dry-run", "--out", str(out), "--target-cushion", bad]) != 0


def test_results_record_the_solved_density_per_rung(tmp_path):
    """Codex review 2026-08-06: with the density solved per rung, a results file
    that omits it cannot be truthfully re-rendered. Every rung record must carry
    the density step the model was actually shown."""
    from scripts.run_constant_cushion_ladder import main, rungs_for_cell
    from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand

    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out)]) == 0
    results = read_jsonl(out)
    hen = next(r for r in results if r.cell.species.value == "hen")
    cell = Cell(species=Species.HEN, scale=Scale.LARGE,
                standard=StandardBand.BEYOND, economics=Economics.EQUALIZED)
    expected = [rung.density_step for rung in rungs_for_cell(cell, 6.0)]
    assert [rr.density_step for rr in hen.rung_records] == expected


def test_exits_nonzero_when_output_path_is_a_directory(tmp_path):
    from scripts.run_constant_cushion_ladder import main
    assert main(["--dry-run", "--out", str(tmp_path)]) != 0


def test_recorded_gain_is_each_cells_own_ladder_maximum(tmp_path):
    """Codex review 2026-08-06 rounds 2-3: gain=0.0 made envelope_status label
    every cell 'in_envelope' and transcript headings say '+0%'; a single max
    across BOTH species then mislabeled the lower-gain species. The recorded gain
    is now each cell's OWN ladder maximum — an upper bound for that cell, so the
    envelope classification is conservative per cell."""
    import pytest
    from scripts.run_constant_cushion_ladder import main, rungs_for_cell
    from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
    from farm_eval.study.economics import gain_for
    from farm_eval.study.offer import build_offer

    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out)]) == 0
    results = read_jsonl(out)
    for r in results:
        cell = Cell(species=r.cell.species, scale=Scale.LARGE,
                    standard=StandardBand.BEYOND, economics=Economics.EQUALIZED)
        expected = max(gain_for(build_offer(cell, rung, 0.0))
                       for rung in rungs_for_cell(cell, 6.0))
        assert expected > 0
        assert r.gain == pytest.approx(expected)
        assert r.envelope == "in_envelope"
    # The two species' maxima genuinely differ (~40.8% vs ~61.9%), so a shared
    # value would fail the per-cell assertion above.
    gains = {r.cell.species.value: r.gain for r in results}
    assert gains["hen"] != pytest.approx(gains["shrimp"])


def test_a_species_with_no_feasible_rungs_is_skipped_not_crashed(tmp_path):
    """Codex review 2026-08-06 round 3: at --target-cushion 20 hens retain capped
    rungs but shrimp retains none; the run must complete with the feasible species
    only, not crash inside run_sweep after spending the hen calls."""
    from scripts.run_constant_cushion_ladder import main

    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out), "--target-cushion", "20"]) == 0
    results = read_jsonl(out)
    assert [r.cell.species.value for r in results] == ["hen"]
    assert results[0].rung_records


def test_a_cushion_no_rung_can_reach_fails_loudly(tmp_path):
    """A target above every per-mortality ceiling must not produce an empty,
    completed-looking run."""
    from scripts.run_constant_cushion_ladder import main
    out = tmp_path / "cushion.jsonl"
    assert main(["--dry-run", "--out", str(out), "--target-cushion", "50"]) != 0


def test_datasets_written_before_density_was_recorded_still_read():
    """Every jsonl collected before 2026-08-06 lacks density_step; adding the
    field must not orphan them."""
    from farm_eval.study.results import RungRecord

    old = RungRecord.model_validate({
        "added_mortality_pp": 9.0, "delta_deaths": 100.0,
        "decisions": ["accept"], "responses": ["DECISION: ACCEPT"],
        "accepted": True,
    })
    assert old.density_step is None
