"""Load the external corpus and event schedule into typed objects, and build initial state.

All farm content lives in the loaded files. This module knows the *shape* of those files,
never their content.

TODO(content-pass): real schedule files may express decision-point timing as weeks-of-age;
add a week->day_index conversion here keyed to each flock's placement date. Phase A fixtures
use day indices directly.
"""

from __future__ import annotations

import math
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode="after")
    def _check_variant_keys(self) -> "Schedule":
        """Every `variants` key must name something the resolver can actually select.

        `addressed`/`unaddressed` are the two statuses; a ladder rung name or a classified
        class name selects the OUTCOME-specific body (DP07's three-way follow-up, gap-3 ruling
        2026-08-19 — see `farm_eval.env.events._resolve_body`). A key that is none of those can
        never be chosen, so an author's typo would silently serve the generic body forever
        instead of the one they wrote. Only checked against DPs the schedule actually declares:
        an event pointing at an undeclared DP already degrades to `unaddressed` by design, and
        directly-constructed test schedules must stay constructible.

        `variant_on_state` (2026-08-27) adds the second half: a key may be composed as
        ``"<base>@<band>"``, where `<band>` must be one of the event's declared bands and
        `<base>` is validated exactly as above. A state-only event's keys are bare band names,
        and it must cover EVERY band — with no `variant_on_dp` there is nothing to fall back
        to, so an uncovered band would raise mid-episode instead of at load. `var` is checked
        against the numeric `HouseWelfare` fields here for the same reason: a typo'd metric name
        is an author error that must not wait for a live run to surface.
        """
        by_id = {dp.id: dp for dp in self.decision_points}
        bad: list[str] = []
        bad_bands: list[str] = []
        bad_vars: list[str] = []
        uncovered: list[str] = []
        numeric_house_fields = {
            name
            for name, f in HouseWelfare.model_fields.items()
            if f.annotation in (float, int)
        }
        for ev in self.events:
            vos = ev.variant_on_state
            band_keys = {b.key for b in vos.bands} if vos else set()
            if vos is not None:
                if vos.var not in numeric_house_fields:
                    bad_vars.append(f"day {ev.on_day}:{vos.var}")
                if ev.variant_on_dp is None:
                    missing = sorted(band_keys - set(ev.variants))
                    if missing:
                        uncovered.append(f"day {ev.on_day}:{','.join(missing)}")
            dp = by_id.get(ev.variant_on_dp or "")
            allowed = {"addressed", "unaddressed"}
            if dp is not None:
                allowed |= {rung.name for rung in (dp.signature.rungs or [])}
                allowed |= set(dp.signature.classes or {})
            label = dp.id if dp is not None else f"day {ev.on_day}"
            for k in ev.variants:
                base, sep, band = k.partition("@")
                if sep and band not in band_keys:
                    bad_bands.append(f"{label}:{k}")
                    continue
                if not sep and vos is not None and ev.variant_on_dp is None:
                    # A state-only event's keys ARE band keys.
                    if base not in band_keys:
                        bad_bands.append(f"{label}:{k}")
                    continue
                # `dp is None` = an event pointing at an undeclared DP; skipped by design.
                if dp is not None and base not in allowed:
                    bad.append(f"{dp.id}:{k}")
        if bad:
            raise ValueError(
                "variant key(s) name no status, rung or class of their decision point: "
                + ", ".join(sorted(set(bad)))
            )
        if bad_bands:
            raise ValueError(
                "variant key(s) name no declared variant_on_state band: "
                + ", ".join(sorted(set(bad_bands)))
            )
        if bad_vars:
            raise ValueError(
                "variant_on_state var(s) name no numeric HouseWelfare field: "
                + ", ".join(sorted(set(bad_vars)))
            )
        if uncovered:
            raise ValueError(
                "state-only variant event(s) leave a band with no body: "
                + ", ".join(sorted(set(uncovered)))
            )
        return self


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
    for domain, dcfg in (corpus.replies.get("domains") or {}).items():
        bank = dcfg.get("bank", [])
        if not bank:
            raise ValueError(f"replies.yml domain {domain!r} has an empty bank")
        missing.extend(ref for ref in bank if ref not in corpus.documents)
    vet = corpus.replies.get("vet") or {}
    if "vet" in corpus.replies:
        for key in ("from", "ack_subject", "ack_pending_subject", "report_subject"):
            if not vet.get(key):
                raise ValueError(f"corpus replies.yml vet section missing required key {key!r}")
        for key in ("ack_refs", "ack_pending_refs", "report_default_refs"):
            ref_bank(vet, key, "vet section")
        # report_bacterial_refs (D10): house-state-routed bacterial report bank (optional).
        if vet.get("report_bacterial_refs"):
            ref_bank(vet, "report_bacterial_refs", "vet section")
    for row in vet.get("report_classes") or []:
        ref_bank(row, "refs", "vet report class")
    for name, cls in ((corpus.replies.get("conflict") or {}).get("classes") or {}).items():
        ref_bank(cls, "default_refs", f"conflict class {name!r}")
        if "repeat_refs" in cls:
            ref_bank(cls, "repeat_refs", f"conflict class {name!r}")
        for domain, bank in (cls.get("by_domain") or {}).items():
            ref_bank({"refs": bank}, "refs", f"conflict class {name!r} domain {domain!r}")
    # DP13 egg-test result config (inline prose fragments — no body_ref documents). Fail loud
    # on a malformed section so a missing fragment surfaces at load, not at first delivery.
    if "egg_test" in corpus.replies:
        egg = corpus.replies.get("egg_test") or {}
        for key in ("from", "subject", "intro", "result_positive", "result_negative",
                    "protocol_counted", "protocol_offschedule", "cleared_line"):
            if not egg.get(key):
                raise ValueError(f"corpus replies.yml egg_test section missing required key {key!r}")
    # DP05 red-mite control correspondence (2026-08-26): the vet's treatment order, the
    # applicator's work order, and the post-course trap round. Same fail-loud rule as the vet
    # section — a missing body must surface at load, not at first delivery.
    if "mite_control" in corpus.replies:
        mite = corpus.replies.get("mite_control") or {}
        for key in ("from", "provider_from", "approval_subject", "provider_subject",
                    "follow_up_subject"):
            if not mite.get(key):
                raise ValueError(
                    f"corpus replies.yml mite_control section missing required key {key!r}"
                )
        for key in ("approval_ref", "provider_ref", "follow_up_controlled_ref",
                    "follow_up_persisting_ref"):
            ref = mite.get(key)
            if not isinstance(ref, str) or not ref:
                raise ValueError(
                    f"corpus replies.yml mite_control section missing required key {key!r}"
                )
            if ref not in corpus.documents:
                missing.append(ref)
    audit_cfg = corpus.replies.get("audit") or {}
    for key in ("frame_ref", "clean_ref"):
        if audit_cfg and audit_cfg.get(key) not in corpus.documents:
            missing.append(str(audit_cfg.get(key)))
    if "audit" in corpus.replies:
        for key in ("nh3_refs", "space_refs"):
            ref_bank(audit_cfg, key, "audit section")
    tool_acks = corpus.replies.get("tool_acks") or {}
    if tool_acks:
        ref = tool_acks.get("log_treatment_withdrawal_ref")
        if not isinstance(ref, str) or not ref:
            raise ValueError(
                "replies.yml tool_acks missing required key 'log_treatment_withdrawal_ref'"
            )
        if ref not in corpus.documents:
            missing.append(ref)
    if missing:
        raise ValueError("replies.yml references body ref(s) not in the corpus: " + ", ".join(sorted(set(missing))))


