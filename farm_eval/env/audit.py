"""Audit-as-process (round-3): audit-day welfare snapshot + deterministic findings letter.

The snapshot is captured when the `type: audit` event fires (audit morning), so the
findings letter — composed later via the `composer: audit_findings` payload — reflects
what the auditor saw ON AUDIT DAY, not the state at delivery time. Composition is a pure
function of (snapshot, corpus): per-metric authored fragments fire only on threshold
breaches, so every claim in the letter is true in every run (spec truthfulness rule).
Same pattern as build_digest: deterministic state-conditioned text, no RNG, no LLM.

Space allowance is derived at snapshot time from the corpus-owned physical house area /
LIVE bird count. The UEP figure is a FLOOR: a violation is sq in/hen BELOW the minimum.
"""

from __future__ import annotations

from farm_eval.env.density import space_sq_in_per_hen
from farm_eval.env.loader import Corpus
from farm_eval.env.state import EnvState


def capture_audit_snapshot(state: EnvState, corpus: Corpus) -> None:
    corpus_area = float(corpus.company["audit_thresholds"]["house_area_sq_in"])
    snap: dict[str, dict[str, float]] = {}
    for hid, hw in state.welfare.houses.items():
        birds = state.world.bird_count.get(hid, 0)
        if birds <= 0:
            continue  # empty/depopulated house: no flock findings to record
        row = {
            "ammonia_ppm": hw.ammonia_ppm,
            "litter_moisture": hw.litter_moisture,
            "space_sq_in_per_hen": space_sq_in_per_hen(
                # Prefer the LIVE per-house area so a usable-area retrofit shows up at
                # audit. Falls back to the corpus constant for states serialized before
                # world.usable_area_sq_in existed (the pinned pilot replay artifacts).
                # `.get(hid, corpus_area)`, NOT `... or corpus_area`: `or` treats a real
                # 0.0 as missing. FarmEnv backfills this dict at construction, so state is
                # authoritative and the corpus value is only reached for a house the
                # backfill could not resolve -- the two readers cannot disagree.
                state.world.usable_area_sq_in.get(hid, corpus_area),
                birds,
            ),
        }
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
    nh3_ordinal = 0
    space_ordinal = 0
    for hid in sorted(state.audit_snapshot):
        row = state.audit_snapshot[hid]
        nh3_shown = round(row.get("ammonia_ppm", 0.0), 1)
        if nh3_shown > nh3_max:
            bank = cfg["nh3_refs"]
            findings.append(
                corpus.document(bank[nh3_ordinal % len(bank)])
                .replace("HOUSE_ID", hid)
                .replace("NH3_VALUE", f"{nh3_shown:.1f}")
            )
            nh3_ordinal += 1
        space = row.get("space_sq_in_per_hen")
        space_shown = round(space, 1) if space is not None else None
        if space_shown is not None and space_shown < space_min:
            bank = cfg["space_refs"]
            findings.append(
                corpus.document(bank[space_ordinal % len(bank)])
                .replace("HOUSE_ID", hid)
                .replace("SPACE_VALUE", f"{space_shown:.1f}")
            )
            space_ordinal += 1
    block = "\n\n".join(findings) if findings else corpus.document(cfg["clean_ref"])
    return corpus.document(cfg["frame_ref"]).replace("FINDINGS_BLOCK", block)
