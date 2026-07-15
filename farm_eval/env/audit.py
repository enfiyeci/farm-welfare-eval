"""Audit-as-process (round-3): audit-day welfare snapshot + deterministic findings letter.

The snapshot is captured when the `type: audit` event fires (audit morning), so the
findings letter — composed later via the `composer: audit_findings` payload — reflects
what the auditor saw ON AUDIT DAY, not the state at delivery time. Composition is a pure
function of (snapshot, corpus): per-metric authored fragments fire only on threshold
breaches, so every claim in the letter is true in every run (spec truthfulness rule).
Same pattern as build_digest: deterministic state-conditioned text, no RNG, no LLM.

Space allowance is derived at snapshot time from house area / LIVE bird count (area =
seeded stocking_density x placed count, both from corpus company houses) — the seeded
HouseWelfare.stocking_density is an initial value the integrator never updates, and the
UEP figure is a FLOOR: a violation is sq in/hen BELOW the minimum.
"""

from __future__ import annotations

from farm_eval.env.loader import Corpus
from farm_eval.env.state import EnvState


def capture_audit_snapshot(state: EnvState, corpus: Corpus) -> None:
    initial = {h["id"]: h for h in corpus.company.get("houses", [])}
    snap: dict[str, dict[str, float]] = {}
    for hid, hw in state.welfare.houses.items():
        birds = state.world.bird_count.get(hid, 0)
        if birds <= 0:
            continue  # empty/depopulated house: no flock findings to record
        row = {"ammonia_ppm": hw.ammonia_ppm, "litter_moisture": hw.litter_moisture}
        init = initial.get(hid)
        if init and init.get("bird_count"):
            area_sq_in = float(init["welfare"]["stocking_density"]) * float(init["bird_count"])
            row["space_sq_in_per_hen"] = area_sq_in / birds
        snap[hid] = row
    state.audit_snapshot = snap


def compose_audit_findings(state: EnvState, corpus: Corpus) -> str:
    if not state.audit_snapshot:
        # A letter without a snapshot would falsely assert a clean inspection that never
        # supplied observations — an ordering/config error, never a clean audit.
        raise ValueError("audit_findings composer fired without an audit snapshot "
                         "(is the type:audit event scheduled before the composer event?)")
    cfg = (corpus.replies or {}).get("audit") or {}
    # Thresholds are REQUIRED corpus content (world-bible §12) — a missing or misspelled
    # key must fail loud, never silently grade against a hidden code default.
    thresholds = corpus.company["audit_thresholds"]
    nh3_max = float(thresholds["nh3_ppm_max"])
    space_min = float(thresholds["space_sq_in_per_hen_min"])
    findings: list[str] = []
    for hid in sorted(state.audit_snapshot):
        row = state.audit_snapshot[hid]
        if row.get("ammonia_ppm", 0.0) > nh3_max:
            findings.append(
                corpus.document(cfg["nh3_ref"])
                .replace("HOUSE_ID", hid)
                .replace("NH3_VALUE", f"{row['ammonia_ppm']:.0f}")
            )
        space = row.get("space_sq_in_per_hen")
        if space is not None and space < space_min:
            findings.append(
                corpus.document(cfg["space_ref"])
                .replace("HOUSE_ID", hid)
                .replace("SPACE_VALUE", f"{space:.0f}")
            )
    block = "\n\n".join(findings) if findings else corpus.document(cfg["clean_ref"])
    return corpus.document(cfg["frame_ref"]).replace("FINDINGS_BLOCK", block)
