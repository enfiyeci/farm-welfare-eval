#!/usr/bin/env python
"""Generate corpus/history.yml candidate content from the calibrated production model, so the
archive is numerically consistent with the live substrate (world-bible §4 roster ages, §7
canonical month). Run once, review, commit the YAML — the runtime never executes this."""
import yaml
from farm_eval.env.model import ModelParams
from farm_eval.env.model.layers.production import production_step

# House roster at day 0 (corpus/company.yml, world-bible §4). Walk each flock's age BACKWARD
# month by month; months before placement belong to the house's PRIOR flock (left absent here,
# hand-filled in corpus/history.yml).
ROSTER = {"H1": 68.0, "H2": 52.0, "H3": 34.0, "H4": 17.0, "H5": 43.0}  # age_wk at 2025-06-09
MONTHS = [f"2024-{m:02d}" for m in range(6, 13)] + [f"2025-{m:02d}" for m in range(1, 6)]
params = ModelParams()
out = {"flock_monthly": {}, "cop_monthly": {}}
for hid, age0 in ROSTER.items():
    rows = {}
    for i, month in enumerate(reversed(MONTHS)):
        age = age0 - (i + 1) * 4.345
        if age < params.breed_age_wk[0]:
            continue  # pre-lay / prior-flock gap: leave the month absent (honest archive gap)
        hen_day = production_step(age, params)["hen_day_pct"]
        rows[month] = {"age_weeks": round(age, 1), "hen_day_pct": round(hen_day, 1),
                       "mortality_pct_month": 0.5}
    out["flock_monthly"][hid] = dict(sorted(rows.items()))
print(yaml.safe_dump(out, sort_keys=False))
