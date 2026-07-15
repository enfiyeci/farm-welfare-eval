"""F-R2-10: the world must never greet the agent by a cast member's name — round 2's
model adopted 'Priya' for 500+ days off four misaddressed greetings."""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _first_names() -> set[str]:
    # personas.yml structure (verified 2026-07-14): top-level `personas:` LIST of entries
    # like {email: dale.renner@cloverdaleeggs.com, name: Dale Renner, max_words: 150}.
    data = yaml.safe_load((ROOT / "corpus" / "personas.yml").read_text())
    names = set()
    for entry in data["personas"]:
        name = entry.get("name") or ""
        if name:
            names.add(name.split()[0])
    return names


def test_no_inbound_body_greets_agent_by_cast_first_name():
    sched = yaml.safe_load((ROOT / "schedule" / "events.yml").read_text())
    company = yaml.safe_load((ROOT / "corpus" / "company.yml").read_text())
    agent = company["agent_email"]
    names = _first_names()
    offenders = []
    for ev in sched.get("events", []):
        payload = ev.get("payload", {})
        if payload.get("to", agent) != agent or not payload.get("body_ref"):
            continue
        body = (ROOT / "corpus" / "documents" / payload["body_ref"]).read_text()
        first_line = body.strip().splitlines()[0].strip()
        m = re.fullmatch(r"([A-Z][a-z]+),", first_line)
        if m and m.group(1) in names:
            offenders.append((payload["body_ref"], first_line))
    assert offenders == [], f"bodies greeting the agent by a cast name: {offenders}"


def test_placement_d0_is_addressed_to_the_agent():
    sched = yaml.safe_load((ROOT / "schedule" / "events.yml").read_text())
    company = yaml.safe_load((ROOT / "corpus" / "company.yml").read_text())
    ev = next(e for e in sched["events"]
              if e.get("payload", {}).get("body_ref") == "emails/placement_d0.md")
    assert ev["payload"]["to"] == company["agent_email"]


def test_briefing_states_the_ops_identity():
    briefing = (ROOT / "prompts" / "operator_briefing.md").read_text()
    assert "Complex 2 Ops (FMS)" in briefing
    for corner in (ROOT / "prompts" / "baselines").glob("*.md"):
        assert "Complex 2 Ops (FMS)" in corner.read_text(), f"{corner.name} not regenerated"
