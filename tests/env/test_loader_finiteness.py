"""Corpus and schedule YAML must reject non-finite floats at load time.

Wave-2 Codex straight review, demonstrated by execution: the EnvState construction guard
does not cover external numbers that enter AFTER construction — `build_initial_state` calls
`refresh_market` (corpus pricing -> state.market) post-construction, and `end_day` fires
schedule event payloads (pricing_shift, state_seed, sensor_anomaly) into a staged
`model_copy(deep=True)`, which never revalidates. A `.nan` authored in pricing.yml therefore
reached `state.market.egg_price_usd_doz` silently.

The fix is at the SOURCE: everything those paths ingest comes out of `load_corpus` /
`load_schedule`, both of which return pydantic models the shared walker can sweep once, at
load — zero per-day cost, and the error names the authored key while the author is looking
at the file. Same posture as `_validate_audit_thresholds`, loader.py's existing fail-at-load
precedent. (`apply_overrides` needs no guard: it replaces document TEXT only.)
"""
import shutil

import pytest
import yaml

from farm_eval.env.loader import load_corpus, load_schedule

FIXTURE_CORPUS = "tests/fixtures/corpus"
FIXTURE_SCHEDULE = "tests/fixtures/schedule"


def _corpus_dir(tmp_path, mutate_file: str, mutate):
    base = tmp_path / "corpus"
    shutil.copytree(FIXTURE_CORPUS, base)
    target = base / mutate_file
    data = yaml.safe_load(target.read_text(encoding="utf-8")) or {}
    mutate(data)
    target.write_text(yaml.safe_dump(data), encoding="utf-8")
    return base


def test_load_corpus_rejects_nan_in_pricing(tmp_path):
    # The exact reviewer PoC: a NaN monthly wholesale price previously flowed through
    # refresh_market into state.market unvalidated.
    base = _corpus_dir(
        tmp_path, "pricing.yml",
        lambda d: d.setdefault("egg_wholesale_usd_doz", {}).__setitem__("2025-06", float("nan")),
    )
    with pytest.raises(ValueError) as exc:
        load_corpus(base)
    assert "pricing" in str(exc.value) and "egg_wholesale_usd_doz" in str(exc.value)


def test_load_corpus_rejects_inf_in_company(tmp_path):
    # company.yml numbers reach more than ModelParams (indemnity tables, house geometry);
    # the load-time sweep covers ALL of them, not just the three params_for keys.
    base = _corpus_dir(
        tmp_path, "company.yml",
        lambda d: d["houses"][0].__setitem__("litter_age_days", float("inf")),
    )
    with pytest.raises(ValueError) as exc:
        load_corpus(base)
    assert "litter_age_days" in str(exc.value)


def test_load_corpus_accepts_the_fixture_corpus():
    load_corpus(FIXTURE_CORPUS)  # positive control: must not raise


def test_load_schedule_rejects_non_finite_event_payload(tmp_path):
    # Event payloads are free-form dict[str, Any] straight from YAML (pricing_shift,
    # state_seed, sensor_anomaly values), and end_day writes them into the staged state.
    base = tmp_path / "schedule"
    base.mkdir()
    with open(f"{FIXTURE_SCHEDULE}/events.yml", encoding="utf-8") as fh:
        src = yaml.safe_load(fh)
    anomaly = next(ev for ev in src["events"] if ev["type"] == "sensor_anomaly")
    anomaly["payload"]["set_value"] = float("inf")
    (base / "events.yml").write_text(yaml.safe_dump(src), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_schedule(base)
    assert "set_value" in str(exc.value)


def test_load_schedule_accepts_the_fixture_schedule():
    load_schedule(FIXTURE_SCHEDULE)  # positive control: must not raise
