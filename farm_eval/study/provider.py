"""The model-call seam.

Phase 1 runs free through the Codex CLI (spec §11.4). Paid providers plug in behind
the same two-method protocol.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from typing import Callable, Protocol


class TextProvider(Protocol):
    def complete(self, prompt: str) -> str: ...


@dataclass
class FakeProvider:
    """Deterministic provider for tests. Records every prompt it is given."""

    responder: Callable[[str], str]
    prompts: list[str] = field(default_factory=list)

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.responder(prompt)


@dataclass
class CodexProvider:
    """Shells out to the Codex CLI. Read-only sandbox; stdin closed.

    stdin=DEVNULL is required: codex exec blocks waiting on stdin when the prompt is
    passed as an argument.
    """

    model: str = "gpt-5.6-sol"
    timeout_s: int = 300

    def complete(self, prompt: str) -> str:
        cmd = [
            "codex", "exec",
            "-m", self.model,
            "-s", "read-only",
            "--skip-git-repo-check",
            prompt,
        ]
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_s,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"codex exec failed ({proc.returncode}): {proc.stderr}")
        return proc.stdout