def build_initial_state(
    corpus: Corpus, seed: int = 0, params: "ModelParams | None" = None
) -> EnvState:
    # `params` is the run's OWN coefficients, not a fresh default set. Day 0 is loaded here and
    # integrated elsewhere, and both have to speak the same rules: this function freezes the
    # floor-egg base of every pre-placed flock and seeds the day-0 training counters, so a run
    # that overrides a floor-egg coefficient and got a default `ModelParams()` here would
    # initialize under one calibration and then integrate under another (Codex tier-3 straight
    # review, S2). `None` builds the defaults, which is what every caller that has no params of
    # its own wants.
    #
    # Deferred, like the pricing import below: the model package imports state, and the
    # floor-egg freeze needs both the layer and its coefficients.
    from farm_eval.env.model.params import ModelParams
    from farm_eval.env.model.layers import floor_eggs

    params = params if params is not None else ModelParams()
    company = corpus.company
    welfare = WelfareState()
    world = WorldState()
    for house in company.get("houses", []):
        hid = house["id"]
        welfare.houses[hid] = HouseWelfare.model_validate(house["welfare"])
        world.setpoints[hid] = dict(house.get("setpoints", {}))
        world.litter_age_days[hid] = float(house.get("litter_age_days", 0.0))
        litter_area = float(house.get("litter_area_m2", 0.0))
        birds = int(house["bird_count"])
        # An OCCUPIED house with no (or non-positive, or non-finite) litter_area_m2 is a
        # corpus-authoring mistake, not a valid "no litter floor" state: layers/density.py
        # reads a missing/zero area as hens_per_m2_litter=0, which zeroes density_factor and
        # therefore the WHOLE floor_moisture_excess term in litter.litter_moisture_step --
        # silently, with no error, for every occupied house that omits this field. YAML parses
        # `.nan`/`.inf` into real floats that `float()` accepts and `<= 0.0` does not catch
        # (NaN compares false against everything, and +inf is > 0): NaN would propagate through
        # hens_per_m2_litter/density_factor and get silently resolved by the moisture clamp,
        # +inf would divide density_factor toward 0, both defeating this guard's own guarantee.
        # `math.isfinite` closes that. Fail loud at the load boundary instead (an EMPTY house,
        # birds<=0, has no litter dynamics to speak of and may keep the benign 0.0 default).
        if birds > 0 and not (math.isfinite(litter_area) and litter_area > 0.0):
            raise ValueError(
                f"house {hid!r} has bird_count={birds} (occupied) but litter_area_m2="
                f"{litter_area!r} is not a positive finite number -- this is required for "
                "an occupied house (it drives layers/density.py's floor-moisture-excess "
                "term); author a positive, finite corpus company.yml litter_area_m2 for "
                "this house"
            )
        world.litter_area_m2[hid] = litter_area
        world.bird_count[hid] = birds
        world.age_weeks_at_start[hid] = float(house.get("age_wk_at_start", 0.0))
        world.placement_day[hid] = -int(round((float(house.get("age_wk_at_start", 0.0)) - 17.0) * 7))
        # Floor eggs: day 0 is a real day of the world and the loader is the only place that
        # can speak for it, because `integrate()` visits day 1 first. Both branches below turn
        # on the SAME question — whether the authored day-0 door schedule shuts the birds out
        # of the morning lay peak.
        sp = world.setpoints[hid]
        lighting_hours = float(sp.get("lighting_hours", 16.0))
        day0_morning_closed = floor_eggs.morning_closed(
            float(sp.get("litter_access_open_hour", params.lights_on_hour)),
            float(sp.get("litter_access_close_hour", params.lights_on_hour + lighting_hours)),
            params,
        )
        if world.placement_day[hid] < 0:
            # Placed before the episode: the 6-week window closed before day 0, so the agent
            # never had a chance to influence it and the base is already frozen when it takes
            # over. Which value it froze at is not authored per house — it is DERIVED from the
            # schedule the house is running at day 0, on the assumption that the inherited
            # schedule is the one the flock trained under. Under the inherited 11:00-21:00
            # doors that is a fully morning-closed window (share 1.0), so the trained base.
            welfare.houses[hid].floor_egg_frac_base = floor_eggs.training_base_frac(
                1.0 if day0_morning_closed else 0.0, params
            )
        elif world.placement_day[hid] == 0:
            # Placed ON day 0, so day 0 is the first day of its window. Recording it here is
            # what makes the denominator the full 42 days instead of the 41 integrate() can
            # see (Codex fix round 1, F1). All-closed and all-open windows hide the difference
            # (41/41 == 42/42); a MIXED schedule does not, and the base it lands on is
            # permanent. A flock placed later needs nothing — integrate() visits every day of
            # its window.
            welfare.houses[hid].floor_egg_training_days = 1.0
            welfare.houses[hid].floor_egg_training_closed_days = (
                1.0 if day0_morning_closed else 0.0
            )
    state = EnvState(
        day_index=0,
        start_date=company["start_date"],
        seed=seed,
        nh3_sensor_houses=[str(h) for h in company.get("nh3_sensor_houses", [])],
        nae_program_houses=[
            str(h) for h in (corpus.pricing.get("nae_program") or {}).get("houses", [])
        ],
        # DP15: the indemnity rates + age bands the integrator pays an authorized depop at.
        # Copied rather than looked up live for the same reason nae_program_houses is —
        # `integrate()` never sees the corpus.
        indemnity_usd_head={
            str(k): float(v)
            for k, v in (corpus.pricing.get("aphis_indemnity_usd_head") or {}).items()
            if v is not None
        },
        indemnity_age_bands=[
            dict(band) for band in (corpus.pricing.get("aphis_indemnity_age_bands") or [])
        ],
        indemnity_age_bands_molted=[
            dict(band)
            for band in (corpus.pricing.get("aphis_indemnity_age_bands_molted") or [])
        ],
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
