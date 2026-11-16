"""The `claude-code/<model>` grader provider: Claude through `claude -p` on Arda's subscription.

Every test runs a FAKE `claude` script placed first on PATH — no real `claude -p` call, no model
spend. The fake records its argv, working folder, environment and stdin, then prints a result
shaped like `claude -p --output-format json`.
"""

import asyncio
import json
import os
import stat
import sys
from importlib.metadata import entry_points

import pytest
from inspect_ai.model import ChatMessageSystem, ChatMessageUser, GenerateConfig, get_model
from inspect_ai.tool import ToolInfo

import farm_eval.judge.claude_code  # noqa: F401  (registers the provider)
from farm_eval.models import model_family, same_model_family

_FAKE = r'''#!{python}
import json, os, sys
mode = os.environ.get("FAKE_CLAUDE_MODE", "ok")
record = {{
    "argv": sys.argv[1:],
    "cwd": os.getcwd(),
    "cwd_entries": os.listdir("."),
    "env_keys": sorted(os.environ),
    "stdin": sys.stdin.read(),
}}
with open(os.environ["FAKE_CLAUDE_LOG"], "w") as f:
    json.dump(record, f)
if mode == "hang":
    import time
    with open(os.environ["FAKE_CLAUDE_LOG"] + ".pid", "w") as f:
        f.write(str(os.getpid()))
    time.sleep(60)
if mode == "exit_fail":
    sys.stderr.write("Error: usage limit reached")
    sys.exit(1)
result = {{
    "type": "result",
    "subtype": "success",
    "is_error": mode == "error_result",
    "result": "Claude AI usage limit reached" if mode == "error_result" else '{{"score": 7}}',
    "usage": {{
        "input_tokens": "unknown" if mode == "bad_usage" else 12,
        "cache_creation_input_tokens": 300,
        "cache_read_input_tokens": 4000,
        "output_tokens": 25,
    }},
    "total_cost_usd": 0.5,
}}
print(json.dumps(result))
'''


@pytest.fixture
def fake_claude(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    script = bindir / "claude"
    script.write_text(_FAKE.format(python=sys.executable))
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    log = tmp_path / "fake-claude.json"
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_CLAUDE_LOG", str(log))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-must-not-reach-claude")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tok-test-must-not-reach-claude")
    for selector in ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY",
                     "CLAUDE_CODE_USE_ANTHROPIC_AWS"):
        monkeypatch.setenv(selector, "1")
    return lambda: json.loads(log.read_text())


def _generate(model, prompt="Grade this transcript.", **kwargs):
    return asyncio.run(model.generate(prompt, **kwargs))


def _model(**model_args):
    return get_model("claude-code/claude-opus-5-5", memoize=False, **model_args)


def test_completion_comes_from_the_cli_result(fake_claude):
    out = _generate(_model())
    assert out.completion == '{"score": 7}'


def test_cli_runs_print_mode_with_no_tools_no_session_and_no_user_settings(fake_claude):
    _generate(_model())
    argv = fake_claude()["argv"]
    assert argv[0] in ("-p", "--print")
    pairs = {argv[i]: argv[i + 1] for i in range(len(argv) - 1)}
    assert pairs["--output-format"] == "json"
    assert pairs["--tools"] == ""
    assert pairs["--model"] == "claude-opus-5-5"
    assert pairs["--setting-sources"] == "project"
    # --safe-mode turns off CLAUDE.md, hooks, plugins and MCP servers while keeping the sign-in.
    for flag in ("--safe-mode", "--no-session-persistence", "--strict-mcp-config", "--disable-slash-commands"):
        assert flag in argv
    assert "--bare" not in argv  # --bare refuses OAuth, so it cannot use the subscription


def test_prompt_goes_on_stdin_not_argv(fake_claude):
    prompt = "Grade this transcript. " * 50
    _generate(_model(), prompt)
    record = fake_claude()
    assert record["stdin"] == prompt
    assert not any("Grade this transcript" in a for a in record["argv"])


def test_cli_runs_in_an_empty_temp_folder_outside_the_repo(fake_claude):
    _generate(_model())
    record = fake_claude()
    assert record["cwd_entries"] == []
    assert os.path.realpath(record["cwd"]) != os.path.realpath(os.getcwd())


def test_api_keys_are_dropped_so_the_subscription_is_used(fake_claude):
    _generate(_model())
    keys = fake_claude()["env_keys"]
    assert "ANTHROPIC_API_KEY" not in keys
    assert "ANTHROPIC_AUTH_TOKEN" not in keys
    assert not [k for k in keys if k.startswith("CLAUDE_CODE_USE_")]  # no cloud-provider routing
    assert os.environ["ANTHROPIC_API_KEY"]  # the parent's environment is untouched


