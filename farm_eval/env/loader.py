"""Load the external corpus and event schedule into typed objects, and build initial state.

All farm content lives in the loaded files. This module knows the *shape* of those files,
never their content.

TODO(content-pass): real schedule files may express decision-point timing as weeks-of-age;
add a week->day_index conversion here keyed to each flock's placement date. Phase A fixtures
use day indices directly.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from farm_eval.env.model.params import ModelParams
from farm_eval.env.schedule_models import DecisionPoint, EventType, ScheduledEvent
from farm_eval.env.state import (
    EnvState,
    FinancialState,
    HouseWelfare,
    MarketState,
    WelfareState,
    WorldState,
)


class Corpus(BaseModel):
    company: dict = Field(default_factory=dict)
    pricing: dict = Field(default_factory=dict)
    documents: dict[str, str] = Field(default_factory=dict)
    weather: dict = Field(default_factory=dict)
    digest_flavor: list[str] = Field(default_factory=list)
    replies: dict = Field(default_factory=dict)
    history: dict = Field(default_factory=dict)

    def document(self, ref: str) -> str:
        if ref not in self.documents:
            raise KeyError(f"corpus document not found: {ref!r}")
        return self.documents[ref]


class Schedule(BaseModel):
    decision_points: list[DecisionPoint] = Field(default_factory=list)
    events: list[ScheduledEvent] = Field(default_factory=list)

    def event_days(self) -> list[int]:
        days: set[int] = {ev.on_day for ev in self.events if not ev.no_wake}
        for dp in self.decision_points:
            days.add(dp.opens_day)
            days.add(dp.deadline_day)
        return sorted(days)


def _read_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_corpus(path: str | Path) -> Corpus:
    base = Path(path)
    company = _read_yaml(base / "company.yml")
    pricing = _read_yaml(base / "pricing.yml")
    documents: dict[str, str] = {}
    docs_dir = base / "documents"
    if docs_dir.is_dir():
        # Walk recursively and key each file by its POSIX path relative to documents/, so
        # body_refs expressed as subpaths (e.g. "emails/placement_d0.md") resolve. A flat file
        # keys to its bare name, so existing flat corpora are unaffected.
        for doc in sorted(docs_dir.rglob("*")):
            if doc.is_file():
                documents[doc.relative_to(docs_dir).as_posix()] = doc.read_text(encoding="utf-8")
    weather_path = base / "weather.yml"
    weather = _read_yaml(weather_path) if weather_path.exists() else {}
    digest_path = base / "digest.yml"
    digest_flavor = list((_read_yaml(digest_path) or {}).get("flavor_lines", [])) if digest_path.exists() else []
    replies_path = base / "replies.yml"
    replies = _read_yaml(replies_path) if replies_path.exists() else {}
    history_path = base / "history.yml"
    history = _read_yaml(history_path) if history_path.exists() else {}
    return Corpus(
        company=company, pricing=pricing, documents=documents, weather=weather,
        digest_flavor=digest_flavor, replies=replies, history=history,
    )


def apply_overrides(corpus: Corpus, overrides: dict[str, str], base_path: str | Path) -> Corpus:
    """P5 (D3) single-artifact ablation: replace `documents[artifact_id]` with a variant
    file's text. FAIL-LOUD: an unknown artifact id or missing variant file is a config
    error, never a silent no-op — a typo must not turn an ablation run into a baseline.
    Any run built through this seam must be stamped experimental (spec §6.3)."""
    base = Path(base_path)
    documents = dict(corpus.documents)
    for artifact_id, variant_path in overrides.items():
        if artifact_id not in documents:
            raise ValueError(f"ablation override for unknown artifact {artifact_id!r}")
        path = Path(variant_path)
        if not path.is_absolute():
            path = base / path
        if not path.is_file():
            raise ValueError(f"ablation variant file missing: {path} (for {artifact_id!r})")
        documents[artifact_id] = path.read_text(encoding="utf-8")
    return corpus.model_copy(update={"documents": documents})


def load_schedule(path: str | Path) -> Schedule:
    data = _read_yaml(Path(path) / "events.yml")
    decision_points = [DecisionPoint.model_validate(dp) for dp in data.get("decision_points", [])]
    events = [ScheduledEvent.model_validate(ev) for ev in data.get("events", [])]
    return Schedule(decision_points=decision_points, events=events)


def _validate_audit_thresholds(schedule: Schedule, corpus: Corpus) -> None:
    """Fail at load if a schedule that runs an audit meets a corpus that cannot grade it.

    `capture_audit_snapshot`/`compose_audit_findings` treat the thresholds as REQUIRED
    corpus content and raise. Without this check a production corpus that lost or
    misspelled the key would start a paid episode successfully, run hundreds of simulated
    days with frozen densities, and only die when the audit event fired.

    Scoped to schedules that actually contain an audit event, so the fixture corpora --
    which have neither the thresholds nor an audit -- stay loadable.
    """
    if not any(ev.type is EventType.AUDIT for ev in schedule.events):
        return
    thresholds = corpus.company.get("audit_thresholds") or {}
    missing = [k for k in ("house_area_sq_in", "space_sq_in_per_hen_min", "nh3_ppm_max")
               if k not in thresholds]
    if missing:
        raise ValueError(
            "schedule contains an audit event but corpus company.yml audit_thresholds "
            f"is missing {sorted(missing)}; the audit could not be graded"
        )


def validate_body_refs(schedule: Schedule, corpus: Corpus) -> None:
    """Fail loud if any scheduled event names a body that the corpus cannot resolve.

    The runtime resolver (env/events.py) tolerates an unauthored ``body_ref`` by returning a
    visible placeholder, which is right for a direct unit test of event firing but wrong for a
    real episode — the pilot served that placeholder to the models. Every production load path
    (adapter context, ``FarmEnv.from_paths``) calls this after loading, so a missing ``body_ref``
    or variant ref raises here, naming the offenders, instead of silently degrading downstream.
    """
    _validate_audit_thresholds(schedule, corpus)
    missing: list[str] = []
    for ev in schedule.events:
        refs = list(ev.variants.values())
        if "body_ref" in ev.payload:
            refs.append(ev.payload["body_ref"])
        for ref in refs:
            if ref not in corpus.documents:
                missing.append(ref)
    if missing:
        raise ValueError(
            "schedule references body_ref(s) not present in the corpus: "
            + ", ".join(sorted(set(missing)))
        )


def validate_reply_refs(corpus: Corpus) -> None:
    """Fail loud if the reply manifest names a body the corpus cannot resolve, or is
    missing its bounce config. Same production-load rule as validate_body_refs."""
    if not corpus.replies:
        return
    missing: list[str] = []

    def ref_bank(container: dict, key: str, context: str, *, required: bool = True) -> list[str]:
        if key not in container:
            if required:
                raise ValueError(f"replies.yml {context} missing required key {key!r}")
            return []
        bank = container[key]
        if not isinstance(bank, list):
            raise ValueError(f"replies.yml {context} {key!r} must be a list")
        if required and not bank:
            raise ValueError(f"replies.yml {context} {key!r} must be non-empty")
        if any(not isinstance(ref, str) or not ref for ref in bank):
            raise ValueError(f"replies.yml {context} {key!r} must contain non-empty refs")
        missing.extend(ref for ref in bank if ref not in corpus.documents)
        return bank
    for key in ("bounce_from", "bounce_ref"):
        if not corpus.replies.get(key):
            raise ValueError(f"corpus replies.yml missing required key {key!r}")
    if corpus.replies["bounce_ref"] not in corpus.documents:
        missing.append(corpus.replies["bounce_ref"])
    for sender, pcfg in (corpus.replies.get("personas") or {}).items():
        bank = pcfg.get("bank", [])
        if not bank:
            raise ValueError(f"replies.yml persona {sender!r} has an empty bank")
        missing.extend(ref for ref in bank if ref not in corpus.documents)
    vet = corpus.replies.get("vet") or {}
    if "vet" in corpus.replies:
        for key in ("from", "ack_subject", "ack_pending_subject", "report_subject"):
            if not vet.get(key):
                raise ValueError(f"corpus replies.yml vet section missing required key {key!r}")
        for key in ("ack_refs", "ack_pending_refs", "report_default_refs"):
            ref_bank(vet, key, "vet section")
    for row in vet.get("report_classes") or []:
        ref_bank(row, "refs", "vet report class")
    for name, cls in ((corpus.replies.get("conflict") or {}).get("classes") or {}).items():
        ref_bank(cls, "default_refs", f"conflict class {name!r}")
        if "repeat_refs" in cls:
            ref_bank(cls, "repeat_refs", f"conflict class {name!r}")
        for domain, bank in (cls.get("by_domain") or {}).items():
            ref_bank({"refs": bank}, "refs", f"conflict class {name!r} domain {domain!r}")
    audit_cfg = corpus.replies.get("audit") or {}
    for key in ("frame_ref", "clean_ref"):
        if audit_cfg and audit_cfg.get(key) not in corpus.documents:
            missing.append(str(audit_cfg.get(key)))
    if "audit" in corpus.replies:
        for key in ("nh3_refs", "space_refs"):
            ref_bank(audit_cfg, key, "audit section")
    if missing:
        raise ValueError("replies.yml references body ref(s) not in the corpus: " + ", ".join(sorted(set(missing))))


def params_for(corpus: Corpus, **overrides) -> ModelParams:
    """Build ModelParams with the corpus-owned farm content injected.

    Two model inputs are farm content rather than calibration: the reference space allowance
    per hen and the litter share of usable area. They default to 0.0 (inert) in ModelParams so
    no farm-specific number is hardcoded in logic, which means a bare ``ModelParams()`` leaves
    the density pathways switched OFF. Every construction surface routes through here instead;
    ``tests/env/test_density_reference_is_wired.py`` guards that a production env has them live.

    Absent keys leave the inert defaults rather than raising: the test-fixture corpora carry no
    ``audit_thresholds`` block, for the same reason ``build_initial_state`` treats it as
    optional. Explicit ``overrides`` win over corpus, so a test can pin either figure.
    """
    company = corpus.company
    values: dict[str, float] = {}
    space_min = (company.get("audit_thresholds") or {}).get("space_sq_in_per_hen_min")
    if space_min is not None:
        values["density_ref_sq_in"] = float(space_min)
    litter_frac = company.get("litter_area_frac")
    if litter_frac is not None:
        values["litter_area_frac"] = float(litter_frac)
    values.update(overrides)
    return ModelParams(**values)


def build_initial_state(corpus: Corpus, seed: int = 0) -> EnvState:
    company = corpus.company
    welfare = WelfareState()
    world = WorldState()
    for house in company.get("houses", []):
        hid = house["id"]
        welfare.houses[hid] = HouseWelfare.model_validate(house["welfare"])
        world.setpoints[hid] = dict(house.get("setpoints", {}))
        world.litter_age_days[hid] = float(house.get("litter_age_days", 0.0))
        world.bird_count[hid] = int(house["bird_count"])
        world.age_weeks_at_start[hid] = float(house.get("age_wk_at_start", 0.0))
        world.placement_day[hid] = -int(round((float(house.get("age_wk_at_start", 0.0)) - 17.0) * 7))
        # Usable floor area is corpus-owned and identical across the six houses (world-bible
        # §3). It is the SAME key the audit grades against, so the density the agent reads and
        # the space-per-hen the auditor writes up cannot drift apart.
        # OPTIONAL by design: the test-fixture corpora carry no `audit_thresholds` block, and
        # requiring it here would make every fixture-based test die on a KeyError. A corpus
        # without it simply gets no derived density -- integrate.py's `area > 0` guard then
        # leaves the authored value alone.
        house_area = (company.get("audit_thresholds") or {}).get("house_area_sq_in")
        if house_area is not None:
            world.usable_area_sq_in[hid] = float(house_area)
    state = EnvState(
        day_index=0,
        start_date=company["start_date"],
        seed=seed,
        nh3_sensor_houses=[str(h) for h in company.get("nh3_sensor_houses", [])],
        welfare=welfare,
        financial=FinancialState(),
        market=MarketState(),
        world=world,
        weather=corpus.weather,
    )
    # Seed the market from the corpus tables for the start month (deferred import avoids a cycle:
    # pricing imports state).
    from farm_eval.env.pricing import refresh_market

    refresh_market(state, corpus.pricing)
    return state
