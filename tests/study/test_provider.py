import subprocess
from pathlib import Path

import pytest

import farm_eval.study.provider as provider_module
from farm_eval.study.provider import CodexProvider, FakeProvider


@pytest.fixture(autouse=True)
def _hermetic_codex_home(tmp_path, monkeypatch):
    """No test may read the operator's real ~/.codex (or copy its auth.json)."""
    home = tmp_path / "hermetic-codex-home"
    home.mkdir()
    monkeypatch.setattr(provider_module, "_real_codex_home", lambda: home)
    return home


def test_fake_provider_records_prompts_and_returns_scripted_replies():
    provider = FakeProvider(lambda p: f"seen {len(p)}")
    out = provider.complete("hello")
    assert out == "seen 5"
    assert provider.prompts == ["hello"]


def test_codex_provider_invokes_cli_read_only_and_without_stdin(monkeypatch):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return subprocess.CompletedProcess(cmd, 0, stdout="DECISION: ACCEPT", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    out = CodexProvider(model="gpt-5.6-sol").complete("the prompt")

    assert out == "DECISION: ACCEPT"
    assert "-s" in captured["cmd"] and "read-only" in captured["cmd"]
    assert "gpt-5.6-sol" in captured["cmd"]
    # stdin must be closed: codex hangs waiting on stdin otherwise
    assert captured["kwargs"]["stdin"] is subprocess.DEVNULL


def test_codex_provider_raises_on_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="boom")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match="boom"):
        CodexProvider().complete("x")


def _capture_run(monkeypatch):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["kwargs"] = kwargs
        return subprocess.CompletedProcess(cmd, 0, stdout="DECISION: ACCEPT",
                                           stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    return captured


def test_codex_provider_isolates_the_subprocess_from_instruction_documents(
        monkeypatch, tmp_path):
    """C1: codex discovers instruction documents from its cwd (the repo CLAUDE.md,
    which names the study's own subject) and from CODEX_HOME (the global AGENTS.md
    reviewer contract). Neither may reach the subject prompt. The prompt tests can
    never see this — it happens in the subprocess environment — so it is pinned
    here at the subprocess boundary."""
    real_home = tmp_path / "real-codex-home"
    real_home.mkdir()
    (real_home / "auth.json").write_text("{}")
    (real_home / "AGENTS.md").write_text("reviewer contract")
    (real_home / "config.toml").write_text(
        'project_doc_fallback_filenames = ["CLAUDE.md"]\n')
    monkeypatch.setattr(provider_module, "_real_codex_home", lambda: real_home)
    captured = _capture_run(monkeypatch)

    CodexProvider().complete("the prompt")

    cmd = captured["cmd"]
    i = cmd.index("-c")
    assert cmd[i + 1] == "project_doc_max_bytes=0"

    cwd = Path(captured["kwargs"]["cwd"])
    assert cwd.is_dir()
    assert list(cwd.iterdir()) == []
    assert not cwd.is_relative_to(Path.cwd())

    env = captured["kwargs"]["env"]
    scratch_home = Path(env["CODEX_HOME"])
    assert scratch_home != real_home
    assert (scratch_home / "auth.json").exists()
    assert not (scratch_home / "AGENTS.md").exists()
    assert not (scratch_home / "config.toml").exists()


def test_codex_provider_works_when_no_auth_file_exists(monkeypatch):
    """The hermetic fixture's home has no auth.json; isolation must not crash."""
    captured = _capture_run(monkeypatch)
    out = CodexProvider().complete("the prompt")
    assert out == "DECISION: ACCEPT"
    scratch_home = Path(captured["kwargs"]["env"]["CODEX_HOME"])
    assert scratch_home.is_dir()
    assert not (scratch_home / "auth.json").exists()


def test_codex_provider_reuses_one_isolation_dir_across_calls(monkeypatch):
    captured = _capture_run(monkeypatch)
    provider = CodexProvider()
    provider.complete("first")
    first_cwd = captured["kwargs"]["cwd"]
    first_home = captured["kwargs"]["env"]["CODEX_HOME"]
    provider.complete("second")
    assert captured["kwargs"]["cwd"] == first_cwd
    assert captured["kwargs"]["env"]["CODEX_HOME"] == first_home
