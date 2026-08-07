**Findings**

Important: `farm_eval/env/model/integrate.py:90` computes `effective_fte_per_100k(state, params)` inside the per-house loop, while `farm_eval/env/model/integrate.py:183` mutates `state.world.bird_count` later in that same loop. With `staffing_fte` set, earlier houses are costed against one complex total and later houses against a post-mortality total, so total labor can exceed the absolute FTE setting and becomes house-order dependent during mortality/depopulation days. Compute the effective ratio once per simulated day before iterating houses.

Important: `farm_eval/env/episode.py:375` and `farm_eval/adapter/tools/controls.py:34` make `0`/omitted `shift_hours` mean “leave unchanged,” while `None` is rejected by `float(raw_shift)` at `episode.py:378`. After any successful non-default `shift_hours`, the agent has no way to restore `WorldState.staffing_shift_hours` to `None`, even though `economics.py:30` defines `None` as the params-default sentinel. It can guess today’s default numeric value, but it cannot reset to “use params default.”

Minor: `tests/env/test_staffing_lever.py:108` uses exactly `100_000` birds and `staffing_fte = 2 * default`, so that unit test would also pass for an inverted conversion formula. Add a non-100k case, e.g. `250_000` birds with `staffing_fte = 2 * default * 250_000 / 100_000`, and assert the effective ratio is `2 * default`.

No Critical findings. I did not modify files. I also could not run Python-level verification here because the active shell lacks the repo dependencies (`pydantic` import failed).