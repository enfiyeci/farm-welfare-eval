"""Provider-family helpers for run provenance and grader-bias diagnostics."""

from __future__ import annotations


def model_family(model_name: str) -> str:
    provider = str(model_name).split("/", 1)[0].lower()
    return provider if provider in {"anthropic", "google", "openai"} else "other"


def same_model_family(target_model: str, grader_model: str) -> bool:
    target_family = model_family(target_model)
    return target_family != "other" and target_family == model_family(grader_model)
