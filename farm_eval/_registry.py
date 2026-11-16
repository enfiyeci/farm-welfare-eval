"""Inspect entry point (pyproject `[project.entry-points.inspect_ai]`): registers farm_eval's
model providers so `--model-role grader=claude-code/<model>` resolves from the inspect CLI."""

from farm_eval.judge.claude_code import ClaudeCodeAPI  # noqa: F401
