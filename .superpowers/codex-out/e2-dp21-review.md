**Findings**

1. Important: `node_applies` can wrongly include DP21 from an arbitrarily old treatment.
[node_scores.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/node_scores.py:135) only checks `rec.day <= entry.deadline_day`, with no lower bound. For DP21, this means:
```python
entry = LedgerEntry(dp_id="DP21_DRUG_RESIDUE", category="integrity", opened_day=252, deadline_day=280)
actions = [ActionRecord(tool="log_treatment", params={"house_id": "H5", "issue": "colibacillosis"}, day=1)]
```
This makes DP21 applicable, even though a day-1 H5 treatment should not create a day-252 withdrawal decision. The intended valid window appears to be the upstream DPN window, `224..252`, not `(-inf)..280`. The existing tests cover “after deadline” only, not “too early”.

2. Important: `applies_if` silently cannot use `transient_before`.
[node_scores.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/node_scores.py:137) calls `action_matches(..., schedule=None)` and also omits `day`. But [tracker.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/env/tracker.py:81) returns `False` for `transient_before` unless both `schedule` and `day` are present. A future gate like:
```yaml
applies_if: {tool: adjust_setpoint, where: {transient_before: audit, system: ventilation}}
```
would silently exclude the node for every run. That is especially risky because `ActionMatch` documentation explicitly lists `transient_before` as part of the `where` language.

3. Minor: per-node validation still assumes a fixed node set.
[validate.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/farm_eval/judge/validate.py:83) indexes every sample by every `node_id`:
```python
judge = [s[node] for s in judge_node_scores]
```
With conditional DP21, this can now crash:
```python
validate_nodes(
    [{"DP01": 8.0}, {"DP01": 6.0, "DP21_DRUG_RESIDUE": 10.0}],
    [{"DP01": 8.0}, {"DP01": 6.0, "DP21_DRUG_RESIDUE": 9.0}],
    ["DP01", "DP21_DRUG_RESIDUE"],
)
```
The first untreated sample omits DP21, so this raises `KeyError`. Runtime headline aggregation handles variable denominators; this validation helper does not.

4. Minor: the real DP21 test gives false confidence on the important issue guard.
[test_node_applicability.py](/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers/tests/judge/test_node_applicability.py:108) asserts only `tool == log_treatment` and `house_id == H5`. It would still pass if the schedule regressed to:
```yaml
applies_if: {tool: log_treatment, where: {house_id: H5}}
```
which would make unrelated H5 treatments trigger DP21. It should also assert `issue == [colibacillosis, e_coli]` or equivalent.

**Non-Findings**

The headline and breakout aggregation paths do not appear to double-count or divide by zero in normal runs. `welfare_headline` correctly uses the scored dict length and fails loud on empty input; stakeholder/category maps are filtered to `scored_ids`.

`node_applies` itself is pure with respect to `(sig, entry, actions)`: no mutation and action ordering does not affect the boolean result.

The `Σ criteria points == 10` invariant is structurally independent of `applies_if`; it is enforced in `NodeScoring` validation, not by whether a node is included in a particular run.

I could not run the tests here: `pytest` is not installed for the available `python3`.