"""Task 12 -- the `scripts/behaviour_report.py` CLI.

Keyless throughout. The episode is the same scripted `mockllm` run the behaviour golden is built
from (`scripts/regen_spectator_golden.run_episode`), so the CLI is exercised over a real `.eval`
log rather than a hand-built stub, and the reader path is scripted through `mockllm` custom
outputs -- no live model is contacted anywhere in this module.

What is pinned:
  - `--json-only` writes `<out>/behaviour_model.json` and it validates as a `BehaviourModel`;
  - the JSON the CLI writes is the builder's own model (same source hash, same counts);
  - `--reader off` (the default) makes NO reader call at all;
  - a reader mode appends verdicts to the JSON the CLI writes;
  - `--reader-model` defaults to the log's recorded grader model;
  - without `--json-only` the HTML report is rendered too, carrying the behaviour sections.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from inspect_ai.model import ModelOutput, get_model

from farm_eval.analysis.model import BehaviourModel
from scripts import behaviour_report
from scripts.regen_spectator_golden import run_episode


@pytest.fixture(scope="module")
def log_location(tmp_path_factory) -> str:
    """One scripted episode for the whole module -- running it is the expensive part."""
    return run_episode(tmp_path_factory.mktemp("cli") / "logs").location


def _scripted_reader(*replies: str):
    return get_model(
        "mockllm/model",
        custom_outputs=[
            ModelOutput.from_content(model="mockllm/model", content=reply) for reply in replies
        ],
    )


_REPLY = json.dumps(
    [
        {
            "interestingness": 8,
            "category": "ventilation_neglect",
            "note": "The agent never revisited the house it opened the episode with.",
            "quotes": [],
        }
    ]
)


# --- the JSON path --------------------------------------------------------------------


def test_json_only_writes_a_behaviour_model_that_validates(log_location, tmp_path) -> None:
    out = tmp_path / "json-only"

    assert behaviour_report.main([log_location, "--out", str(out), "--json-only"]) == 0

    written = out / "behaviour_model.json"
    assert written.exists()
    model = BehaviourModel.model_validate_json(written.read_text(encoding="utf-8"))
    assert model.feed_fidelity == "full"
    assert model.day_map_valid is True
    assert model.reader_verdicts == []
    assert model.dossiers and model.tool_profiles


def test_json_only_does_not_render_the_html_report(log_location, tmp_path) -> None:
    out = tmp_path / "no-html"
    behaviour_report.main([log_location, "--out", str(out), "--json-only"])

    assert list(out.glob("*.html")) == []


def test_the_written_json_is_the_builders_own_model(log_location, tmp_path) -> None:
    """The CLI must be a thin wrapper: what it writes is what `build_behaviour_model` returned."""
    out = tmp_path / "same"
    behaviour_report.main([log_location, "--out", str(out), "--json-only"])
    written = json.loads((out / "behaviour_model.json").read_text(encoding="utf-8"))

    from farm_eval.analysis.build import build_behaviour_model

    direct = json.loads(build_behaviour_model(log_location).model_dump_json())
    assert written == direct


# --- the reader path (scripted; never live) -------------------------------------------


def test_the_default_reader_mode_makes_no_model_call(log_location, tmp_path, monkeypatch) -> None:
    def explode(*args, **kwargs):  # pragma: no cover - the point is that it never runs
        raise AssertionError("the CLI must not call the reader unless --reader asks for it")

    monkeypatch.setattr(behaviour_report, "read_behaviour", explode)
    out = tmp_path / "reader-off"

    assert behaviour_report.main([log_location, "--out", str(out), "--json-only"]) == 0
    assert json.loads((out / "behaviour_model.json").read_text())["reader_verdicts"] == []


def test_sweep_verdicts_land_in_the_written_json(log_location, tmp_path, monkeypatch) -> None:
    # The scripted episode's digest is one chunk, so sweep mode is exactly one generate call.
    monkeypatch.setattr(
        "farm_eval.analysis.reader.get_model", lambda *a, **k: _scripted_reader(_REPLY)
    )
    out = tmp_path / "sweep"

    assert behaviour_report.main(
        [log_location, "--out", str(out), "--json-only", "--reader", "sweep",
         "--reader-model", "mockllm/model"]
    ) == 0

    verdicts = json.loads((out / "behaviour_model.json").read_text())["reader_verdicts"]
    assert [v["mode"] for v in verdicts] == ["sweep"]
    assert verdicts[0]["category"] == "ventilation_neglect"


def test_reader_model_defaults_to_the_logs_recorded_grader(log_location, tmp_path, monkeypatch) -> None:
    seen: list[object] = []

    def capture(name, *args, **kwargs):
        seen.append(name)
        return _scripted_reader(_REPLY)

    monkeypatch.setattr("farm_eval.analysis.reader.get_model", capture)
    out = tmp_path / "default-model"

    behaviour_report.main([log_location, "--out", str(out), "--json-only", "--reader", "sweep"])

    assert seen == ["mockllm/model"], "the reader must run on the log's own grader model"


# --- the HTML path --------------------------------------------------------------------


def test_the_html_report_is_rendered_with_the_behaviour_sections(log_location, tmp_path) -> None:
    out = tmp_path / "full"

    assert behaviour_report.main([log_location, "--out", str(out)]) == 0

    html = (out / "behaviour_report.html").read_text(encoding="utf-8")
    assert 'id="offnode-findings"' in html
    assert 'id="pertool-behaviour"' in html
    assert (out / "behaviour_model.json").exists()


def test_the_report_run_does_not_touch_the_committed_pilot_history(log_location, tmp_path) -> None:
    """Reading the trend is fine; a diagnostic re-render must not append a row to it."""
    history = Path(behaviour_report.HISTORY_PATH)
    before = history.read_bytes() if history.exists() else None

    behaviour_report.main([log_location, "--out", str(tmp_path / "history")])

    after = history.read_bytes() if history.exists() else None
    assert after == before
