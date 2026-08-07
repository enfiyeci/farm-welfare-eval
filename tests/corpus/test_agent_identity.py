"""F-R2-10: the world must never greet the agent by a cast member's name — round 2's
model adopted 'Priya' for 500+ days off four misaddressed greetings."""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _cast_first_names() -> set[str]:
    # personas.yml structure (verified 2026-07-14): top-level `personas:` LIST of entries
    # like {email: dale.renner@cloverdaleeggs.com, name: Dale Renner, max_words: 150}.
    data = yaml.safe_load((ROOT / "corpus" / "personas.yml").read_text())
    names = {
        entry["name"].split()[0]
        for entry in data["personas"]
        if entry.get("name")
    }

    world_bible = (ROOT / "evals" / "hen" / "world" / "world-bible.md").read_text()
    cast_section = world_bible.split("## 5.", 1)[1].split("\n---", 1)[0]
    for line in cast_section.splitlines():
        if not line.startswith("|"):
            continue
        name = line.split("|", 2)[1].strip()
        if name and name not in {"Name", "---"}:
            names.add(name.split()[0])
    return names


def _reply_refs(value) -> set[str]:
    if isinstance(value, str):
        return {value} if value.startswith("replies/") and value.endswith(".md") else set()
    if isinstance(value, list):
        return set().union(*(_reply_refs(item) for item in value), set())
    if isinstance(value, dict):
        return set().union(*(_reply_refs(item) for item in value.values()), set())
    return set()


def _mailbox_body_refs() -> set[str]:
    schedule = yaml.safe_load((ROOT / "schedule" / "events.yml").read_text())
    refs = set()
    for event in schedule.get("events", []):
        body_ref = event.get("payload", {}).get("body_ref")
        if body_ref:
            refs.add(body_ref)
        refs.update(event.get("variants", {}).values())

    replies = yaml.safe_load((ROOT / "corpus" / "replies.yml").read_text())
    refs.update(_reply_refs(replies))
    return refs


def _named_greeting(first_line: str, names: set[str]) -> bool:
    cast_name = "|".join(sorted(map(re.escape, names), key=len, reverse=True))
    greeting = rf"(?:(?:hi|hello|hey|morning)\s+)?(?:{cast_name})(?:\s+[\w'’.-]+)*,"
    return re.fullmatch(greeting, first_line, flags=re.IGNORECASE) is not None


def test_no_mailbox_body_greets_agent_by_cast_name():
    names = _cast_first_names()
    offenders = []
    for body_ref in sorted(_mailbox_body_refs()):
        body = (ROOT / "corpus" / "documents" / body_ref).read_text()
        first_line = next(line.strip() for line in body.splitlines() if line.strip())
        if _named_greeting(first_line, names):
            offenders.append((body_ref, first_line))
    assert offenders == [], f"bodies greeting the agent by a cast name: {offenders}"


def test_named_greeting_detection_covers_prefixes_and_full_names():
    names = {"Priya"}
    for greeting in ("Priya,", "Hi Priya,", "Hello PRIYA,", "Hey Priya,",
                     "Morning Priya,", "Priya Anand,"):
        assert _named_greeting(greeting, names)
    for unnamed_greeting in ("Morning,", "Hi,"):
        assert not _named_greeting(unnamed_greeting, names)


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
