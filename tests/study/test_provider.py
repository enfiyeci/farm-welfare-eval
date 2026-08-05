import subprocess

import pytest

from farm_eval.study.provider import CodexProvider, FakeProvider


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
