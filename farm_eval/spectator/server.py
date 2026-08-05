"""Stdlib HTTP surface over a spectator feed tree (spec §6), in the pattern of `scripts/play.py`.

One server serves both entry points, because both produce the same thing: a tree of per-sample
feeds at `<feed_root>/<run_id>/<sample_id>/feed.ndjson`, written live by the emitter or all at
once by the replay extractor. The page is one implementation for the same reason.

    GET /                                        -> static/index.html
    GET /runs                                    -> [{run_id, sample_id, size, live}, ...]
    GET /feed?run=&sample=&offset=<bytes>        -> {"lines": [...], "offset": N, "live": bool}
    GET /email?run=&sample=&id=<email_id>        -> {"body": "..."}

Everything else is a 404. Localhost, single viewer, read-only; no auth by design (like the play
server), and no writes of any kind — the spectator only ever reads feed files.

Four things here are contracts rather than choices.

**Offsets are BYTE offsets that advance only past complete `\\n`-terminated lines.** The page polls
a file another process is appending to, so a poll can land mid-line. A partial tail is neither
returned nor consumed: the page's cursor stays before it and the next poll returns the whole line
once the writer has finished it. (The emitter's side of the same contract: it appends whole lines
and flushes, never partial ones — so a partial tail only ever means "mid-write", never "corrupt".)

**`live` means the feed carries no `episode_end` line** — never file mtime. A single model call
routinely takes longer than any poll interval, so an mtime-based badge would flap on a healthy run.
`episode_end` is the one signal that says the sample is actually over.

**`lines` are raw NDJSON strings, not decoded objects.** The server is a byte pump: it does not
parse or validate what it serves, so a feed written by a newer emitter renders instead of 400-ing,
and a half-written file can never make the page's poll fail. `parse_feed_line` lives on the reading
side (the page does `JSON.parse`; tests use `parse_feed_line`).

**`run`/`sample` name directories and are resolved inside `feed_root`.** They arrive as query
parameters, so a `..` hop or an absolute path is refused (404) rather than served — the same
untrusted-path discipline any static file server needs.

Per-feed scanning (the `/email` body map and the `episode_end` flag) is cached and INCREMENTAL:
feeds are append-only, so each poll re-reads only the bytes appended since the last scan. That is
what keeps a 1 Hz poll on a long run cheap without ever consulting mtime.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

from farm_eval.spectator.extract import FEED_FILENAME

#: The page and its assets; Task 7 owns the file's contents.
STATIC_DIR = Path(__file__).resolve().parent / "static"

#: Feed event kinds whose bodies `/email` serves. Bodies travel in the feed (spec §3) — they are
#: never resolved from `corpus/` at view time, and sent-mail bodies exist nowhere else.
_EMAIL_KINDS = frozenset({"email_delivered", "email_sent"})

#: The one kind that ends a sample. Its presence anywhere in the feed clears `live`.
_END_KIND = "episode_end"


def _param(query: dict[str, list[str]], name: str) -> str:
    """The first value of *name*, or `""` when absent — repeated parameters are not a feature."""
    values = query.get(name) or []
    return values[0] if values else ""


def find_feeds(feed_root: Path) -> list[Path]:
    """Every per-sample feed under *feed_root*, newest first.

    Newest-first is by mtime, which is display ordering only — it never decides liveness. Anything
    in the tree that is not a `<run>/<sample>/feed.ndjson` file (the emitter's error log, a sample
    directory whose run has not written a line yet) is simply not a feed.
    """
    feeds = [path for path in feed_root.glob(f"*/*/{FEED_FILENAME}") if path.is_file()]
    return sorted(feeds, key=lambda path: path.stat().st_mtime, reverse=True)


def complete_lines(data: bytes) -> tuple[list[str], int]:
    """The complete `\\n`-terminated lines in *data*, and how many bytes they occupy.

    A trailing fragment is reported by neither: the caller advances its cursor by the returned byte
    count, which leaves the fragment to be re-read whole on the next pass. Splitting on `\\n` also
    means the decoded slice always ends on a character boundary.

    The split is on `"\\n"` and nothing else, because `str.splitlines()` would break a line that a
    feed legitimately contains. `dump_feed_line` writes with `json.dumps(ensure_ascii=False)`, which
    escapes every C0 control (`\\v`, `\\f`, `\\r`, `\\x1c`-`\\x1e`) but NOT `U+0085`, `U+2028` or
    `U+2029` — all three of which `splitlines()` treats as breaks. A model sentence or an email
    body carrying one is written literally inside its JSON string, on ONE physical NDJSON line;
    `splitlines()` would tear it into two unparseable fragments, which the page cannot render,
    `_absorb` silently drops (an affected `episode_end` would leave the LIVE badge stuck on), and
    `/email` never indexes. The empty string `split` leaves after the final `\\n` is dropped by the
    `if line` filter, as is any blank line.
    """
    end = data.rfind(b"\n") + 1
    if end == 0:
        return [], 0
    text = data[:end].decode("utf-8")
    return [line for line in text.split("\n") if line], end


def read_lines(path: Path, offset: int) -> tuple[list[str], int]:
    """Complete lines of *path* from *offset* on, plus the offset the caller should poll next."""
    with path.open("rb") as handle:
        handle.seek(offset)
        lines, consumed = complete_lines(handle.read())
    return lines, offset + consumed


@dataclass
class _FeedScan:
    """What one feed says beyond its raw bytes, accumulated as the file grows."""

    scanned: int = 0
    emails: dict[str, str] = field(default_factory=dict)
    ended: bool = False

    def refresh(self, path: Path) -> None:
        """Absorb every complete line appended since the last refresh."""
        size = path.stat().st_size
        if size < self.scanned:  # the file was rewritten (a re-run extraction) — start over
            self.scanned, self.emails, self.ended = 0, {}, False
        if size == self.scanned:
            return
        with path.open("rb") as handle:
            handle.seek(self.scanned)
            lines, consumed = complete_lines(handle.read())
        self.scanned += consumed
        for line in lines:
            self._absorb(line)

    def _absorb(self, line: str) -> None:
        try:
            event = json.loads(line)
        except ValueError:
            return  # a feed the server cannot parse is still a feed it can serve
        if not isinstance(event, dict):
            return
        kind = event.get("kind")
        if kind == _END_KIND:
            self.ended = True
        elif kind in _EMAIL_KINDS:
            email_id = event.get("email_id")
            if email_id:  # an unaddressed sent mail has no id to look it up by
                self.emails[str(email_id)] = str(event.get("body", ""))


class _FeedStore:
    """Read access to one feed tree: path resolution and the cached per-feed scans."""

    def __init__(self, feed_root: Path) -> None:
        self.root = feed_root.resolve()
        self._scans: dict[Path, _FeedScan] = {}
        self._lock = threading.Lock()

    def path_for(self, run_id: str, sample_id: str) -> Path | None:
        """The feed file for one run/sample, or `None` when it escapes the root or is absent."""
        if not run_id or not sample_id:
            return None
        candidate = (self.root / run_id / sample_id / FEED_FILENAME).resolve()
        if not candidate.is_relative_to(self.root):
            return None
        return candidate if candidate.is_file() else None

    def scan(self, path: Path) -> _FeedScan:
        """The up-to-date scan of *path*. Serialized: viewers share one incremental read."""
        with self._lock:
            scan = self._scans.setdefault(path, _FeedScan())
            scan.refresh(path)
            return scan

    def runs(self) -> list[dict[str, Any]]:
        """One entry per feed in the tree, newest first."""
        entries = []
        for path in find_feeds(self.root):
            entries.append(
                {
                    "run_id": path.parent.parent.name,
                    "sample_id": path.parent.name,
                    "size": path.stat().st_size,
                    "live": not self.scan(path).ended,
                }
            )
        return entries


def create_server(
    feed_root: Path, host: str = "127.0.0.1", port: int = 0
) -> ThreadingHTTPServer:
    """An HTTP server over the feed tree at *feed_root*. `port=0` binds an ephemeral port.

    Returned unstarted: the caller runs `serve_forever()` and reads the bound address from
    `server.server_address` (which is how tests reach an ephemeral port).
    """
    store = _FeedStore(Path(feed_root))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # quiet: the terminal belongs to the operator
            pass

        def _send(self, status: int, payload, content_type="application/json"):
            body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            # A polled API must never be answered from a cache: a stale /runs or /feed would
            # freeze the page mid-run with no way to tell.
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _feed_path(self, query: dict[str, list[str]]) -> Path | None:
            return store.path_for(_param(query, "run"), _param(query, "sample"))

        def do_GET(self):
            url = urlsplit(self.path)
            query = parse_qs(url.query)

            if url.path == "/":
                page = STATIC_DIR / "index.html"
                if not page.is_file():
                    return self._send(404, {"error": "the spectator page is not installed"})
                return self._send(
                    200, page.read_bytes(), content_type="text/html; charset=utf-8"
                )

            if url.path == "/runs":
                return self._send(200, store.runs())

            if url.path == "/feed":
                path = self._feed_path(query)
                if path is None:
                    return self._send(404, {"error": "no feed for that run and sample"})
                raw = _param(query, "offset") or "0"
                try:
                    offset = int(raw)
                except ValueError:
                    return self._send(400, {"error": f"offset must be a byte count, got {raw!r}"})
                if offset < 0:
                    return self._send(400, {"error": "offset must not be negative"})
                lines, next_offset = read_lines(path, offset)
                # Scanned AFTER the read, so `live` covers at least the lines just returned: a
                # response carrying `episode_end` can never also claim the sample is live.
                return self._send(
                    200,
                    {"lines": lines, "offset": next_offset, "live": not store.scan(path).ended},
                )

            if url.path == "/email":
                path = self._feed_path(query)
                if path is None:
                    return self._send(404, {"error": "no feed for that run and sample"})
                email_id = _param(query, "id")
                body = store.scan(path).emails.get(email_id)
                if body is None:
                    return self._send(404, {"error": f"no email {email_id!r} in this feed"})
                return self._send(200, {"body": body})

            return self._send(404, {"error": "not found"})

    return ThreadingHTTPServer((host, port), Handler)
