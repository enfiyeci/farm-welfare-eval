"""End to end: manifest -> samples -> solver -> node scorer, on mockllm, over the node fixture."""
import math
from pathlib import Path

import pytest
from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

from farm_eval.node_task import farm_node_task
from farm_eval.report.reliability import rows_from_log, summarize

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

CONFIG = {
    "corpus_path": str(FIX / "corpus"),
    "schedule_path": str(FIX / "node_schedule"),
    "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
    "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
    "seed": 1,
    "epochs": 1,
    "max_turns_per_day": 10,
    "judge_samples": 1,
    "dimension_mode": "validity_only",
}
_GATES = ["realism", "eval_awareness", "assistant_persona_bleed", "helplessness_resignation"]


def _validity_json():
    parts = [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in _GATES]
    return ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")


def _act():
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name="adjust_setpoint",
                                     tool_arguments={"house_id": "H_NOSENSOR", "system": "ventilation", "value": 1.2})


def _end():
    return ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})


def test_node_task_expands_manifest_and_scores_each_episode():
    # three samples (neutral, history_bad, QUIET_D15). mockllm's custom_outputs is ONE iterator
    # per model instance shared across concurrently-running samples, so max_samples=1 is required
    # to force strict dataset order — otherwise whichever sample reaches generate() first consumes
    # _act() and the others only ever see end_day, making the neutral-scores-10.0 assertion below
    # a race. With order forced, only the first sample (neutral) acts; the rest only end days.
    target = get_model("mockllm/model", custom_outputs=[_act(), *[_end() for _ in range(8)]] * 3)
    grader = get_model("mockllm/model", custom_outputs=[_validity_json() for _ in range(3)])
    log = inspect_eval(farm_node_task(config=CONFIG), model="mockllm/model",
                       model_roles={"target": target, "grader": grader}, display="none",
                       max_samples=1)[0]
    assert log.status == "success"
    by_id = {s.id: s for s in log.samples}
    assert set(by_id) == {"DP_PLACEHOLDER_2::neutral", "DP_PLACEHOLDER_2::history_bad", "QUIET_D15::neutral"}
    neutral = by_id["DP_PLACEHOLDER_2::neutral"]
    assert neutral.metadata["dp_id"] == "DP_PLACEHOLDER_2" and neutral.metadata["arm"] == "neutral"
    score = neutral.scores["node_welfare_judge"]
    assert score.value["welfare_headline"] == 10.0
    assert score.metadata["node_scores"] == {"DP_PLACEHOLDER_2": 10.0}
    # Ruling 21: the farm carried BOTH fixture decisions (DP_PLACEHOLDER_1 lapsed on day 5 before
    # this episode opened); the judge scored only the episode's own.
    assert "DP_PLACEHOLDER_1" not in score.metadata["node_scores"]
    assert score.metadata["episode_id"] == "DP_PLACEHOLDER_2" and score.metadata["arm"] == "neutral"
    assert "welfare_decision_quality" not in score.value      # validity_only: weighted dims not graded
    assert "eval_awareness" in score.value
    # WP2 / D1: the persisted log says WHY — one record per authored criterion, whose credits sum
    # (after the node's cap/floor) to the node score, and one explanation line per criterion.
    records = score.metadata["node_criteria"]["DP_PLACEHOLDER_2"]
    assert [r["name"] for r in records] == ["addressed"]
    steps = score.metadata["node_score_steps"]["DP_PLACEHOLDER_2"]
    assert sum(r["credit"] for r in records) == pytest.approx(steps["criteria_sum"])
    assert steps["cap_floor"] is None and steps["score"] == 10.0
    assert "DP_PLACEHOLDER_2.addressed [mechanical]" in score.explanation
    assert "DP_PLACEHOLDER_1" not in score.metadata["node_criteria"]
    # D6 / E1: run-health counters and the realism-source diagnostic ride along.
    assert score.metadata["text_only_turns"] == 0 and score.metadata["forced_advances"] == 0
    assert score.metadata["realism_quote_source"] == "unknown"  # the mock grader cites nothing
    quiet = by_id["QUIET_D15::neutral"].scores["node_welfare_judge"]
    # grade_episode assigns float("nan") in-process, and inspect_eval's returned EvalLog has
    # already been through the log's JSON round-trip. That persists NaN as null up to inspect-ai
    # 0.3.241 (read back as None) and as a NaN constant from 0.3.266 (read back as nan); see
    # tests/judge/test_scorer_partial.py. Either way a quiet episode has NO finite headline.
    headline = quiet.value["welfare_headline"]
    assert headline is None or math.isnan(headline)
    assert quiet.metadata["quiet_episode"] is True

    # D10: rows_from_log/summarize read the same log post hoc (report/reliability.py, Task 11).
    rows = rows_from_log(log)
    assert len(rows) == 3
    rel = summarize(rows, headline_arm="neutral")
    assert rel.headline == 10.0
    assert rel.headline_n_nodes == 1
    assert rel.quiet_episodes == 1
    assert rel.nodes[("DP_PLACEHOLDER_2", "history_bad")].mean == 0.0


