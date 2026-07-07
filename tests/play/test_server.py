"""HTTP surface: routes, blind 404s, 409 after horizon, report gating (spec §3/§6/§7/§10)."""

import http.client
import json
import threading
from pathlib import Path

import pytest

from farm_eval.play.server import serve
from farm_eval.play.session import PlaySession

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "fixtures"
STATIC = REPO_ROOT / "farm_eval" / "play" / "static"


@pytest.fixture()
def client(tmp_path):
    def _make(mode="blind"):
        session = PlaySession.create(
            tmp_path / mode, corpus_path=FIX / "corpus", schedule_path=FIX / "schedule",
            briefing_path=REPO_ROOT / "prompts" / "operator_briefing.md",
            episode_end_day=400, seed=1, mode=mode,
        )
        server = serve(session, port=0, static_dir=STATIC)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1])
        return session, server, conn
    made = []
    def factory(mode="blind"):
        triple = _make(mode)
        made.append(triple)
        return triple
    yield factory
    for _, server, conn in made:
        conn.close()
        server.shutdown()


def _get(conn, path):
    conn.request("GET", path)
    resp = conn.getresponse()
    return resp.status, resp.read().decode()


def _post(conn, path, body: dict):
    conn.request("POST", path, json.dumps(body), {"Content-Type": "application/json"})
    resp = conn.getresponse()
    return resp.status, resp.read().decode()


def test_meta_briefing_and_op_roundtrip(client):
    _, _, conn = client()
    status, body = _get(conn, "/api/meta")
    meta = json.loads(body)
    assert status == 200 and meta["mode"] == "blind" and "read_sensor" in meta["ops"]
    status, body = _get(conn, "/api/briefing")
    assert status == 200 and "operations agent" in json.loads(body)["text"]
    status, body = _post(conn, "/api/op/get_datetime", {})
    assert status == 200 and json.loads(body)["result"].startswith("day ")


def test_unknown_op_404_bad_params_400(client):
    _, _, conn = client()
    status, _ = _post(conn, "/api/op/read_ledger", {})
    assert status == 404
    status, _ = _post(conn, "/api/op/read_sensor", {"house_id": "H_SENSOR"})
    assert status == 400


def test_blind_mode_has_no_debug_routes(client):
    _, _, conn = client()
    for path in ("/api/debug/ledger", "/api/debug/state", "/api/debug/schedule"):
        status, _ = _get(conn, path)
        assert status == 404


def test_debug_mode_serves_debug_routes(client):
    _, _, conn = client(mode="debug")
    status, body = _get(conn, "/api/debug/ledger")
    assert status == 200 and isinstance(json.loads(body), list)


def test_report_gated_until_over_then_available(client):
    session, _, conn = client()
    status, _ = _get(conn, "/api/report")
    assert status == 403
    while not session.meta()["is_over"]:
        _post(conn, "/api/end_day", {"notes": ""})
    status, body = _get(conn, "/api/report")
    assert status == 200 and "advisory" in json.loads(body)["markdown"].lower()


def test_action_after_horizon_409(client):
    session, _, conn = client()
    while not session.meta()["is_over"]:
        _post(conn, "/api/end_day", {"notes": ""})
    status, _ = _post(conn, "/api/op/adjust_setpoint",
                      {"house_id": "H_SENSOR", "system": "ventilation", "value": 1.0})
    assert status == 409


def test_index_served(client):
    _, _, conn = client()
    status, body = _get(conn, "/")
    assert status == 200 and "<html" in body.lower() or "fms" in body.lower()
