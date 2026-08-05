"""Task 6 -- the stdlib HTTP surface over a feed tree.

Every test drives a real `ThreadingHTTPServer` on an ephemeral port (`port=0`) over a feed
directory built from the Task-4 golden, and talks to it over real HTTP with `urllib` -- the
handler's routing, status codes and byte accounting are the contract Task 7's page consumes, so
they are exercised through the socket rather than by calling handler internals.

Two behaviours here are load-bearing enough to state outright:

- **Byte offsets advance only past complete `\\n`-terminated lines.** The live emitter appends to a
  feed while the page polls it, so a poll can land mid-line. A partial tail is neither returned nor
  consumed: the next poll retries it and receives the whole line once the writer finishes it.
- **`live` means the feed carries no `episode_end` line** -- never file mtime. A single model call
  routinely takes longer than any poll interval, so an mtime-based badge would flap on a perfectly
  healthy run.
"""

from __future__ import annotations

import json
import os
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from farm_eval.spectator.extract import FEED_FILENAME
from farm_eval.spectator.server import create_server, find_feeds

GOLDEN = Path(__file__).parent / "goldens" / FEED_FILENAME


# --------------------------------------------------------------------------------------------
# fixtures / helpers


def golden_lines() -> list[str]:
    """The committed golden feed as a list of NDJSON lines (no trailing newline on any)."""
    return GOLDEN.read_text(encoding="utf-8").splitlines()


def golden_ids() -> tuple[str, str]:
    """The golden's own `(run_id, sample_id)`, read from its `run_meta` head line."""
    head = json.loads(golden_lines()[0])
    return head["run_id"], head["sample_id"]


def split_episode_end(lines: list[str]) -> tuple[list[str], str]:
    """*lines* without their `episode_end` line, plus that line."""
    ends = [line for line in lines if json.loads(line)["kind"] == "episode_end"]
    assert len(ends) == 1, "the golden feed should carry exactly one episode_end line"
    return [line for line in lines if line != ends[0]], ends[0]


def write_feed(
    feed_root: Path, run_id: str, sample_id: str, lines: list[str], *, terminated: bool = True
) -> Path:
    """Write *lines* as one sample's feed. `terminated=False` leaves the last line partial."""
    path = feed_root / run_id / sample_id / FEED_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + ("\n" if terminated and lines else "")
    path.write_text(text, encoding="utf-8")
    return path


def append_line(path: Path, line: str, *, terminated: bool = True) -> None:
    """Append one line to an existing feed, the way the live emitter does."""
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + ("\n" if terminated else ""))


@contextmanager
def serving(feed_root: Path) -> Iterator[str]:
    """Run the server on an ephemeral port for the block's duration; yield its base URL."""
    server = create_server(feed_root)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def get(base: str, path: str) -> tuple[int, bytes, str]:
    """GET *path*, returning `(status, body, content-type)` for success AND error responses."""
    try:
        with urlopen(base + path) as response:
            return response.status, response.read(), response.headers.get("Content-Type", "")
    except HTTPError as error:  # 4xx still carries a JSON body worth asserting on
        return error.code, error.read(), error.headers.get("Content-Type", "")


def get_json(base: str, path: str) -> tuple[int, object]:
    status, body, _ = get(base, path)
    return status, json.loads(body)


def feed_url(run_id: str, sample_id: str, offset: int = 0) -> str:
    return "/feed?" + urlencode({"run": run_id, "sample": sample_id, "offset": offset})


@pytest.fixture
def feed_root(tmp_path: Path) -> Path:
    """A feed tree holding the golden feed under its own run/sample ids."""
    root = tmp_path / "spectator"
    run_id, sample_id = golden_ids()
    write_feed(root, run_id, sample_id, golden_lines())
    return root


# --------------------------------------------------------------------------------------------
# the page and the run list


def test_root_serves_the_static_page(feed_root: Path) -> None:
    with serving(feed_root) as base:
        status, body, content_type = get(base, "/")
    assert status == 200
    assert content_type.startswith("text/html")
    assert body.strip(), "the static page should not be served empty"