def test_inspect_effort_setting_is_passed_through(fake_claude):
    # Inspect's GenerateConfig.effort takes exactly the CLI's values (low..max), and the role's
    # config is recorded in the log, so the effort pin is part of provenance. CLI form:
    # --model-role 'grader={model: claude-code/<id>, effort: high}'
    model = get_model("claude-code/claude-opus-5-5", memoize=False, config=GenerateConfig(effort="high"))
    _generate(model)
    argv = fake_claude()["argv"]
    assert argv[argv.index("--effort") + 1] == "high"


def test_unknown_model_args_are_refused():
    with pytest.raises(RuntimeError, match="unknown model args"):
        _model(effort="high")


def test_no_effort_flag_by_default(fake_claude):
    _generate(_model())
    assert "--effort" not in fake_claude()["argv"]


def test_system_message_becomes_the_system_prompt(fake_claude):
    _generate(_model(), [ChatMessageSystem(content="Be a strict grader."), ChatMessageUser(content="Go.")])
    record = fake_claude()
    argv = record["argv"]
    assert argv[argv.index("--system-prompt") + 1] == "Be a strict grader."
    assert record["stdin"] == "Go."


def test_usage_is_recorded(fake_claude):
    usage = _generate(_model()).usage
    assert usage.input_tokens == 12
    assert usage.input_tokens_cache_write == 300
    assert usage.input_tokens_cache_read == 4000
    assert usage.output_tokens == 25
    assert usage.total_tokens == 12 + 300 + 4000 + 25


def test_malformed_usage_keeps_the_completion(fake_claude, monkeypatch):
    # Never a ValueError out of generate(): the criterion path would record it as 0 points.
    monkeypatch.setenv("FAKE_CLAUDE_MODE", "bad_usage")
    out = _generate(_model())
    assert out.completion == '{"score": 7}'
    assert out.usage is None


def test_unencodable_prompt_raises_runtime_error(fake_claude):
    # An unpaired surrogate makes UTF-8 encoding raise UnicodeEncodeError, a ValueError subclass.
    with pytest.raises(RuntimeError) as info:
        _generate(_model(), "grade \ud800 this")
    assert not isinstance(info.value, ValueError)


def test_error_result_raises_runtime_error_not_value_error(fake_claude, monkeypatch):
    # The criterion path catches ValueError and records the criterion as 0 points: a usage-limit
    # failure must crash loudly instead of silently zeroing welfare criteria.
    monkeypatch.setenv("FAKE_CLAUDE_MODE", "error_result")
    with pytest.raises(RuntimeError, match="usage limit") as info:
        _generate(_model())
    assert not isinstance(info.value, ValueError)


def test_nonzero_exit_raises_with_stderr(fake_claude, monkeypatch):
    monkeypatch.setenv("FAKE_CLAUDE_MODE", "exit_fail")
    with pytest.raises(RuntimeError, match="usage limit reached") as info:
        _generate(_model())
    assert not isinstance(info.value, ValueError)


def test_timeout_raises_and_kills_the_cli(fake_claude, monkeypatch):
    monkeypatch.setenv("FAKE_CLAUDE_MODE", "hang")
    model = get_model("claude-code/claude-opus-5-5", memoize=False, timeout=1)
    with pytest.raises(RuntimeError, match="timed out"):
        _generate(model)
    pid = int(open(os.environ["FAKE_CLAUDE_LOG"] + ".pid").read())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)  # the child is gone, not left running


def test_tools_are_refused(fake_claude):
    tool = ToolInfo(name="send_email", description="send")
    with pytest.raises(RuntimeError, match="tools"):
        _generate(_model(), tools=[tool])


def test_multi_turn_input_is_refused(fake_claude):
    from inspect_ai.model import ChatMessageAssistant

    msgs = [ChatMessageUser(content="a"), ChatMessageAssistant(content="b"), ChatMessageUser(content="c")]
    with pytest.raises(RuntimeError, match="one user message"):
        _generate(_model(), msgs)


def test_claude_code_counts_as_the_anthropic_family():
    assert model_family("claude-code/claude-opus-5-5") == "anthropic"
    assert same_model_family("anthropic/claude-opus-5-5", "claude-code/claude-opus-5-5")
    assert not same_model_family("google/gemini-3.8-flash", "claude-code/claude-opus-5-5")


def test_provider_is_registered_through_an_inspect_entry_point():
    # Lets `--model-role grader=claude-code/<id>` resolve from the inspect CLI without an import.
    eps = [ep for ep in entry_points(group="inspect_ai") if ep.value.startswith("farm_eval")]
    assert eps, "farm_eval has no inspect_ai entry point (reinstall: pip install -e . --no-deps)"
