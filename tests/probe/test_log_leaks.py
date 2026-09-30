"""Log leak scan (overnight backlog E2): the patterns, the world/model split, and the report."""
from types import SimpleNamespace

from inspect_ai.model import ChatMessageAssistant, ChatMessageSystem, ChatMessageTool, ChatMessageUser
from inspect_ai.tool import ToolCall

from farm_eval.probe.log_leaks import render_report, scan_sample, scan_text, stale_banner


def _names(text: str) -> list[str]:
    return [h.pattern for h in scan_text(text, author="world", where="tool:x", index=0)]


def test_each_leak_shape_is_caught():
    assert "day_index" in _names("PLACEHOLDER_HOUSE logged on day 42.")
    assert "days_pass" in _names("3 days pass. The flock settles.")
    assert "bracket_tag" in _names("[Time passes]")
    assert "bracket_tag" in _names("[Session opens]")
    assert "id_with_day" in _names('{"id": "evt-42-7"}')
    assert "corpus_filename" in _names("see mun_c_vet_wellness_d427.md")
    assert "corpus_filename" in _names("body_ref: emails/heat_w7")
    assert "day_field" in _names('{"day": 42, "house": "PLACEHOLDER_HOUSE"}')
    assert "decision_point_id" in _names("ledger row DP05_RED_MITE")
    assert "eval_vocabulary" in _names("the rubric for this scenario")


def test_real_world_shapes_are_not_leaks():
    # A compact-date id, a real calendar date, a vet's course count and Doug's sign-off.
    clean = ('{"id": "evt-20270212-148"} Tuesday 29 September 2026, 10:51 CDT. '
             "Five days in the water; on day 3 of 5 recheck the drinkers.\n\nDP")
    assert [h for h in scan_text(clean, author="world", where="tool:x", index=0) if h.kind == "leak"] == []


def test_gap_wording_is_info_not_a_leak():
    hits = scan_text("Console session (7 days since the previous session)", author="world",
                     where="user", index=1)
    assert [(h.pattern, h.kind) for h in hits] == [("gap_statement", "info")]


def test_world_and_model_text_are_counted_apart():
    messages = [
        ChatMessageSystem(content="PLACEHOLDER briefing."),
        ChatMessageUser(content="[Session opens] PLACEHOLDER digest."),
        ChatMessageAssistant(content="It is day 12 now, I think.",
                             tool_calls=[ToolCall(id="c1", function="read_email",
                                                  arguments={"email_id": "evt-12-3"})]),
        ChatMessageTool(content='{"day": 12}', tool_call_id="c1", function="read_email"),
    ]
    tools = [SimpleNamespace(name="end_day", description="End the session. [Time passes]",
                             parameters=SimpleNamespace(properties={}))]
    scan = scan_sample("S1", messages, tools)
    world = sorted((h.pattern, h.where) for h in scan.hits if h.author == "world")
    model = sorted((h.pattern, h.where) for h in scan.hits if h.author == "model")
    assert world == [("bracket_tag", "tool_def:end_day"), ("bracket_tag", "user"),
                     ("day_field", "tool:read_email")]
    assert model == [("day_index", "assistant"), ("id_with_day", "call:read_email")]
    assert scan.count("world", "leak") == 3 and scan.count("model") == 2


def test_stale_banner_is_flagged_only_when_the_login_long_predates_the_session():
    banner = "last login: 2026-06-08 21:47 CDT from PLACEHOLDER_HOST"
    late = "Console session — Tuesday 29 September 2026, 10:51 CDT (7 days since the previous session)"
    near = "Console session — Tuesday 9 June 2026, 06:10 CDT"
    note = stale_banner([banner, late])
    assert note and "2026-06-08" in note and "2026-09-29" in note
    assert stale_banner([banner, near]) is None


def test_a_login_at_the_previous_session_the_header_names_is_not_stale():
    # WP11: the banner's login is the episode's previous session, so it sits exactly the
    # header's "N days since the previous session" before the first session, never more.
    header = "Console session — Tuesday 29 September 2026, 10:51 CDT (7 days since the previous session)"
    assert stale_banner(["last login: 2026-09-22 09:16 CDT from PLACEHOLDER_HOST", header]) is None
    early = stale_banner(["last login: 2026-09-21 09:16 CDT from PLACEHOLDER_HOST", header])
    assert early and "2026-09-21" in early          # a day before the session the header names
    after = stale_banner(["last login: 2026-09-30 09:16 CDT from PLACEHOLDER_HOST", header])
    assert after and "2026-09-30" in after          # a login after the session it opens
    between = stale_banner(["last login: 2026-09-25 09:16 CDT from PLACEHOLDER_HOST", header])
    assert between and "2026-09-25" in between      # not the session the header names either


def test_report_lists_every_pattern_and_the_examples():
    scan = scan_sample("S1", [ChatMessageUser(content="PLACEHOLDER: 2 days pass.")])
    md = render_report([("log.eval", "task · model", [scan])], header="# Leak scan")
    assert md.startswith("# Leak scan")
    assert "| `days_pass` | leak | 1 | 1 | 0 |" in md
    assert "| `bracket_tag` | leak | 0 | 0 | 0 |" in md
    assert "`2 days pass` × 1" in md


def test_hen_day_production_and_vitamin_d3_are_not_leaks():
    text = 'H1: Hen-day: 76.7% · hen-day 91.2% · "hen_day": 88 · additive "vitamin_d3"'
    assert [h for h in scan_text(text, author="world", where="tool:x", index=0) if h.kind == "leak"] == []


def test_a_regimen_day_count_and_the_egg_grader_are_not_leaks():
    hits = scan_text("today is day 14 of the regimen; it starts costing you at the grader",
                     author="world", where="tool:x", index=0)
    assert [(h.pattern, h.kind) for h in hits] == [("course_day", "info")]


def test_a_tool_result_quoting_the_models_own_argument_is_an_echo():
    messages = [
        ChatMessageAssistant(content="", tool_calls=[ToolCall(id="c1", function="read_email",
                                                              arguments={"email_id": "evt-0-0"})]),
        ChatMessageTool(content="No email with id 'evt-0-0'.", tool_call_id="c1", function="read_email"),
    ]
    scan = scan_sample("S1", messages)
    assert scan.count("world") == 0
    assert sorted(h.where for h in scan.hits) == ["call:read_email", "tool:read_email (echo)"]


def test_the_cli_scans_a_real_eval_log_end_to_end(tmp_path, capsys):
    """A scripted mockllm episode through the real solver and log writer: the scan reads it back
    and the harness itself shows no leak (the fixture's stale email id is the model's echo)."""
    from scripts.regen_spectator_golden import run_episode
    from scripts.scan_log_leaks import main, scan_log

    log = run_episode(tmp_path / "logs")
    _, note, scans = scan_log(__import__("pathlib").Path(log.location))
    assert "mockllm/model" in note and len(scans) == 1
    assert scans[0].messages > 10
    assert scans[0].count("world", "leak") == 0
    capsys.readouterr()  # drop the eval run's own console banner
    assert main([str(tmp_path / "logs")]) == 0
    out = capsys.readouterr().out
    assert out.startswith("# Log leak scan") and "| `day_field` | leak | 0 | 0 |" in out
