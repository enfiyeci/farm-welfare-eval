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

from farm_eval.env.schedule_models import DecisionPoint, ScheduledEvent
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

    def document(self, ref: str) -> str:
        if ref not in self.documents:
            raise KeyError(f"corpus document not found: {ref!r}")
        return self.documents[ref]


class Schedule(BaseModel):
    decision_points: list[DecisionPoint] = Field(default_factory=list)
    events: list[ScheduledEvent] = Field(default_factory=list)

    def event_days(self) -> list[int]:
        days: set[int] = {ev.on_day for ev in self.events}
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
    return Corpus(company=company, pricing=pricing, documents=documents, weather=weather)


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


def validate_body_refs(schedule: Schedule, corpus: Corpus) -> None:
    """Fail loud if any scheduled event names a body that the corpus cannot resolve.

    The runtime resolver (env/events.py) tolerates an unauthored ``body_ref`` by returning a
    visible placeholder, which is right for a direct unit test of event firing but wrong for a
    real episode — the pilot served that placeholder to the models. Every production load path
    (adapter context, ``FarmEnv.from_paths``) calls this after loading, so a missing ``body_ref``
    or variant ref raises here, naming the offenders, instead of silently degrading downstream.
    """
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
