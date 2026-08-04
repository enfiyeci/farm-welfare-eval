"""Tier-2 judge pass over a play session (spec §6): convert the session record to the judge's
message shape and run the same grading path as welfare_judge (grade_episode), then merge into
the tier-1 report card. Human results are ADVISORY — bannered, never sweep-comparable.

Usage:
    ./venv/bin/python scripts/score_session.py sessions/my-run --model anthropic/claude-opus-4-8 \\
        [--samples 3] [--out sessions/my-run/report.md] [--dimensions-dir judge/dimensions]
"""

import argparse
import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


async def score_session(
    session_dir: pathlib.Path, model_name: str, samples: int,
    out: pathlib.Path, dimensions_dir: pathlib.Path, *, model=None,
) -> str:
    """Grade a completed play session with the tier-2 judge and write the merged report.

    `model` may be pre-built and injected (tests do this with a scripted `mockllm/model` so the
    grader's outputs are deterministic); when omitted, `get_model(model_name)` is called here.
    """
    import yaml
    from inspect_ai.model import get_model

    from farm_eval.env.loader import load_schedule
    from farm_eval.judge.dimensions import load_dimensions
    from farm_eval.judge.scorer import grade_episode, load_signatures
    from farm_eval.play.record import load_record, record_to_messages
    from farm_eval.play.report import build_report
    from farm_eval.play.session import PlaySession

    session_dir = pathlib.Path(session_dir)
    meta = yaml.safe_load((session_dir / "meta.yml").read_text(encoding="utf-8"))
    try:
        session = PlaySession.resume(session_dir)
    except ValueError as exc:
        sys.exit(str(exc))
    try:
        env_state = session.state_for_report()
    except PermissionError:
        sys.exit(
            f"session at {session_dir} is not finished — finish playing (reach the end of the "
            f"episode) before running the judge pass"
        )
    # The session's snapshotted briefing (the text the player actually saw), never the live file.
    messages = record_to_messages(load_record(session_dir), session.briefing())

    if model is None:
        model = get_model(model_name)

    async def generate(prompt: str) -> str:
        return (await model.generate(prompt)).completion

    score = await grade_episode(
        messages, env_state,
        dimensions=load_dimensions(dimensions_dir),
        signatures=load_signatures(meta["schedule_path"]),
        schedule=load_schedule(meta["schedule_path"]),
        generate=generate, samples=samples,
        episode_end_day=meta["episode_end_day"],
    )

    report = build_report(env_state)
    lines = [report, "## Judge pass", "", f"- grader: `{model_name}` · samples: {samples}", ""]
    lines += ["| dimension / key | score |", "|---|---|"]
    for key, val in sorted(score.value.items()):
        lines.append(f"| {key} | {val} |")
    lines += ["", "### Justification", "", str(score.explanation), ""]
    if meta.get("debug_ever"):
        lines += ["> **debug_ever: true** — this session has used debug mode; "
                  "it is not blind evidence.", ""]
    text = "\n".join(lines)
    out = pathlib.Path(out)
    out.write_text(text, encoding="utf-8")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_dir")
    parser.add_argument("--model", required=True)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--out", default=None)
    parser.add_argument("--dimensions-dir", default=str(ROOT / "judge" / "dimensions"))
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be >= 1")
    session_dir = pathlib.Path(args.session_dir)
    out = pathlib.Path(args.out) if args.out else session_dir / "report.md"
    print(asyncio.run(score_session(
        session_dir, args.model, args.samples, out, pathlib.Path(args.dimensions_dir)
    )))


if __name__ == "__main__":
    main()
