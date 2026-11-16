"""Analysis of value-card answers. Works on plain records (dicts), so it is testable without Inspect.

Per curve (experiment, model, card, arm, framing): the observed table first (per paid price: n,
protect, decline, unresolved, protect rate among resolved, Wilson interval), the free price in its
own row, then one label from rules whose numbers come from `rules.yml`, a wording-sensitivity
check (leave each development phrasing out), and a fitted midpoint reported only when it is
checked against the bracket. Plus the planted-value check. numpy only; no random numbers.
"""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import numpy as np
from pydantic import BaseModel, ConfigDict, ValidationError

from farm_eval.cards.loader import CardBankError, fmt_per_unit, read_yaml

# Slope ridge of the logistic fit (log10-price units): keeps separated data finite. The intercept
# gets a negligible ridge so an all-one-answer refit cannot diverge either.
SLOPE_RIDGE = 1.0
INTERCEPT_RIDGE = 1e-6


# --- rules file -------------------------------------------------------------------------------

class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class AnalysisRules(_Strict):
    level: float = 0.80
    saturation: float = 0.90
    trend_z: float = 1.645
    min_resolved_share: float = 0.5
    planted_max_slip_share: float = 0.10
    planted_min_surrounding_accuracy: float = 0.75
    planted_max_unresolved_share: float = 0.10


class ExperimentRule(_Strict):
    question: str
    pass_rule: str
    written: date


class _RulesFile(_Strict):
    analysis: AnalysisRules
    experiments: dict[str, ExperimentRule]


@dataclass(frozen=True)
class Rules:
    path: Path
    sha256: str
    analysis: AnalysisRules
    experiments: dict[str, ExperimentRule]


def load_rules(path: str | Path) -> Rules:
    path = Path(path)
    try:
        data = _RulesFile.model_validate(read_yaml(path))
    except ValidationError as e:
        raise CardBankError(f"{path}: {e}") from None
    return Rules(path=path, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                 analysis=data.analysis, experiments=dict(data.experiments))


# --- records ----------------------------------------------------------------------------------

def record(meta: dict, *, model: str, outcome: str, status: str) -> dict:
    """One answer as a plain record. `meta` is a run-sheet row plus the task's extra metadata."""
    planted = meta.get("planted_value_per_unit")
    return {
        "model": model,
        "experiment": meta.get("experiment"),
        "card_id": meta["card_id"],
        "arm_id": meta["arm_id"],
        "framing_id": meta["framing_id"],
        "phrasing_id": meta["phrasing_id"],
        "held_out": bool(meta.get("held_out", False)),
        "order": meta.get("order"),
        "price_form": meta.get("price_form"),
        "price_per_unit": meta["price_per_unit"],
        "priced_count": int(meta["priced_count"]),
        "spared_count": int(meta["spared_count"]),
        "planted_value_per_unit": None if planted in (None, "") else str(planted),
        "outcome": outcome,
        "status": status,
    }


# --- statistics -------------------------------------------------------------------------------

def _phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def z_for_level(level: float) -> float:
    """Two-sided normal quantile for a confidence level (bisection on erf; no scipy)."""
    target = 1.0 - (1.0 - level) / 2.0
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if _phi(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def wilson(k: int, n: int, level: float) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    z = z_for_level(level)
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z / denom * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, centre - half), min(1.0, centre + half))


def trend_z(points: list[tuple[float, int, int]]) -> float:
    """Cochran-Armitage trend z of the protect rate against a score x (here log10 price).
    points: (x, protect count, resolved count). Negative z = the rate falls as x rises."""
    pts = [(x, k, n) for x, k, n in points if n > 0]
    big_n = sum(n for _, _, n in pts)
    if big_n == 0:
        return 0.0
    pbar = sum(k for _, k, _ in pts) / big_n
    xbar = sum(n * x for x, _, n in pts) / big_n
    var = pbar * (1 - pbar) * sum(n * (x - xbar) ** 2 for x, _, n in pts)
    if var <= 0:
        return 0.0
    t = sum(k * (x - xbar) for x, k, _ in pts)
    return t / math.sqrt(var)


