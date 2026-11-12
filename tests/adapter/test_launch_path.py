from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[2]


def test_inspect_is_pinned_and_provider_extra_matches_installed_requirements():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert "inspect-ai==0.3.244" in project["dependencies"]
    assert project["optional-dependencies"]["providers"] == [
        "anthropic>=0.115.0",
        "openai>=2.40.0",
        "google-genai>=1.69.0",
    ]


def test_node_launcher_has_bounded_retries_and_timeouts_without_echoing_keys():
    text = (ROOT / "scripts" / "run_node_episode.sh").read_text()
    assert "--max-retries 6" in text
    assert "--attempt-timeout 600" in text
    assert "ANTHROPIC_API_KEY" in text and "OPENAI_API_KEY" in text
    assert "GOOGLE_CLOUD_PROJECT" in text and "GOOGLE_CLOUD_LOCATION" in text
    assert "echo \"$ANTHROPIC_API_KEY\"" not in text