def test_episode_filter_selects_a_subset():
    target = get_model("mockllm/model", custom_outputs=[_end() for _ in range(8)])
    grader = get_model("mockllm/model", custom_outputs=[_validity_json()])
    log = inspect_eval(farm_node_task(config=CONFIG, episode_ids="QUIET_D15"), model="mockllm/model",
                       model_roles={"target": target, "grader": grader}, display="none")[0]
    assert [s.id for s in log.samples] == ["QUIET_D15::neutral"]


def test_invalid_dimension_mode_rejected_before_any_run():
    with pytest.raises(ValueError, match="dimension_mode"):
        farm_node_task(config=CONFIG, dimension_mode="validty_only")


def test_relative_paths_resolve_against_repo_root_when_cwd_differs(monkeypatch):
    # `inspect eval farm_eval/node_task.py -T config_path=config-nodes.yml` — Inspect chdirs into
    # the task file's directory (farm_eval/) at load AND run time, so a bare relative path would
    # otherwise look for farm_eval/config-nodes.yml and farm_eval/corpus. Both must resolve
    # against the repo root instead (the real manifest, no model call: construction only).
    monkeypatch.chdir(REPO_ROOT / "farm_eval")
    t = farm_node_task(config_path="config-nodes.yml", episode_ids="DP05_RED_MITE")
    assert [s.id for s in t.dataset] == ["DP05_RED_MITE::neutral"]


def test_episode_ids_accepts_the_list_form_inspect_passes_for_comma_values():
    # `inspect eval -T episode_ids=A,B` reaches the task as a list, `-T episode_ids=A` as a str.
    as_list = farm_node_task(config_path="config-nodes.yml", episode_ids=["QUIET_A", "QUIET_B"])
    as_str = farm_node_task(config_path="config-nodes.yml", episode_ids="QUIET_A, QUIET_B")
    assert sorted(s.id for s in as_list.dataset) == sorted(s.id for s in as_str.dataset)
    assert {s.id for s in as_list.dataset} == {"QUIET_A::neutral", "QUIET_B::neutral"}


# --- B4 (k=1 run, 2026-09-22): one errored sample must not cancel the batch -----------------------
# Inspect's default `fail_on_error=True` turned DP15's provider 400 into a cancel of every other
# in-flight sample (DP12, DPF) and ended the 17-sample task at 7. A node run isolates per-sample
# errors: the errored sample is recorded with its error, the others still run and score.


class _ProviderError(RuntimeError):
    """Stands in for a provider rejection (e.g. Vertex 400 INVALID_ARGUMENT)."""


def _target_failing_first_call():
    script = iter([*[_end() for _ in range(8)]] * 3)
    calls = {"n": 0}

    def generate(input, tools, tool_choice, config):
        calls["n"] += 1
        if calls["n"] == 1:
            raise _ProviderError("Requests ending with a model turn are not supported.")
        return next(script)

    return get_model("mockllm/model", custom_outputs=generate)


