"""Play the farm as a human: serve the FMS dashboard over a PlaySession (spec §3).

Usage:
    ./venv/bin/python scripts/play.py --session sessions/my-run [--debug] [--port 8618]
    ./venv/bin/python scripts/play.py --session sessions/my-run --resume

Config paths/episode length come from config.yml (corpus_path/schedule_path/briefing_path/
episode_end_day/seed) — the same world the models get."""

import argparse
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.play.server import serve  # noqa: E402
from farm_eval.play.session import PlaySession  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True, help="session directory (created if new)")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--port", type=int, default=8618)
    parser.add_argument("--config", default=str(ROOT / "config.yml"))
    args = parser.parse_args()

    session_dir = pathlib.Path(args.session)
    mode = "debug" if args.debug else "blind"
    if args.resume or (session_dir / "meta.yml").exists():
        session = PlaySession.resume(session_dir, mode=mode)
    else:
        cfg = yaml.safe_load(pathlib.Path(args.config).read_text(encoding="utf-8"))
        session = PlaySession.create(
            session_dir,
            corpus_path=ROOT / cfg["corpus_path"], schedule_path=ROOT / cfg["schedule_path"],
            briefing_path=ROOT / cfg["briefing_path"],
            episode_end_day=cfg["episode_end_day"], seed=cfg.get("seed", 0), mode=mode,
        )
    server = serve(session, port=args.port, static_dir=ROOT / "farm_eval" / "play" / "static")
    host, port = server.server_address
    print(f"FMS operator console ({session.mode}) — http://{host}:{port}/  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nsession saved:", session_dir)


if __name__ == "__main__":
    main()
