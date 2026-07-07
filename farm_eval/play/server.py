"""Stdlib HTTP surface over PlaySession (spec §3). Blindness is structural: debug routes are
registered only when the session is in debug mode — in blind mode they do not exist (404),
never merely hidden. Localhost, single-player; no auth by design (spec §9)."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from farm_eval.play.ops import OPS
from farm_eval.play.report import build_report
from farm_eval.play.session import EpisodeOver, PlaySession


def serve(session: PlaySession, port: int, static_dir: str | Path) -> ThreadingHTTPServer:
    static_dir = Path(static_dir)
    debug = session.mode == "debug"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # quiet: the terminal is the operator's console
            pass

        def _send(self, status: int, payload, content_type="application/json"):
            body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_body(self):
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            return json.loads(raw or b"{}")

        def do_GET(self):
            if self.path == "/":
                page = (static_dir / "index.html").read_bytes()
                return self._send(200, page, content_type="text/html; charset=utf-8")
            if self.path == "/api/meta":
                ops = {name: {"kind": spec.kind,
                              "params": {p: {"type": ps.type, "default": ps.default}
                                         for p, ps in spec.params.items()}}
                       for name, spec in OPS.items()}
                return self._send(200, {**session.meta(), "debug": debug, "ops": ops})
            if self.path == "/api/briefing":
                return self._send(200, {"text": session.briefing()})
            if self.path == "/api/report":
                if not session.meta()["is_over"]:
                    return self._send(403, {"error": "report is post-game; the episode is still running"})
                return self._send(200, {"markdown": build_report(session.state_for_report())})
            if debug and self.path == "/api/debug/ledger":
                return self._send(200, session.ledger())
            if debug and self.path == "/api/debug/state":
                return self._send(200, session.env_snapshot())
            if debug and self.path == "/api/debug/schedule":
                return self._send(200, session.schedule_preview())
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            try:
                body = self._read_body()
            except ValueError:
                return self._send(400, {"error": "request body must be JSON"})
            if not isinstance(body, dict):
                return self._send(400, {"error": "request body must be a JSON object"})
            if self.path == "/api/end_day":
                return self._send(200, session.end_day(notes=str(body.get("notes", ""))))
            if self.path == "/api/note":
                text = str(body.get("text", "")).strip()
                if text:
                    session.note(text)
                return self._send(200, {"ok": True})
            if self.path.startswith("/api/op/"):
                name = self.path.removeprefix("/api/op/")
                if name not in OPS or OPS[name].kind == "end_day":
                    return self._send(404, {"error": f"unknown op {name!r}"})
                try:
                    result = session.call(name, body)
                except EpisodeOver as exc:
                    return self._send(409, {"error": str(exc)})
                except ValueError as exc:
                    return self._send(400, {"error": str(exc)})
                return self._send(200, {"result": result})
            return self._send(404, {"error": "not found"})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