def test_one_errored_sample_does_not_cancel_the_others():
    grader = get_model("mockllm/model", custom_outputs=[_validity_json() for _ in range(3)])
    # max_samples=1 forces dataset order: the first sample (neutral) takes the provider error.
    log = inspect_eval(farm_node_task(config=CONFIG), model="mockllm/model",
                       model_roles={"target": _target_failing_first_call(), "grader": grader},
                       display="none", max_samples=1)[0]
    assert log.status == "success", log.error
    by_id = {s.id: s for s in log.samples}
    assert set(by_id) == {"DP_PLACEHOLDER_2::neutral", "DP_PLACEHOLDER_2::history_bad", "QUIET_D15::neutral"}
    errored = by_id["DP_PLACEHOLDER_2::neutral"]
    assert errored.error is not None and "model turn" in errored.error.message
    for sid in ("DP_PLACEHOLDER_2::history_bad", "QUIET_D15::neutral"):
        assert by_id[sid].error is None
        assert "node_welfare_judge" in (by_id[sid].scores or {})
    # the reliability report lists the errored sample instead of raising (report/reliability.py)
    rows = rows_from_log(log)
    assert len(rows) == 3


def test_node_config_file_isolates_sample_errors():
    # The shipped config carries the setting, so a launch line without --fail-on-error is safe.
    import yaml
    cfg = yaml.safe_load((REPO_ROOT / "config-nodes.yml").read_text(encoding="utf-8"))
    assert cfg["fail_on_error"] is False
    assert farm_node_task(config_path="config-nodes.yml", episode_ids="QUIET_A").fail_on_error is False


def test_fail_on_error_is_configurable():
    assert farm_node_task(config={**CONFIG, "fail_on_error": 0.5}).fail_on_error == 0.5
    assert farm_node_task(config=CONFIG).fail_on_error is False   # key absent: still isolated


# --- WP11: each sample's console banner shows ITS previous session, not the run's day 0 ---------

def _login_line(text: str) -> str:
    return next(l for l in text.splitlines() if l.startswith("last login: "))


def _expected_login(cfg: dict, sample) -> tuple[str | None, str]:
    """(the previous session the opening digest's own header announces, as the banner writes it
    — date + that day's console-open time — or None when the header names no earlier session;
    the opening digest itself)."""
    from farm_eval.adapter.context import EpisodeConfig, resolve_episode, snapshot_for
    from farm_eval.config_paths import anchor_paths
    from farm_eval.env.clock import advance_elapsed, date_for_day, session_open_text
    from farm_eval.node_task import _PATH_KEYS

    c = anchor_paths(cfg, _PATH_KEYS)
    ecfg = EpisodeConfig(corpus_path=c["corpus_path"], schedule_path=c["schedule_path"],
                         episode_end_day=10_000, seed=int(c.get("seed", 0)), node_episodes=True)
    ep = resolve_episode(ecfg, sample.metadata)
    state, digest = snapshot_for(ecfg, ep)
    elapsed = advance_elapsed(digest)
    if not elapsed:
        return None, digest
    prev = ep.start_day - elapsed
    return f"last login: {date_for_day(state.start_date, prev)} {session_open_text(state.start_date, prev)} ", digest


def test_fixture_samples_show_their_own_previous_session_as_last_login():
    task = farm_node_task(config=CONFIG)
    authored = _login_line((REPO_ROOT / "prompts" / "operator_briefing.md").read_text(encoding="utf-8"))
    checked = 0
    for sample in task.dataset:
        want, _ = _expected_login(CONFIG, sample)
        line = _login_line(sample.input)
        if want is None:
            assert line == authored
            continue
        assert line.startswith(want), (sample.id, line, want)
        assert line.endswith(authored.split(" from ", 1)[1]) and " from " in line
        checked += 1
    assert checked >= 1


def test_no_real_node_sample_opens_under_a_stale_banner():
    """The leak scan's stale-banner check (farm_eval/probe/log_leaks.py) over every real
    (episode, arm): the banner's login is exactly the previous session the header names."""
    import yaml
    from farm_eval.probe.log_leaks import stale_banner

    cfg = yaml.safe_load((REPO_ROOT / "config-nodes.yml").read_text(encoding="utf-8"))
    task = farm_node_task(config_path="config-nodes.yml")
    assert len(task.dataset) >= 20
    for sample in task.dataset:
        want, digest = _expected_login(cfg, sample)
        assert want is not None, sample.id      # every real episode opens after a routine session
        assert _login_line(sample.input).startswith(want), (sample.id, _login_line(sample.input), want)
        assert stale_banner([sample.input, digest]) is None, sample.id
