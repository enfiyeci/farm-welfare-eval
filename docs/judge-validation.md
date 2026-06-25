# Judge validation (credibility gate)

Welfare scoring is value-laden. Before trusting any cross-model welfare delta from a sweep, the
judge must be shown to track human judgement on a held-out sample of transcripts. This is a hard
gate (spec §15/§16), not a nicety.

## What it measures

`farm_eval/judge/validate.py` reports **Spearman rank correlation (ρ)** per dimension between the
judge's scores and human hand-labels:

```python
from farm_eval.judge.validate import validate_judge

rho = validate_judge(judge_scores, human_labels, dimension_ids)
# {"welfare_decision_quality": 0.81, "integrity_transparency": 0.77, ...}
```

- `judge_scores` / `human_labels`: one `{dimension_id: score}` dict per transcript, paired by index.
- ρ is rank-based, so it rewards the judge ordering transcripts the same way a human would, even if
  the absolute scales differ.

**Target:** Bloom's reported range, ~**0.75–0.86**. Below that, do not trust cross-model deltas —
revise the rubric anchors and/or the grader prompt and re-validate.

## Procedure

1. Sample a held-out set of transcripts (across models and welfare outcomes).
2. Have a human — ideally a vet or welfare expert — label each transcript on the welfare-first
   dimensions, blind to the judge's scores.
3. Run the judge (`welfare_judge` scorer) on the same transcripts.
4. `validate_judge(...)` → ρ per dimension. Report it alongside any sweep results.

## Status

The validation maths is implemented and tested. The held-out labeled set and the harness that
runs the judge over stored `.eval` logs are part of the content/pilot pass (they need an authored
`corpus/` and real rubric anchors first). Until ρ is reported, sweep welfare deltas are indicative
only.
