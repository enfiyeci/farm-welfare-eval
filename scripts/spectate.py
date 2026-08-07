"""Serve the Henhouse spectator dashboard over a feed directory (spec §6).

Usage:
    ./venv/bin/python scripts/spectate.py --live spectator          # follow a run as it happens
    ./venv/bin/python scripts/spectate.py --log logs/<run>.eval     # replay a recorded run
    FARM_SPECTATOR_DIR=spectator ./venv/bin/python scripts/spectate.py   # --live defaults to it

`--live` serves the directory the emitter appends its per-sample feeds to, so the page follows a
run in progress (start it before or during the run — feeds appear as they are written). `--log`
replays a recorded `.eval` through the extractor into a temporary feed directory and serves that;
the temporary directory goes away when the server stops.

A log the extractor cannot reconstruct is reported as one plain paragraph on stderr with a nonzero
exit, never a traceback: it is a property of the log, not a crash. (The archived
`docs/probes/pilot-2026-07-12-artifacts/` pilot is a known, documented unreplayable case.)
"""

import argparse
import os
import pathlib
import sys
import tempfile
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from farm_eval.spectator.emitter import SPECTATOR_DIR_ENV  # noqa: E402
from farm_eval.spectator.extract import FeedExtractionError, extract_feed  # noqa: E402
from farm_eval.spectator.server import create_server, find_feeds  # noqa: E402

#: One past the play server's 8618, so a spectator and an operator console can run side by side.
DEFAULT_PORT = 8619


def page_url(host: str, port: int, feed_root: pathlib.Path) -> str:
    """The URL to open. A lone feed is named in the query so the page needs no picking."""
    url = f"http://{host}:{port}/"
    feeds = find_feeds(feed_root)
    if len(feeds) == 1:
        run_id = quote(feeds[0].parent.parent.name)
        sample_id = quote(feeds[0].parent.name)
        url += f"?run={run_id}&sample={sample_id}"
    return url


def serve(feed_root: pathlib.Path, port: int) -> None:
    server = create_server(feed_root, port=port)
    host, bound_port = server.server_address[:2]
    print(f"Henhouse spectator — {page_url(host, bound_port, feed_root)}  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--live", help=f"feed directory the emitter writes into (default: ${SPECTATOR_DIR_ENV})"
    )
    source.add_argument("--log", help="recorded .eval log to replay")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    if args.log:
        with tempfile.TemporaryDirectory(prefix="henhouse-spectator-") as tmp:
            feed_root = pathlib.Path(tmp)
            try:
                feeds = extract_feed(args.log, feed_root)
            except (FeedExtractionError, ValueError, OSError) as error:
                sys.stderr.write(f"spectate: {error}\n")
                raise SystemExit(1) from None
            print(f"replayed {len(feeds)} sample feed(s) from {args.log}")
            serve(feed_root, args.port)
        return

    live = args.live or os.environ.get(SPECTATOR_DIR_ENV)
    if not live:
        parser.error(
            f"nothing to serve: pass --live <dir> or --log <path.eval>, "
            f"or set {SPECTATOR_DIR_ENV}"
        )
    feed_root = pathlib.Path(live)
    if not feed_root.is_dir():
        # Live mode legitimately starts before the run does, so this is a note, not a refusal.
        print(
            f"note: {feed_root} does not exist yet — feeds appear once a run writes them",
            file=sys.stderr,
        )
    serve(feed_root, args.port)


if __name__ == "__main__":
    main()
