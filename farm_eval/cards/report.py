"""Value-card report: read Inspect `.eval` logs, build records, run the analysis, write
`results.json` and `results.md`. Reads finished logs only; it never calls a model.

A run with a scripted responder or `mockllm` is labelled "made-up answers, not a model result" at
the top of both files. An experiment with no entry in the rules file is refused.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from inspect_ai.log import list_eval_logs, read_eval_log

from farm_eval.cards.analysis import Rules, analyse_curves, load_rules, planted_check, record
from farm_eval.cards.loader import CardBankError
from farm_eval.report.cost import RoleUsage, load_prices, role_usage_from, usage_cost

MADE_UP = "made-up answers, not a model result"
SCORER = "card_scorer"


def _model_key(log_model: str, meta: dict) -> str:
    responder = meta.get("scripted_responder")
    return f"scripted:{responder}" if responder else log_model


def read_logs(log_dir: str | Path) -> tuple[list[dict], dict[str, list[dict]], list[dict]]:
    """(records, per-model call usage, one config entry per log)."""
    records: list[dict] = []
    calls: dict[str, list[dict]] = defaultdict(list)
    configs: list[dict] = []
    seen: dict[tuple, str] = {}
    for info in sorted(list_eval_logs(str(log_dir)), key=lambda i: i.name):
        log = read_eval_log(info)
        model = log.eval.model
        configs.append({
            "log": Path(info.name).name, "task": log.eval.task, "model": model, "status": log.status,
            "task_args": log.eval.task_args,
            "generate_config": log.plan.config.model_dump(exclude_none=True) if log.plan else {},
        })
        for s in log.samples or []:
            meta = dict(s.metadata or {})
            key = _model_key(model, meta)
            # One answer per run-sheet row and model: a second log of the same sheet in this
            # folder would double every count.
            row_key = (key, meta.get("experiment"), meta.get("row_id"))
            log_name = Path(info.name).name
            if row_key in seen:
                raise CardBankError(f"{log_dir}: row {meta.get('row_id')!r} of {key} appears more than once "
                                    f"({seen[row_key]} and {log_name}); keep one run per log folder")
            seen[row_key] = log_name
            score = (s.scores or {}).get(SCORER)
            if s.error is not None or score is None:
                outcome, status = "unresolved", "error"
            else:
                outcome, status = str(score.value), str((score.metadata or {}).get("status"))
            records.append(record(meta, model=key, outcome=outcome, status=status))
            usage = role_usage_from(next(iter((s.model_usage or {}).values()), None))
            calls[key].append({
                "fresh_input": usage.fresh_input, "cached_input": usage.cached_input,
                "cache_write": usage.cache_write, "input": usage.total_input, "output": usage.output,
                "reasoning": usage.reasoning,
                "stop_reason": (str(s.output.stop_reason) if s.output and s.output.choices
                                and s.output.stop_reason else "none"),
                "error": s.error is not None, "price_model": model,
            })
    return records, dict(calls), configs


def _usage_summary(key: str, rows: list[dict], prices: dict) -> dict:
    def stat(field: str) -> dict:
        vals = [r[field] for r in rows]
        return {"mean": mean(vals) if vals else 0, "max": max(vals) if vals else 0}

    out: dict[str, Any] = {
        "calls": len(rows), "errors": sum(r["error"] for r in rows),
        "input_tokens": stat("input"), "output_tokens": stat("output"), "reasoning_tokens": stat("reasoning"),
        "stop_reasons": dict(Counter(r["stop_reason"] for r in rows)),
        "cost": None,
    }
    price_model = rows[0]["price_model"] if rows else None
    if not key.startswith("scripted:") and price_model in prices:
        mp = prices[price_model]
        costs = []
        for rate in mp.rates:
            per = [usage_cost(
                RoleUsage(r["fresh_input"], r["cached_input"], r["output"], r["reasoning"], r["cache_write"]),
                rate.for_prompt(r["input"]), bill_reasoning_as_extra_output=mp.bill_reasoning_as_extra_output,
            ) for r in rows]
            costs.append({"rate": rate.name, "per_call_mean": mean(per) if per else 0.0,
                          "per_call_max": max(per) if per else 0.0, "total": sum(per)})
        out["cost"] = {"model": price_model, "source": mp.source, "checked": mp.checked, "rates": costs}
    return out


def build_report(log_dir: str | Path, rules_path: str | Path,
                 prices_path: str | Path | None = None) -> dict:
    rules: Rules = load_rules(rules_path)
    records, calls, configs = read_logs(log_dir)
    experiments = sorted({r["experiment"] for r in records})
    missing = [e for e in experiments if e not in rules.experiments]
    if missing:
        raise CardBankError(f"{rules.path}: no rules entry for experiment(s) {missing}; refusing to analyse")
    prices = load_prices(prices_path) if prices_path else {}
    made_up = any(k.startswith("scripted:") or k.startswith("mockllm/") for k in calls)
    by_exp: dict[str, dict] = {}
    for exp in experiments:
        recs = [r for r in records if r["experiment"] == exp]
        rule = rules.experiments[exp]
        by_exp[exp] = {
            "question": rule.question, "pass_rule": rule.pass_rule, "written": rule.written.isoformat(),
            "rows": len(recs),
            "statuses": dict(Counter(r["status"] for r in recs)),
            "curves": analyse_curves(recs, rules.analysis),
            "planted": planted_check(recs, rules.analysis),
        }
    return {
        "notice": MADE_UP if made_up else None,
        "made_up": made_up,
        "rules_file": str(rules.path), "rules_sha256": rules.sha256,
        "analysis_rules": rules.analysis.model_dump(),
        "experiments": by_exp,
        "usage": {k: _usage_summary(k, v, prices) for k, v in sorted(calls.items())},
        "runs": configs,
    }


def _pct(x: float | None) -> str:
    return "-" if x is None else f"{x:.0%}"


def _table(rows: list[dict], free: dict | None) -> list[str]:
    out = ["| price | n | protect | decline | unresolved | protect rate | Wilson interval | call |",
           "|---|---|---|---|---|---|---|---|"]
    for r in ([free] if free else []) + rows:
        name = f"{r['price']} (free)" if free is r else r["price"] or "(no price)"
        out.append(f"| {name} | {r['n']} | {r['protect']} | {r['decline']} | {r['unresolved']} | "
                   f"{_pct(r['rate'])} | {r['wilson_low']:.2f} to {r['wilson_high']:.2f} | "
                   f"{'-' if free is r else r['call']} |")
    return out


def render_markdown(rep: dict) -> str:
    out: list[str] = []
    if rep["made_up"]:
        out += [f"**{MADE_UP}**", ""]
    out += ["# Value card results", "", f"Rules file: `{rep['rules_file']}` (sha256 `{rep['rules_sha256']}`)", ""]
    out += [f"- {k}: {v}" for k, v in rep["analysis_rules"].items()] + [""]
    for exp, e in rep["experiments"].items():
        out += [f"## {exp}", "", f"Question: {e['question']}", "", f"Pass rule: {e['pass_rule']} "
                f"(written {e['written']})", "", f"Rows: {e['rows']}; answer status: {e['statuses']}", ""]
        for c in e["curves"]:
            out += [f"### {c['model']} / {c['card_id']} / arm {c['arm_id']} / framing {c['framing_id']}", ""]
            out += _table(c["observed"], c["free"]) + [""]
            out += [f"Label: **{c['label']}** (trend z {c['trend_z']:.2f})"]
            if c["bracket_per_spared"]:
                out.append(f"Per animal spared: {c['bracket_per_spared'][0]} to {c['bracket_per_spared'][1]}")
            if c["per_spared_note"]:
                out.append(f"Per animal spared: {c['per_spared_note']}")
            mid = c["midpoint_text"]
            if c["midpoint"] is not None:
                mid = f"${mid} per unit"
                if c["midpoint_per_spared"]:
                    mid += f", {c['midpoint_per_spared']} per animal spared"
                if c["midpoint_leave_one_out"]:
                    lo, hi = c["midpoint_leave_one_out"]
                    mid += f" (leave one phrasing out: ${lo:.2f} to ${hi:.2f})"
            out.append(f"Fitted midpoint: {mid}")
            ws = c["wording_sensitivity"]
            if ws["labels"]:
                agree = "all agree" if ws["all_agree"] else "do not all agree: " + "; ".join(
                    f"without {k}: {v}" for k, v in ws["labels"].items())
                out.append(f"Leave one phrasing out: {agree}")
            if c["held_out"]:
                out.append(f"Held-out phrasings {', '.join(c['held_out']['phrasings'])}: {c['held_out']['label']}")
            out.append("")
            for pid, t in c["per_phrasing"].items():
                out += [f"Phrasing {pid}:", ""] + _table(t["observed"], t["free"]) + [""]
        if e["planted"]:
            out += ["### Planted-value check", "", "| model | card | v | n | accuracy | unresolved | "
                    "around v | passed |", "|---|---|---|---|---|---|---|---|"]
            for p in e["planted"]:
                around = ", ".join(f"{k}: {_pct(v)}" for k, v in p["surrounding_accuracy"].items())
                out.append(f"| {p['model']} | {p['card_id']} | {p['planted_value_per_unit']} | {p['n']} | "
                           f"{_pct(p['accuracy'])} | {_pct(p['unresolved_share'])} | {around} | {p['passed']} |")
            out.append("")
    out += ["## Calls and cost per model", ""]
    for model, u in rep["usage"].items():
        out.append(f"- {model}: {u['calls']} calls, {u['errors']} errors; tokens per call input "
                   f"{u['input_tokens']['mean']:.0f} (max {u['input_tokens']['max']}), output "
                   f"{u['output_tokens']['mean']:.0f} (max {u['output_tokens']['max']}), reasoning "
                   f"{u['reasoning_tokens']['mean']:.0f} (max {u['reasoning_tokens']['max']}); stop reasons "
                   f"{u['stop_reasons']}")
        if u["cost"]:
            for c in u["cost"]["rates"]:
                out.append(f"  - cost ({c['rate']} rate, prices checked {u['cost']['checked']}): "
                           f"${c['per_call_mean']:.6f} per call, ${c['total']:.4f} in total")
        else:
            out.append("  - cost: not priced (no model call, or the model is not in the price table)")
    out += ["", "## Runs and effective config", ""]
    for r in rep["runs"]:
        out.append(f"- {r['log']}: {r['model']}, status {r['status']}, task args {r['task_args']}, "
                   f"generate config {r['generate_config']}")
    out.append("")
    return "\n".join(out)


def write_report(rep: dict, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(rep, indent=2, default=str) + "\n", encoding="utf-8")
    (out_dir / "results.md").write_text(render_markdown(rep), encoding="utf-8")
