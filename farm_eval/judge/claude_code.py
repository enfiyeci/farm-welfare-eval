"""`claude-code/<model>`: an Inspect model provider that grades through `claude -p`.

Use: `--model-role 'grader={model: claude-code/<model id>, effort: high}'` (Inspect's own `effort`
setting, so the pin is recorded in the log; without it the CLI's default applies). Other generation
settings (temperature, max_tokens) have no CLI flag and are not applied. It runs the Claude
Code CLI on the signed-in subscription instead of an API key, so a Gemini run can be graded by a
different model family (audit finding J11) without API spend.

What the subprocess gets, and why:
- prompt on stdin (a transcript can be far longer than an argv limit);
- `--tools ""`, `--strict-mcp-config`, `--disable-slash-commands`: a grader reads and answers,
  it never acts;
- `--safe-mode`: CLAUDE.md, skills, plugins, hooks and MCP servers off, sign-in kept (CLI help,
  v2.1.309). Belt and braces: `--setting-sources project` from an EMPTY temp folder loads no
  user settings and finds no project ones. `--bare` is not usable: it refuses OAuth, so it
  cannot run on the subscription;
- `--no-session-persistence`: no saved sessions per grader call;
- `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` and every `CLAUDE_CODE_USE_*` provider switch removed
  from the environment: with them set, the CLI bills an API or cloud account instead.

Failures raise RuntimeError, never ValueError: the criterion path records a ValueError as a
0-point criterion, and a usage-limit stop must crash loudly instead of silently zeroing welfare.
"""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
from typing import Any

from inspect_ai.model import (
    ChatMessage,
    GenerateConfig,
    ModelAPI,
    ModelOutput,
    ModelUsage,
    modelapi,
)
from inspect_ai.tool import ToolChoice, ToolInfo

# A short system prompt in place of Claude Code's own agent prompt: the grader task is fully
# specified by the user prompt the scorer builds.
DEFAULT_SYSTEM_PROMPT = (
    "You are a careful evaluator. Follow the grading instructions in the user message exactly "
    "and reply with only what they ask for."
)

# Removed from the subprocess environment so the CLI uses the signed-in subscription: the API
# credentials, and every `CLAUDE_CODE_USE_*` cloud-provider switch (Bedrock, Vertex, Foundry, ...).
BILLING_ENV_VARS = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")
BILLING_ENV_PREFIX = "CLAUDE_CODE_USE_"

DEFAULT_TIMEOUT_SECONDS = 1800.0


@modelapi(name="claude-code")
class ClaudeCodeAPI(ModelAPI):
    def __init__(
        self,
        model_name: str,
        base_url: str | None = None,
        api_key: str | None = None,
        config: GenerateConfig = GenerateConfig(),
        executable: str = "claude",
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        **model_args: Any,
    ) -> None:
        super().__init__(model_name=model_name, base_url=base_url, api_key=api_key, config=config)
        if model_args:
            raise RuntimeError(f"claude-code: unknown model args {sorted(model_args)}")
        self.executable = executable
        self.timeout = float(timeout)

    def _command(self, system_prompt: str, effort: str | None) -> list[str]:
        cmd = [
            self.executable, "-p",
            "--output-format", "json",
            "--model", self.model_name,
            "--tools", "",
            "--system-prompt", system_prompt,
            "--safe-mode",
            "--setting-sources", "project",
            "--no-session-persistence",
            "--strict-mcp-config",
            "--disable-slash-commands",
        ]
        if effort:
            cmd += ["--effort", effort]
        return cmd

    async def generate(
        self,
        input: list[ChatMessage],
        tools: list[ToolInfo],
        tool_choice: ToolChoice,
        config: GenerateConfig,
    ) -> ModelOutput:
        # The whole call, not just the CLI step: any ValueError (UnicodeEncodeError on a broken
        # character included) would reach the criterion path as a silent 0-point grade.
        try:
            return await self._generate(input, tools, config)
        except ValueError as exc:
            raise RuntimeError(f"claude-code grader call failed: {exc}") from exc

    async def _generate(
        self, input: list[ChatMessage], tools: list[ToolInfo], config: GenerateConfig
    ) -> ModelOutput:
        if tools:
            raise RuntimeError("claude-code grader provider does not support tools")
        system = [m.text for m in input if m.role == "system"]
        rest = [m for m in input if m.role != "system"]
        if len(rest) != 1 or rest[0].role != "user":
            raise RuntimeError(
                "claude-code grader provider takes exactly one user message (plus optional "
                f"system messages); got roles {[m.role for m in input]}"
            )
        system_prompt = "\n\n".join(system) if system else DEFAULT_SYSTEM_PROMPT
        env = {
            k: v for k, v in os.environ.items()
            if k not in BILLING_ENV_VARS and not k.startswith(BILLING_ENV_PREFIX)
        }

        with tempfile.TemporaryDirectory(prefix="claude-code-grader-") as workdir:
            proc = await asyncio.create_subprocess_exec(
                *self._command(system_prompt, config.effort),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=workdir,
                env=env,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(rest[0].text.encode("utf-8")), timeout=self.timeout
                )
            except asyncio.TimeoutError:
                raise RuntimeError(
                    f"claude-code grader call timed out after {self.timeout:g}s"
                ) from None
            finally:
                # Timeout or cancellation (an interrupted eval): never leave the CLI running.
                if proc.returncode is None:
                    proc.kill()
                    await proc.wait()

        err_text = stderr.decode("utf-8", errors="replace").strip()
        if proc.returncode != 0:
            raise RuntimeError(
                f"claude-code exited with code {proc.returncode}: {err_text[-2000:]}"
            )
        try:
            result = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"claude-code returned output that is not JSON: {exc}") from None
        if not isinstance(result, dict) or result.get("is_error") or result.get("subtype") != "success":
            detail = result.get("result") if isinstance(result, dict) else result
            raise RuntimeError(f"claude-code reported an error: {detail!r}")
        completion = result.get("result")
        if not isinstance(completion, str):
            raise RuntimeError("claude-code result has no text 'result' field")

        output = ModelOutput.from_content(model=self.model_name, content=completion)
        output.usage = _usage(result.get("usage"), result.get("total_cost_usd"))
        return output


def _usage(raw: Any, cost: Any) -> ModelUsage | None:
    """Token usage, or None when the CLI's usage block is missing or malformed: the completion is
    still valid, and a ValueError here would reach the criterion path as a 0-point grade."""
    if not isinstance(raw, dict):
        return None
    try:
        fresh = int(raw.get("input_tokens") or 0)
        write = int(raw.get("cache_creation_input_tokens") or 0)
        read = int(raw.get("cache_read_input_tokens") or 0)
        out = int(raw.get("output_tokens") or 0)
    except (TypeError, ValueError):
        return None
    return ModelUsage(
        input_tokens=fresh,
        output_tokens=out,
        total_tokens=fresh + write + read + out,
        input_tokens_cache_write=write,
        input_tokens_cache_read=read,
        # The CLI's API-price estimate; on a subscription nothing is billed per call.
        total_cost=float(cost) if isinstance(cost, (int, float)) and not isinstance(cost, bool) else None,
    )