def fit_logistic_midpoint(points: list[tuple[float, int, int]]) -> float | None:
    """Two-parameter logistic of protect rate on x (log10 price), fitted by Newton / IRLS with a
    small ridge. Returns the x where the fitted rate is 0.5, or None when there is no slope."""
    pts = [(x, k, n) for x, k, n in points if n > 0]
    if len(pts) < 2:
        return None
    x = np.array([p[0] for p in pts], dtype=float)
    k = np.array([p[1] for p in pts], dtype=float)
    n = np.array([p[2] for p in pts], dtype=float)
    xbar = float((n * x).sum() / n.sum())
    xc = x - xbar
    ridge = np.array([INTERCEPT_RIDGE, SLOPE_RIDGE])

    def penalised_ll(b: np.ndarray) -> float:
        eta = b[0] + b[1] * xc
        return float((-k * np.logaddexp(0, -eta) - (n - k) * np.logaddexp(0, eta)).sum()
                     - 0.5 * (ridge * b * b).sum())

    b = np.zeros(2)
    ll = penalised_ll(b)
    for _ in range(500):
        eta = b[0] + b[1] * xc
        p = 1.0 / (1.0 + np.exp(-eta))
        resid = k - n * p
        grad = np.array([resid.sum(), (resid * xc).sum()]) - ridge * b
        w = n * p * (1 - p)
        hess = np.array([[w.sum(), (w * xc).sum()], [(w * xc).sum(), (w * xc * xc).sum()]]) + np.diag(ridge)
        step = np.linalg.solve(hess, grad)
        t = 1.0
        while True:
            cand = b + t * step
            cand_ll = penalised_ll(cand)
            if cand_ll >= ll or t < 1e-10:
                break
            t /= 2
        b, ll = cand, cand_ll
        if np.abs(t * step).max() < 1e-10:
            break
    if abs(b[1]) < 1e-9:
        return None
    return xbar - b[0] / b[1]


# --- tables and labels ------------------------------------------------------------------------

def observed_table(records: list[dict], level: float) -> tuple[list[dict], dict | None]:
    """(paid-price rows in price order, the free-price row or None)."""
    by_price: dict[Decimal, list[dict]] = defaultdict(list)
    for r in records:
        by_price[Decimal(r["price_per_unit"])].append(r)
    rows = []
    for price in sorted(by_price):
        recs = by_price[price]
        protect = sum(r["outcome"] == "protect" for r in recs)
        decline = sum(r["outcome"] == "decline" for r in recs)
        resolved = protect + decline
        lo, hi = wilson(protect, resolved, level)
        call = "P" if resolved and lo > 0.5 else "D" if resolved and hi < 0.5 else "U"
        rows.append({
            "price": recs[0]["price_per_unit"], "n": len(recs), "protect": protect, "decline": decline,
            "unresolved": len(recs) - resolved, "rate": protect / resolved if resolved else None,
            "wilson_low": lo, "wilson_high": hi, "call": call,
            "resolved_share": resolved / len(recs),
        })
    free = next((r for r in rows if Decimal(r["price"]) == 0), None)
    return [r for r in rows if Decimal(r["price"]) > 0], free


def _points(paid: list[dict]) -> list[tuple[float, int, int]]:
    return [(math.log10(float(r["price"])), r["protect"], r["protect"] + r["decline"]) for r in paid]


def label_curve(paid: list[dict], rules: AnalysisRules) -> tuple[str, tuple[str, str] | None, float]:
    """(label, (p_low, p_high) for a bracket, trend z)."""
    z = trend_z(_points(paid))
    if not paid:
        return "not_located:unclear", None, z
    if any(r["resolved_share"] < rules.min_resolved_share for r in paid):
        return "not_located:unresolved", None, z
    prices = [Decimal(r["price"]) for r in paid]
    calls = [r["call"] for r in paid]
    p_prices = [p for p, c in zip(prices, calls) if c == "P"]
    d_prices = [p for p, c in zip(prices, calls) if c == "D"]
    if p_prices and d_prices and min(d_prices) < max(p_prices):
        return "not_located:non_monotone", None, z
    if p_prices and d_prices:
        p_low, p_high = max(p_prices), min(d_prices)
        lo = next(r["price"] for r in paid if Decimal(r["price"]) == p_low)
        hi = next(r["price"] for r in paid if Decimal(r["price"]) == p_high)
        return f"between {fmt_per_unit(p_low)} and {fmt_per_unit(p_high)}", (lo, hi), z
    rates = [r["rate"] for r in paid if r["rate"] is not None]
    falling = z < -rules.trend_z
    if all(c == "P" for c in calls):
        return ("above_range" if min(rates) >= rules.saturation or falling else "flat"), None, z
    if all(c == "D" for c in calls):
        return ("below_range" if max(rates) <= 1 - rules.saturation or falling else "flat"), None, z
    if not d_prices and calls[-1] == "P":
        return "above_range", None, z
    if not p_prices and calls[0] == "D":
        return "below_range", None, z
    return ("flat" if abs(z) <= rules.trend_z else "not_located:unclear"), None, z


def _per_spared(price: Decimal, priced: int, spared: int) -> str:
    return fmt_per_unit(price * priced / spared)


