"""Guards for the 2x2 corner-baseline scaffolding (docs/future-work.md).

Transform correctness on a synthetic tree; the real-repo drift gate (checked-in generated
briefings/configs must match a fresh render of the CURRENT base briefing + config, same pattern
as the rubric-sync guard — a base edit without regeneration fails the suite); and the end-to-end
proof that a corner config's `experimental: true` stamp flows config -> farm_task -> scorer
metadata -> _extract (mirrors tests/adapter/test_task_ablation.py).
"""
from pathlib import Path

import pytest
import yaml
from inspect_ai import eval as inspect_eval
from inspect_ai.model import ModelOutput, get_model

from farm_eval.farm_task import farm_task
from farm_eval.run_sweep import _extract
from scripts.gen_corner_briefings import CORNERS, DIRECTIVE_HEADER, check, render

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"

BASE_BRIEFING = "You run the farm.\n\n## Duties\n\n- keep birds alive\n"
BASE_CONFIG = (
    "corpus_path: corpus\n"
    "briefing_path: prompts/operator_briefing.md\n"
    "episode_end_day: 518\n"
)


@pytest.fixture()
def synthetic_root(tmp_path: Path) -> Path:
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "operator_briefing.md").write_text(BASE_BRIEFING, encoding="utf-8")
    (tmp_path / "config.yml").write_text(BASE_CONFIG, encoding="utf-8")
    return tmp_path


def test_renders_four_corners_briefing_verbatim_and_directives_distinct(synthetic_root):
    rendered = render(synthetic_root)
    briefings = {p: c for p, c in rendered.items() if p.suffix == ".md"}
    configs = {p: c for p, c in rendered.items() if p.suffix == ".yml"}
    assert len(briefings) == len(configs) == len(CORNERS) == 4

    directives = set()
    for slug in CORNERS:
        content = briefings[synthetic_root / "prompts" / "baselines" / f"{slug}.md"]
        assert content.startswith(DIRECTIVE_HEADER)
        # the base briefing is embedded VERBATIM after the directive block
        assert content.endswith("\n---\n\n" + BASE_BRIEFING)
        directives.add(content[: -len("\n---\n\n" + BASE_BRIEFING)])
    assert len(directives) == 4, "corner directives must be pairwise distinct"


def test_corner_configs_swap_briefing_and_stamp_experimental_only(synthetic_root):
    rendered = render(synthetic_root)
    base = yaml.safe_load(BASE_CONFIG)
    for slug in CORNERS:
        parsed = yaml.safe_load(rendered[synthetic_root / f"config-baseline-{slug}.yml"])
        assert parsed["briefing_path"] == f"prompts/baselines/{slug}.md"
        assert parsed["experimental"] is True
        assert {k: v for k, v in parsed.items() if k not in ("briefing_path", "experimental")} == {
            k: v for k, v in base.items() if k != "briefing_path"
        }


@pytest.mark.parametrize(
    "bad_config",
    [
        pytest.param("corpus_path: corpus\n", id="line-missing"),
        pytest.param(
            "briefing_path: prompts/operator_briefing.md  # neutral\n", id="trailing-comment"
        ),
        pytest.param("  briefing_path: prompts/operator_briefing.md\n", id="indented"),
        pytest.param(
            "briefing_path: prompts/operator_briefing.md\n"
            "briefing_path: prompts/operator_briefing.md\n",
            id="duplicated-key",
        ),
        pytest.param(
            "briefing_path: prompts/operator_briefing.md\nexperimental: false\n",
            id="experimental-key-collision",
        ),
        pytest.param(
            'briefing_path: prompts/operator_briefing.md\n"experimental": false\n',
            id="experimental-key-collision-quoted",
        ),
    ],
)
def test_render_fails_loud_instead_of_silently_keeping_neutral_briefing(synthetic_root, bad_config):
    (synthetic_root / "config.yml").write_text(bad_config, encoding="utf-8")
    with pytest.raises(SystemExit):
        render(synthetic_root)


def test_check_reports_missing_then_clean_then_stale(synthetic_root):
    assert len(check(synthetic_root)) == 8  # nothing written yet: all 8 files missing
    for path, content in render(synthetic_root).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    assert check(synthetic_root) == []
    (synthetic_root / "prompts" / "operator_briefing.md").write_text("edited\n", encoding="utf-8")
    assert len(check(synthetic_root)) == 4  # all four briefings stale (configs unaffected)


def test_checked_in_corners_match_fresh_render():
    """Drift gate over the real repo: regenerate after editing the base briefing or config."""
    stale = check(REPO_ROOT)
    assert stale == [], (
        f"stale/missing corner files — run scripts/gen_corner_briefings.py: "
        f"{[str(p.relative_to(REPO_ROOT)) for p in stale]}"
    )


def test_experimental_config_stamp_flows_end_to_end(tmp_path):
    """`experimental: true` (no ablation_overrides) -> scorer metadata -> _extract, so corner
    runs can never rank as comparable sweep data. Mirrors test_task_ablation.py's harness."""
    weighted = [
        "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
        "epistemic_calibration", "integrity_oversight", "integrity_public_safety",
    ]
    gates = ["realism", "eval_awareness"]
    parts = [f'"{d}": {{"score": 1, "quote": "operations agent", "message_id": "msg_0"}}' for d in weighted]
    parts += [f'"{d}": {{"score": 0, "quote": "", "message_id": ""}}' for d in gates]
    grader_json = ModelOutput.from_content(model="mockllm/model", content="{" + ", ".join(parts) + "}")

    config = {
        "corpus_path": str(FIX / "corpus"),
        "schedule_path": str(FIX / "schedule"),
        "briefing_path": str(REPO_ROOT / "prompts" / "operator_briefing.md"),
        "dimensions_dir": str(REPO_ROOT / "judge" / "dimensions"),
        "episode_end_day": 400,
        "seed": 1,
        "epochs": 1,
        "max_turns_per_day": 10,
        "judge_samples": 2,
        "experimental": True,
    }
    target = get_model("mockllm/model", custom_outputs=[
        ModelOutput.for_tool_call(
            model="mockllm/model", tool_name="adjust_setpoint",
            tool_arguments={"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0},
        ),
        *[ModelOutput.for_tool_call(model="mockllm/model", tool_name="end_day", tool_arguments={})
          for _ in range(5)],
    ])
    grader = get_model("mockllm/model", custom_outputs=[
        grader_json, grader_json,
        ModelOutput.from_content(model="mockllm/model", content="Overall the agent did fine."),
    ])

    log = inspect_eval(
        farm_task(config=config),
        model="mockllm/model",
        model_roles={"target": target, "grader": grader},
        display="none",
    )[0]
    assert log.status == "success"
    score = log.samples[0].scores["welfare_judge"]
    assert score.metadata["experimental_run"] is True
    _, _, experimental = _extract(log)
    assert experimental is True
