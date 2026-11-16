"""Sections 2 and 3: run sheets (built from experiments.yml) and the wording export."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from farm_eval.cards.loader import CardBankError, load_bank
from farm_eval.cards.runsheet import COLUMNS, build_rows, load_experiments, read_sheet, write_sheet
from farm_eval.cards.export import export_markdown, export_all_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL = REPO_ROOT / "schedule" / "cards"
FIX = Path(__file__).resolve().parent / "fixtures" / "bank"
PY = sys.executable


def _rows(exp_id, cards_dir=FIX):
    return build_rows(load_bank(cards_dir), load_experiments(cards_dir / "experiments.yml"), exp_id)


def test_columns_are_the_spec_columns():
    assert COLUMNS == ["row_id", "experiment", "card_id", "arm_id", "phrasing_id", "order", "price_form",
                       "price_per_unit", "framing_id", "repeat", "text_status"]


def test_row_count_is_the_product_of_the_factors():
    assert len(_rows("FX_curves")) == 1 * 1 * 5 * 2 * 2 * 1 * 7 * 1
    assert len(_rows("FX_small")) == 1 * 2 * 2 * 2 * 1 * 1 * 2 * 2


def test_row_ids_unique_and_order_fixed():
    rows = _rows("FX_small")
    ids = [r["row_id"] for r in rows]
    assert len(set(ids)) == len(ids)
    assert rows == _rows("FX_small")
    prices = [r["price_per_unit"] for r in rows if r["arm_id"] == "base" and r["phrasing_id"] == "p1"
              and r["order"] == "protect_a" and r["repeat"] == "1"]
    assert prices == ["1.50", "8.00"]


def test_building_twice_gives_identical_bytes(tmp_path):
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    write_sheet(_rows("FX_curves"), a)
    write_sheet(_rows("FX_curves"), b)
    assert a.read_bytes() == b.read_bytes()
    assert read_sheet(a) == _rows("FX_curves")


def test_text_status_per_row():
    rows = _rows("FX_curves")
    status = {r["phrasing_id"]: r["text_status"] for r in rows}
    assert status["p1"] == "owner_approved"
    assert status["p2"] == "draft"
    planted = _rows("FX_planted")
    assert {r["text_status"] for r in planted} == {"draft"}  # approved p1 under draft framings


def _with_experiment(tmp_path, exp):
    d = tmp_path / "bank"
    d.mkdir()
    for f in FIX.glob("*.yml"):
        (d / f.name).write_text(f.read_text())
    data = yaml.safe_load((d / "experiments.yml").read_text())
    data["experiments"].append(exp)
    (d / "experiments.yml").write_text(yaml.safe_dump(data, sort_keys=False))
    return d


BASE_EXP = {"id": "X", "cards": ["fx_widget"], "arms": ["base"], "phrasings": ["p1"], "orders": ["protect_a"],
            "price_forms": ["unit_first"], "framings": ["fx_agent"], "prices": ["1.50"], "repeats": 1}


def test_missing_price_form_is_a_build_error(tmp_path):
    d = _with_experiment(tmp_path, {**BASE_EXP, "price_forms": ["total_first"]})
    rows = _rows("X", d)  # the fixture card has total_first
    assert len(rows) == 1
    # the real card has no total_first
    exp = {**BASE_EXP, "cards": ["chick_sourcing"], "framings": ["farm_agent"], "price_forms": ["total_first"]}
    with pytest.raises(CardBankError, match="total_first"):
        build_rows(load_bank(REAL), load_experiments_from(exp), "X")


def test_free_price_without_free_sentence_is_a_build_error():
    exp = {**BASE_EXP, "cards": ["chick_sourcing"], "framings": ["farm_agent"], "prices": ["0", "1.50"]}
    with pytest.raises(CardBankError, match="free"):
        build_rows(load_bank(REAL), load_experiments_from(exp), "X")


def test_build_check_skips_sentence_when_body_has_no_slot(tmp_path):
    d = _with_experiment(tmp_path, {**BASE_EXP, "price_forms": ["unit_first", "total_first"], "prices": ["0", "1.50"]})
    card = yaml.safe_load((d / "fx_widget.yml").read_text())
    card["phrasings"][0]["body"] = "Costs in the options.\n\n{option_a}\n{option_b}\n"
    del card["phrasings"][0]["price_sentence"]
    (d / "fx_widget.yml").write_text(yaml.safe_dump(card, sort_keys=False))
    rows = _rows("X", d)
    assert len(rows) == 4
    assert {r["price_form"] for r in rows} == {"unit_first", "total_first"}  # recorded, selects nothing


def test_unknown_arm_or_experiment_is_an_error():
    with pytest.raises(CardBankError, match="nope"):
        build_rows(load_bank(FIX), load_experiments_from({**BASE_EXP, "arms": ["nope"]}), "X")
    with pytest.raises(CardBankError, match="Y"):
        build_rows(load_bank(FIX), load_experiments_from(BASE_EXP), "Y")


def test_a_factor_listed_twice_is_an_error_at_build_time():
    # Without this the sheet is written with repeated row ids and Inspect refuses it at run time.
    with pytest.raises(CardBankError, match="listed twice"):
        build_rows(load_bank(FIX), load_experiments_from({**BASE_EXP, "phrasings": ["p1", "p1"]}), "X")


def test_a_planted_value_on_both_the_framing_and_the_arm_is_an_error_at_build_time():
    exp = {**BASE_EXP, "arms": ["v230"], "framings": ["fx_planted_040"]}
    with pytest.raises(CardBankError, match="both"):
        build_rows(load_bank(FIX), load_experiments_from(exp), "X")


def load_experiments_from(exp):
    from farm_eval.cards.runsheet import ExperimentsFile
    return ExperimentsFile.model_validate({"ladder": ["0", "1.50"], "experiments": [exp]})


def test_balanced_subset_keeps_whole_wording_cells():
    exp = {**BASE_EXP, "phrasings": ["p1", "p2", "p3", "p4"], "orders": ["protect_a", "protect_b"],
           "prices": "ladder", "subset": {"size": 3, "seed": 7}}
    rows = build_rows(load_bank(FIX), load_experiments_from(exp), "X")
    cells = {(r["phrasing_id"], r["order"]) for r in rows}
    assert len(cells) == 3
    for cell in cells:
        assert sorted(r["price_per_unit"] for r in rows if (r["phrasing_id"], r["order"]) == cell) == ["0", "1.50"]
    assert rows == build_rows(load_bank(FIX), load_experiments_from(exp), "X")
    with pytest.raises(CardBankError, match="subset"):
        build_rows(load_bank(FIX), load_experiments_from({**exp, "subset": {"size": 9, "seed": 7}}), "X")


def test_real_e7_sheet_is_built_and_approved():
    rows = _rows("E7_noise_floor", REAL)
    assert len(rows) == 80
    assert {r["text_status"] for r in rows} == {"owner_approved"}
    assert sorted({r["price_per_unit"] for r in rows}) == ["1.50", "8.00"]
    committed = REAL / "runsheets" / "E7_noise_floor.csv"
    assert read_sheet(committed) == rows


def test_build_script_writes_the_same_bytes(tmp_path):
    out = tmp_path / "sheets"
    subprocess.run([PY, str(REPO_ROOT / "scripts" / "cards_build_sheets.py"), "--cards-dir", str(FIX),
                    "--out-dir", str(out), "--experiment", "FX_small"], check=True, cwd=REPO_ROOT)
    expected = tmp_path / "x.csv"
    write_sheet(_rows("FX_small"), expected)
    assert (out / "FX_small.csv").read_bytes() == expected.read_bytes()


# --- export -------------------------------------------------------------------------------------

def test_export_lists_each_distinct_prompt_once(tmp_path):
    rows = _rows("FX_small")  # repeats 2: every prompt appears on two rows
    md = export_markdown(load_bank(FIX), rows, title="FX_small")
    distinct = {(r["card_id"], r["arm_id"], r["phrasing_id"], r["order"], r["price_form"], r["price_per_unit"],
                 r["framing_id"]) for r in rows}
    assert md.count("\n## Prompt ") == len(distinct)
    assert md.count("rows: 2") == len(distinct)
    assert "Take option one for $1,500." in md
    assert md.count("Take option one for $1,500.") == 2  # protect_a and protect_b, base arm, p1


def test_export_script_from_a_sheet(tmp_path):
    sheet, out = tmp_path / "s.csv", tmp_path / "s.md"
    write_sheet(_rows("FX_small"), sheet)
    subprocess.run([PY, str(REPO_ROOT / "scripts" / "cards_export.py"), "--cards-dir", str(FIX),
                    "--sheet", str(sheet), "--out", str(out)], check=True, cwd=REPO_ROOT)
    assert out.read_text() == export_markdown(load_bank(FIX), read_sheet(sheet), title=sheet.name)


def test_export_all_covers_every_phrasing_order_form_and_price():
    from farm_eval.cards.render import render
    bank = load_bank(FIX)
    md = export_all_markdown(bank, ladder=["0", "0.10", "1.50"])
    card = bank.cards["fx_widget"]
    texts = set()
    for arm in card.arms:
        for ph in card.phrasings:
            for order in ("protect_a", "protect_b"):
                for form in ("unit_first", "total_first"):
                    for price in ("0", "0.10", "1.50"):
                        r = render(card, bank.framings["fx_agent"], arm.arm_id, ph.id, order, form, price)
                        texts.add((r.system, r.user))
                        assert r.user in md
    assert md.count("\n## Prompt ") == len(texts)
    real = export_all_markdown(load_bank(REAL), ladder=["0", "1.50"])
    assert "## Not available" in real  # the free price and total_first have no text on the real card
    assert "no total_first price sentence" in real and "`free` price sentence" in real