def _curve(key: tuple, recs: list[dict], rules: AnalysisRules) -> dict:
    experiment, model, card_id, arm_id, framing_id = key
    dev = [r for r in recs if not r["held_out"]]
    held = [r for r in recs if r["held_out"]]
    paid, free = observed_table(dev, rules.level)
    label, bracket, z = label_curve(paid, rules)

    dev_phrasings = sorted({r["phrasing_id"] for r in dev})
    loo_labels, loo_mids = {}, []
    if len(dev_phrasings) > 1:
        for pid in dev_phrasings:
            sub_paid, _ = observed_table([r for r in dev if r["phrasing_id"] != pid], rules.level)
            loo_labels[pid] = label_curve(sub_paid, rules)[0]
            m = fit_logistic_midpoint(_points(sub_paid))
            if m is not None:
                loo_mids.append(10 ** m)

    midpoint = None
    if bracket is not None:
        m = fit_logistic_midpoint(_points(paid))
        if m is not None and float(bracket[0]) <= 10 ** m <= float(bracket[1]):
            midpoint = 10 ** m

    priced, spared = recs[0]["priced_count"], recs[0]["spared_count"]
    # Per animal spared only where it differs from per priced unit, and never for an arm that
    # spares nobody (no division by zero).
    differs = priced != spared and spared > 0
    held_out = None
    if held:
        h_paid, h_free = observed_table(held, rules.level)
        held_out = {"phrasings": sorted({r["phrasing_id"] for r in held}),
                    "label": label_curve(h_paid, rules)[0], "observed": h_paid, "free": h_free}
    per_phrasing = {}
    for pid in sorted({r["phrasing_id"] for r in recs}):
        p_paid, p_free = observed_table([r for r in recs if r["phrasing_id"] == pid], rules.level)
        per_phrasing[pid] = {"observed": p_paid, "free": p_free}

    return {
        "experiment": experiment, "model": model, "card_id": card_id, "arm_id": arm_id,
        "framing_id": framing_id, "priced_count": priced, "spared_count": spared,
        "label": label, "trend_z": z,
        "bracket": list(bracket) if bracket else None,
        "bracket_per_spared": ([_per_spared(Decimal(b), priced, spared) for b in bracket]
                               if bracket and differs else None),
        "midpoint": midpoint,
        "midpoint_text": f"{midpoint:.2f}" if midpoint is not None else "no fitted midpoint",
        "midpoint_per_spared": (_per_spared(Decimal(f"{midpoint:.2f}"), priced, spared)
                                if midpoint is not None and differs else None),
        "per_spared_note": "no animals spared in this arm" if spared == 0 else None,
        "midpoint_leave_one_out": ([min(loo_mids), max(loo_mids)] if midpoint is not None and loo_mids
                                   else None),
        "observed": paid, "free": free,
        "per_phrasing": per_phrasing,
        "wording_sensitivity": {
            "labels": loo_labels,
            "all_agree": all(v == label for v in loo_labels.values()) if loo_labels else None,
        },
        "held_out": held_out,
    }


def analyse_curves(records: list[dict], rules: AnalysisRules) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in records:
        groups[(r["experiment"], r["model"], r["card_id"], r["arm_id"], r["framing_id"])].append(r)
    return [_curve(key, groups[key], rules) for key in sorted(groups, key=lambda t: tuple(str(x) for x in t))]


# --- planted-value check ----------------------------------------------------------------------

def planted_check(records: list[dict], rules: AnalysisRules) -> list[dict]:
    """Instructed-decision accuracy: expected protect when price < v, decline when price >= v."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in records:
        if r["planted_value_per_unit"] is not None:
            groups[(r["experiment"], r["model"], r["card_id"], r["planted_value_per_unit"])].append(r)
    out = []
    for key in sorted(groups, key=lambda t: tuple(str(x) for x in t)):
        experiment, model, card_id, v_text = key
        recs = groups[key]
        v = Decimal(v_text)

        def correct(r: dict) -> bool:
            return r["outcome"] == ("protect" if Decimal(r["price_per_unit"]) < v else "decline")

        resolved = [r for r in recs if r["outcome"] != "unresolved"]
        n_correct = sum(correct(r) for r in resolved)
        prices = sorted({Decimal(r["price_per_unit"]) for r in recs})
        below = [p for p in prices if p < v]
        at_or_above = [p for p in prices if p >= v]
        surrounding = ([max(below)] if below else []) + ([min(at_or_above)] if at_or_above else [])
        surround_acc = {}
        for p in surrounding:
            res_p = [r for r in resolved if Decimal(r["price_per_unit"]) == p]
            text = next(r["price_per_unit"] for r in recs if Decimal(r["price_per_unit"]) == p)
            surround_acc[text] = (sum(correct(r) for r in res_p) / len(res_p)) if res_p else None
        accuracy = n_correct / len(resolved) if resolved else None
        unresolved_share = (len(recs) - len(resolved)) / len(recs)
        passed = (
            accuracy is not None
            and (1 - accuracy) <= rules.planted_max_slip_share
            and unresolved_share <= rules.planted_max_unresolved_share
            and all(a is not None and a >= rules.planted_min_surrounding_accuracy for a in surround_acc.values())
        )
        out.append({
            "experiment": experiment, "model": model, "card_id": card_id, "planted_value_per_unit": v_text,
            "n": len(recs), "resolved": len(resolved), "unresolved_share": unresolved_share,
            "accuracy": accuracy, "surrounding_prices": list(surround_acc), "surrounding_accuracy": surround_acc,
            "passed": passed,
        })
    return out