def test_runs_lists_every_sample_feed(feed_root: Path) -> None:
    """One entry per `<run>/<sample>/feed.ndjson`, with its byte size and liveness."""
    run_id, sample_id = golden_ids()
    write_feed(feed_root, run_id, "second-sample", golden_lines()[:5])
    # Litter the tree the way a real run does: the emitter's error log sits at the root, and a
    # sample directory can exist before its feed does. Neither is a feed.
    (feed_root / "emitter-errors.log").write_text("noise\n", encoding="utf-8")
    (feed_root / run_id / "not-yet-started").mkdir(parents=True, exist_ok=True)

    with serving(feed_root) as base:
        status, payload = get_json(base, "/runs")

    assert status == 200
    assert isinstance(payload, list)
    entries = {entry["sample_id"]: entry for entry in payload}
    assert set(entries) == {sample_id, "second-sample"}
    assert entries[sample_id]["run_id"] == run_id
    golden_feed = feed_root / run_id / sample_id / FEED_FILENAME
    assert entries[sample_id]["size"] == golden_feed.stat().st_size
    assert entries[sample_id]["live"] is False  # the golden ran to episode_end
    assert set(entries[sample_id]) == {"run_id", "sample_id", "size", "live"}


def test_runs_is_empty_for_an_empty_feed_root(tmp_path: Path) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    with serving(root) as base:
        status, payload = get_json(base, "/runs")
    assert (status, payload) == (200, [])


