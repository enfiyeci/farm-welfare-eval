"""Section 7: the report over Inspect logs, cost per call, and the dry run."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from inspect_ai import eval as inspect_eval

from farm_eval.card_task import card_task
from farm_eval.cards.loader import CardBankError, load_bank
from farm_eval.cards.report import MADE_UP, _usage_summary, build_report, write_report
from farm_eval.cards.runsheet import build_rows, load_experiments, write_sheet
from farm_eval.report.cost import load_prices

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures" / "bank"
REAL = REPO_ROOT / "schedule" / "cards"
PRICES = REPO_ROOT / "scripts" / "model_prices.yml"


def _run(tmp_path, exp_id, responder, cards_dir=FIX, sheet=None):
    if sheet is None:
        sheet = tmp_path / f"{exp_id}.csv"
        write_sheet(build_rows(load_bank(cards_dir), load_experiments(cards_dir / "experiments.yml"), exp_id), sheet)
    task = card_task(sheet=str(sheet), cards_dir=str(cards_dir), allow_draft=True, responder=responder)
    log = inspect_eval(task, model="mockllm/model", display="none", log_dir=str(tmp_path / "logs"))[0]
    assert log.status == "success"
    return tmp_path / "logs"


def test_report_on_a_scripted_run_is_labelled_made_up(tmp_path):
    logs = _run(tmp_path, "FX_curves", "threshold_2.30")
    rep = build_report(logs, FIX / "rules.yml", PRICES)
    write_report(rep, tmp_path / "out")
    md = (tmp_path / "out" / "results.md").read_text()
    js = (tmp_path / "out" / "results.json").read_text()
    assert md.startswith(f"**{MADE_UP}**")
    assert json.loads(js)["notice"] == MADE_UP
    assert js.lstrip("{\n ").startswith('"notice"')
    curve = rep["experiments"]["FX_curves"]["curves"][0]
    assert curve["model"] == "scripted:threshold_2.30"
    assert curve["label"] == "between $1.50 and $3.50"
    assert rep["rules_sha256"] in md
    for key in ("level", "saturation", "trend_z", "min_resolved_share"):
        assert f"- {key}: " in md
    assert "Fixture curve check on made-up answers." in md
    assert rep["usage"]["scripted:threshold_2.30"]["calls"] == 140
    assert rep["usage"]["scripted:threshold_2.30"]["cost"] is None


def test_report_refuses_an_experiment_without_a_rules_entry(tmp_path):
    logs = _run(tmp_path, "FX_small", "always_protect")
    rules = tmp_path / "rules.yml"
    rules.write_text((FIX / "rules.yml").read_text().split("  FX_small:")[0])
    with pytest.raises(CardBankError, match="FX_small"):
        build_report(logs, rules, PRICES)


def test_report_refuses_the_same_row_twice_for_one_model(tmp_path):
    # A sheet rerun into the same log folder would double every count without this refusal.
    _run(tmp_path, "FX_small", "always_protect")
    logs = _run(tmp_path, "FX_small", "always_protect")
    with pytest.raises(CardBankError, match="more than once"):
        build_report(logs, FIX / "rules.yml", PRICES)


def test_mockllm_run_of_e7_reports_unresolved_and_config(tmp_path):
    logs = _run(tmp_path, "E7_noise_floor", None, cards_dir=REAL, sheet=REAL / "runsheets" / "E7_noise_floor.csv")
    rep = build_report(logs, REAL / "rules.yml", PRICES)
    e7 = rep["experiments"]["E7_noise_floor"]
    assert e7["pass_rule"] == "none: descriptive only; measures repeat variation and cost per call"
    assert e7["statuses"] == {"missing": 80}
    assert e7["curves"][0]["label"] == "not_located:unresolved"
    assert rep["made_up"] is True
    assert rep["usage"]["mockllm/model"]["calls"] == 80
    assert rep["usage"]["mockllm/model"]["stop_reasons"] == {"stop": 80}
    assert rep["runs"][0]["generate_config"]["max_tokens"] == 2000
    assert rep["runs"][0]["generate_config"]["max_retries"] == 3
    # per animal spared differs from per pullet on this card: 124,000 priced, 121,500 spared
    assert e7["curves"][0]["priced_count"] == 124000 and e7["curves"][0]["spared_count"] == 121500


def test_cost_per_call_from_the_price_table():
    prices = load_prices(PRICES)
    rows = [{"fresh_input": 1000, "cached_input": 0, "cache_write": 0, "input": 1000, "output": 100,
             "reasoning": 0, "stop_reason": "stop", "error": False, "price_model": "anthropic/claude-haiku-4-5"}] * 4
    u = _usage_summary("anthropic/claude-haiku-4-5", rows, prices)
    (rate,) = u["cost"]["rates"]
    assert rate["per_call_mean"] == pytest.approx((1000 * 1 + 100 * 5) / 1e6)
    assert rate["total"] == pytest.approx(4 * 0.0015)
    assert u["input_tokens"] == {"mean": 1000, "max": 1000}


def test_dry_run_prints_the_expected_labels():
    out = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "cards_dry_run.py")],
                         check=True, cwd=REPO_ROOT, capture_output=True, text=True).stdout
    lines = set(out.splitlines())
    assert MADE_UP in lines
    assert "label scripted:always_protect: above_range; fitted midpoint: no fitted midpoint" in lines
    assert "label scripted:never_protect: below_range; fitted midpoint: no fitted midpoint" in lines
    assert any(l.startswith("label scripted:threshold_2.30: between $1.50 and $3.50; fitted midpoint: ")
               and "no fitted" not in l for l in lines)
    assert any(l.startswith("label scripted:noisy_threshold_2.30: between $1.50 and $3.50") for l in lines)
    assert "label scripted:malformed_mix: not_located:unresolved; fitted midpoint: no fitted midpoint" in lines
    assert "label mockllm/model: not_located:unresolved; fitted midpoint: no fitted midpoint" in lines
    flat = next(l for l in lines if l.startswith("label scripted:flat_60: "))
    assert flat.split(": ")[1].split(";")[0] in ("flat", "not_located:unclear")
    assert "no fitted midpoint" in flat
    for v in ("0", "0.40", "2.30"):
        assert f"planted scripted:planted_follower v={v}: pass" in lines
    assert "planted scripted:always_protect v=0: fail" in lines
    assert "planted scripted:never_protect v=2.30: fail" in lines
