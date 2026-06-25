"""Judge validation (credibility gate, spec §15/§16).

Welfare is value-laden, so cross-model deltas should not be trusted until the judge is shown to
track human (ideally vet/welfare-expert) hand-labels. This reports Spearman rank correlation per
dimension between the judge's scores and the human labels on a held-out transcript sample. Run
before any production sweep; target Bloom's range (~0.75-0.86). See docs/judge-validation.md.
"""

from __future__ import annotations

import numpy as np


def _rankdata(values: np.ndarray) -> np.ndarray:
    """1-based ranks with average ranks for ties (scipy.stats.rankdata equivalent, no scipy dep)."""
    order = np.argsort(values, kind="mergesort")
    sorted_vals = values[order]
    ranks = np.empty(len(values), dtype=float)
    i = 0
    n = len(values)
    while i < n:
        j = i
        while j + 1 < n and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0  # average of the 1-based ranks i+1..j+1
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman_rho(a: list[float], b: list[float]) -> float:
    """Spearman's rank correlation = Pearson correlation of the rank-transformed values."""
    av = np.asarray(a, dtype=float)
    bv = np.asarray(b, dtype=float)
    if av.ndim != 1 or bv.ndim != 1:
        raise ValueError("spearman_rho inputs must be 1-D")
    if av.shape != bv.shape:
        raise ValueError(f"spearman_rho inputs must be the same length: {av.shape} vs {bv.shape}")
    if av.size < 2:
        raise ValueError("spearman_rho needs at least 2 paired observations")
    if not (np.all(np.isfinite(av)) and np.all(np.isfinite(bv))):
        # A NaN/inf label (e.g. a blank human-label cell) must FAIL the gate, not get a manufactured
        # rank (NaN never ties, so it would otherwise slip through as a normal value).
        raise ValueError("spearman_rho inputs must be finite (no NaN/inf)")
    ranks_a = _rankdata(av)
    ranks_b = _rankdata(bv)
    if np.std(ranks_a) == 0 or np.std(ranks_b) == 0:
        # A constant series has undefined correlation; report 0 (no monotonic relationship observable).
        return 0.0
    return float(np.corrcoef(ranks_a, ranks_b)[0, 1])


def validate_judge(
    judge_scores: list[dict], human_labels: list[dict], dimension_ids: list[str]
) -> dict[str, float]:
    """Per-dimension Spearman rho between judge scores and human labels across the labeled sample.
    Each list element is one transcript's {dimension_id: score}."""
    if len(judge_scores) != len(human_labels):
        raise ValueError(
            f"judge_scores and human_labels must be paired: {len(judge_scores)} vs {len(human_labels)}"
        )
    out: dict[str, float] = {}
    for dim in dimension_ids:
        judge = [s[dim] for s in judge_scores]
        human = [s[dim] for s in human_labels]
        out[dim] = spearman_rho(judge, human)
    return out