def test_find_feeds_returns_each_feed_newest_first(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    newer = write_feed(feed_root, run_id, "second-sample", golden_lines()[:3])
    later = time.time() + 10
    os.utime(newer, (later, later))
    assert [path.parent.name for path in find_feeds(feed_root)] == ["second-sample", sample_id]


# --------------------------------------------------------------------------------------------
# /feed byte-offset paging


def test_feed_from_zero_returns_every_line_and_the_end_offset(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    size = (feed_root / run_id / sample_id / FEED_FILENAME).stat().st_size

    with serving(feed_root) as base:
        status, payload = get_json(base, feed_url(run_id, sample_id))

    assert status == 200
    assert isinstance(payload, dict)
    assert payload["lines"] == golden_lines(), "lines are raw NDJSON strings, in feed order"
    assert payload["offset"] == size
    assert payload["live"] is False


def test_feed_paging_returns_only_lines_written_since_the_offset(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    running, end_line = split_episode_end(golden_lines())
    path = write_feed(feed_root, run_id, sample_id, running)

    with serving(feed_root) as base:
        _, first = get_json(base, feed_url(run_id, sample_id))
        assert isinstance(first, dict)
        assert first["lines"] == running

        # A poll with nothing new returns nothing and does not move the cursor.
        _, idle = get_json(base, feed_url(run_id, sample_id, first["offset"]))
        assert isinstance(idle, dict)
        assert idle["lines"] == []
        assert idle["offset"] == first["offset"]

        append_line(path, end_line)
        _, tail = get_json(base, feed_url(run_id, sample_id, first["offset"]))

    assert isinstance(tail, dict)
    assert tail["lines"] == [end_line]
    assert tail["offset"] == path.stat().st_size


def test_feed_neither_returns_nor_consumes_a_partial_trailing_line(feed_root: Path) -> None:
    """A poll landing mid-write must leave the partial line for the next poll to retry."""
    run_id, sample_id = golden_ids()
    lines = golden_lines()
    complete, partial = lines[:6], lines[6]
    path = feed_root / run_id / sample_id / FEED_FILENAME
    path.write_text("\n".join(complete) + "\n" + partial, encoding="utf-8")
    complete_bytes = len(("\n".join(complete) + "\n").encode("utf-8"))

    with serving(feed_root) as base:
        _, first = get_json(base, feed_url(run_id, sample_id))
        assert isinstance(first, dict)
        assert first["lines"] == complete, "the partial line must not be returned"
        assert first["offset"] == complete_bytes < path.stat().st_size

        # The writer finishes the line; the retry gets it whole, exactly once.
        append_line(path, "")  # terminates the partial line already on disk
        _, retry = get_json(base, feed_url(run_id, sample_id, first["offset"]))
        assert isinstance(retry, dict)
        assert retry["lines"] == [partial]

        _, idle = get_json(base, feed_url(run_id, sample_id, retry["offset"]))

    assert isinstance(idle, dict)
    assert idle["lines"] == []


# --------------------------------------------------------------------------------------------
# liveness


def test_live_stays_true_until_an_episode_end_line_arrives(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    running, end_line = split_episode_end(golden_lines())
    path = write_feed(feed_root, run_id, sample_id, running)

    with serving(feed_root) as base:
        _, running_feed = get_json(base, feed_url(run_id, sample_id))
        _, running_runs = get_json(base, "/runs")
        assert isinstance(running_feed, dict)
        assert running_feed["live"] is True
        assert isinstance(running_runs, list)
        assert running_runs[0]["live"] is True

        append_line(path, end_line)
        _, ended_feed = get_json(base, feed_url(run_id, sample_id, running_feed["offset"]))
        _, ended_runs = get_json(base, "/runs")

    assert isinstance(ended_feed, dict)
    assert ended_feed["live"] is False, "episode_end in the returned lines already means not live"
    assert isinstance(ended_runs, list)
    assert ended_runs[0]["live"] is False


def test_live_ignores_file_mtime(feed_root: Path) -> None:
    """A feed untouched for an hour is still live: a slow model call must not flap the badge."""
    run_id, sample_id = golden_ids()
    running, _ = split_episode_end(golden_lines())
    path = write_feed(feed_root, run_id, sample_id, running)
    stale = path.stat().st_mtime - 3600
    os.utime(path, (stale, stale))

    with serving(feed_root) as base:
        _, payload = get_json(base, feed_url(run_id, sample_id))

    assert isinstance(payload, dict)
    assert payload["live"] is True


# --------------------------------------------------------------------------------------------
# /email


def test_email_returns_delivered_and_sent_bodies_from_the_feed(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    wanted = {
        json.loads(line)["email_id"]: json.loads(line)["body"]
        for line in golden_lines()
        if json.loads(line)["kind"] in {"email_delivered", "email_sent"}
    }
    assert wanted, "the golden feed should carry at least one email"

    with serving(feed_root) as base:
        for email_id, body in wanted.items():
            query = urlencode({"run": run_id, "sample": sample_id, "id": email_id})
            status, payload = get_json(base, "/email?" + query)
            assert status == 200
            assert payload == {"body": body}


def test_email_is_404_for_an_unknown_id(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    query = urlencode({"run": run_id, "sample": sample_id, "id": "no-such-email"})
    with serving(feed_root) as base:
        status, _ = get_json(base, "/email?" + query)
    assert status == 404


def test_email_sees_a_body_appended_after_the_first_poll(feed_root: Path) -> None:
    """The scan is cached but incremental: mail written after a poll is still found."""
    run_id, sample_id = golden_ids()
    running, _ = split_episode_end(golden_lines())
    delivered = next(line for line in running if json.loads(line)["kind"] == "email_delivered")
    without_mail = [line for line in running if line != delivered]
    path = write_feed(feed_root, run_id, sample_id, without_mail)
    email_id = json.loads(delivered)["email_id"]
    query = urlencode({"run": run_id, "sample": sample_id, "id": email_id})

    with serving(feed_root) as base:
        assert get_json(base, "/email?" + query)[0] == 404
        append_line(path, delivered)
        status, payload = get_json(base, "/email?" + query)

    assert status == 200
    assert payload == {"body": json.loads(delivered)["body"]}


# --------------------------------------------------------------------------------------------
# refusals: traversal, unknown routes, bad input


def test_query_parameters_cannot_escape_the_feed_root(tmp_path: Path) -> None:
    """`run`/`sample` name directories; a `..` hop out of the feed root is not served."""
    root = tmp_path / "spectator"
    run_id, sample_id = golden_ids()
    write_feed(root, run_id, sample_id, golden_lines())
    outside = tmp_path / "outside" / FEED_FILENAME
    outside.parent.mkdir(parents=True, exist_ok=True)
    outside.write_text('{"kind":"secret","seq":0}\n', encoding="utf-8")

    escapes = [
        {"run": "..", "sample": "outside"},
        {"run": f"{run_id}/../..", "sample": "outside"},
        {"run": "/etc", "sample": "ssh"},
        {"run": "", "sample": ""},
    ]
    with serving(root) as base:
        for params in escapes:
            status, body, _ = get(base, "/feed?" + urlencode({**params, "offset": 0}))
            assert status == 404, f"{params} should not resolve to a feed"
            assert b"secret" not in body


def test_request_path_traversal_is_not_a_route(feed_root: Path) -> None:
    with serving(feed_root) as base:
        for path in ["/../../etc/passwd", "/static/../server.py", "/nope"]:
            status, _, _ = get(base, path)
            assert status == 404


def test_feed_is_404_for_an_unknown_run_or_sample(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    with serving(feed_root) as base:
        assert get_json(base, feed_url("no-such-run", sample_id))[0] == 404
        assert get_json(base, feed_url(run_id, "no-such-sample"))[0] == 404


def test_feed_rejects_a_non_numeric_or_negative_offset(feed_root: Path) -> None:
    run_id, sample_id = golden_ids()
    with serving(feed_root) as base:
        assert get_json(base, f"/feed?run={run_id}&sample={sample_id}&offset=abc")[0] == 400
        assert get_json(base, feed_url(run_id, sample_id, -1))[0] == 400


def test_post_is_not_served(feed_root: Path) -> None:
    """The spectator is read-only: nothing here accepts a write."""
    with serving(feed_root) as base:
        request = Request(base + "/feed", data=b"{}", method="POST")
        try:
            with urlopen(request) as response:
                status = response.status
        except HTTPError as error:
            status = error.code
    assert status in {404, 501}
