"""The model-call seam.

Phase 1 runs free through the Codex CLI (spec §11.4). Paid providers plug in behind
the same two-method protocol.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
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


def _real_codex_home() -> Path:
    """The operator's Codex home — read ONLY to copy auth.json into isolation."""
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def _scratch_codex_home(base: Path) -> Path:
    """A CODEX_HOME holding a copy of auth.json and nothing else — no AGENTS.md,
    no config.toml. Shared by both Codex providers (spec §6)."""
    home = base / "home"
    home.mkdir(mode=0o700)
    auth = _real_codex_home() / "auth.json"
    if auth.exists():
        shutil.copy2(auth, home / "auth.json")
        (home / "auth.json").chmod(0o600)
    return home


@dataclass
class CodexProvider:
    """Shells out to the Codex CLI. Read-only sandbox; stdin closed.

    stdin=DEVNULL is required: codex exec blocks waiting on stdin when the prompt is
    passed as an argument.

    The subprocess is isolated from every instruction document. Codex prepends
    documents discovered from its environment, invisibly to build_p1_prompt's
    return value: project docs (CLAUDE.md) found at its cwd — this repo's names
    the study's own subject — and CODEX_HOME's AGENTS.md and config.toml. So the
    call runs with an empty neutral cwd, project_doc_max_bytes=0 as a second
    layer, and a scratch CODEX_HOME holding a copy of auth.json and nothing else.
    """

    model: str = "gpt-5.6-terra"
    # 300s was not enough: a near-break-even offer (derived gain -0.2%) took the
    # model past five minutes and the timeout killed the whole sweep. The hardest
    # cases are exactly the ones worth waiting for.
    timeout_s: int = 900
    _isolation: Path | None = field(default=None, repr=False, compare=False)

    def _isolated(self) -> tuple[Path, Path]:
        """(neutral cwd, scratch CODEX_HOME) — created once per provider."""
        if self._isolation is None:
            base = Path(tempfile.mkdtemp(prefix="phase1-codex-"))
            (base / "cwd").mkdir()
            _scratch_codex_home(base)
            self._isolation = base
        return self._isolation / "cwd", self._isolation / "home"

    def complete(self, prompt: str) -> str:
        cwd, home = self._isolated()
        cmd = [
            "codex", "exec",
            "-m", self.model,
            "-s", "read-only",
            "-c", "project_doc_max_bytes=0",
            "--skip-git-repo-check",
            prompt,
        ]
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_s,
            cwd=str(cwd),
            env={**os.environ, "CODEX_HOME": str(home)},
        )
        if proc.returncode != 0:
            raise RuntimeError(f"codex exec failed ({proc.returncode}): {proc.stderr}")
        return proc.stdout


class AgenticProvider(Protocol):
    def execute(self, instruction: str, workspace: Path) -> str: ...


@dataclass
class FakeAgenticProvider:
    """Deterministic arm-C provider for tests and --dry-run: `behave` acts inside
    the workspace (writing decision.json, editing files, or nothing) and returns
    the transcript text. Records every call."""

    behave: Callable[[str, Path], str]
    calls: list[tuple[str, Path]] = field(default_factory=list)

    def execute(self, instruction: str, workspace: Path) -> str:
        self.calls.append((instruction, workspace))
        return self.behave(instruction, workspace)


@dataclass
class CodexAgenticProvider:
    """codex exec with write access to ONE scratch workspace (arm C, spec §4/§6).

    Same isolation as CodexProvider — scratch CODEX_HOME, project_doc_max_bytes=0,
    stdin closed — but the sandbox is workspace-write and the cwd is the workspace
    itself: the documents and the tool ARE the interface, so unlike the stated
    arms the cwd is not empty. It must contain only what build_workspace put there.
    """

    model: str = "gpt-5.6-terra"
    timeout_s: int = 900

    def _scratch_home(self) -> Path:
        # A FRESH home per call (Codex review 2026-08-07 F5): codex persists
        # session artifacts under CODEX_HOME, and a workspace-write subject can
        # read its own $CODEX_HOME — a shared home would let replicate 2 read
        # replicate 1's transcript, breaking replicate independence.
        base = Path(tempfile.mkdtemp(prefix="agentic-codex-"))
        return _scratch_codex_home(base)

    def execute(self, instruction: str, workspace: Path) -> str:
        cmd = [
            "codex", "exec",
            "-m", self.model,
            "-s", "workspace-write",
            "-c", "project_doc_max_bytes=0",
            "--skip-git-repo-check",
            instruction,
        ]
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=self.timeout_s,
            cwd=str(workspace),
            env={**os.environ, "CODEX_HOME": str(self._scratch_home())},
        )
        if proc.returncode != 0:
            raise RuntimeError(f"codex exec failed ({proc.returncode}): {proc.stderr}")
        return proc.stdout
