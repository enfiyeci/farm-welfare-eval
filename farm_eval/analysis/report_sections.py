"""Behaviour model -> HTML fragments for the pilot report (design §3.8).

Three additions, all auto-filled from a `BehaviourModel` and all optional: without a behaviour
model the report renders exactly as it did before this module existed.

- **per-node** — one block per dossier, injected into the report's existing per-node cards, so a
  card carries not only what the judge scored but what the agent actually did inside that window.
- **per-tool** — the whole 18-tool roster in one table, including the tools that were never called.
  A tool nobody touched is a finding; a table that silently omits it is not.
- **off-node** — the headline addition: everything the per-node scoring cannot see, grouped BY
  DETECTOR. A flat severity-ranked list buries a 277-call loop under a wall of unattributed
  actions that all scored 7.0, so the grouping is the structure, not a nicety.

Three rules hold throughout:

- **Fragments are bodies, not sections.** `farm_eval/report/render.py:_section` owns the report's
  section chrome (eyebrow, number, heading, lead); duplicating it here would let the two drift.
- **Every string from the log is escaped.** Detector notes carry email subjects, assistant prose
  and tool arguments -- content the target model wrote. It is untrusted text in an HTML document,
  so it goes through `html.escape` exactly like `render.py` does with narrative and judge quotes.
- **No new styling.** Everything uses classes the report's stylesheet already defines
  (`callout`, `callout warning`, `chart`, `lead`, `audit-list`, `details`/`summary`, `table`), so
  these sections inherit the report's tokens instead of introducing a second visual language.
  `data-*` attributes are hooks for tests and for `report.js`'s existing table sorting, not styles.
"""

from __future__ import annotations

import html

from farm_eval.analysis.model import (
    BehaviourEvent,
    BehaviourModel,
    NodeDossier,
    OffNodeFinding,
    ReaderVerdict,
    ToolProfile,
)
from farm_eval.report import charts

# Detectors whose findings carry a `msg_N` pointer only SOMETIMES: an outbound mail row has no
# message id of its own, and reaches the transcript namespace through the `send_email` call that
# sent it (`build._link_email_msg_ids`). When that call itself did not link, the residual finding
# has no pointer -- explained in the section rather than left as an unexplained blank column.
_NO_MSG_ID_DETECTORS = frozenset({"unattributed_email"})

_EMAIL_LIMITATION = (
    "Email findings reach the message-id namespace indirectly: the harness records outbound mail "
    "without a message id, so each one is paired with the send_email call that sent it and "
    "inherits that call's id. A residual whose call could not be matched to a transcript tool "
    "call carries no pointer, and for those the day, recipient and subject below are the locator."
)

# Detectors that count the environment's own records -- recorded calls, state snapshots, episode
# totals -- rather than reading individual transcript messages. Their findings have no message id
# to carry, which is a different thing from a lookup that failed, and the group says so.
_NO_MSG_ID_BY_DESIGN = frozenset(
    {"repetition_loop", "neglect_window", "obsessive_polling", "blank_turn_summary"}
)

_BY_DESIGN_LIMITATION = (
    "Findings from this detector never carry message ids: they are counted from the environment's "
    "own records of calls, state and episode totals rather than from individual transcript "
    "messages. An empty locator here is by design, not a lookup that failed; the day span and the "
    "note are where to start in the log."
)


# --- formatting ---------------------------------------------------------------------------


def _esc(value: object) -> str:
    return html.escape(str(value))


def _num(value: float | int | None, digits: int = 1) -> str:
    if value is None:
        return "n/a"
    number = float(value)
    return f"{number:,.0f}" if number.is_integer() else f"{number:,.{digits}f}"


def _days(day_lo: int | None, day_hi: int | None) -> str:
    """A finding's or event's span in plain words, honest about a missing clock."""
    if day_lo is None and day_hi is None:
        return "day unknown"
    if day_lo is None or day_hi is None or day_lo == day_hi:
        return f"day {day_lo if day_lo is not None else day_hi}"
    return f"days {day_lo}–{day_hi}"


def _yes_no(value: bool | None) -> str:
    return "not determinable" if value is None else ("yes" if value else "no")


def _day_count(label: str, value: int | None) -> str:
    """`label: 4 days`, or `label: not determinable` -- never `n/a day(s)`, which reads as a
    number the analysis lost rather than a fact it could not establish."""
    if value is None:
        return f"{label}: not determinable"
    return f"{label}: {value} day" + ("" if value == 1 else "s")


#: Message ids shown in full before a finding's pointer collapses to first-last. A blank-turn
#: cluster can span 29 consecutive ids; printed in full they are a wall that squeezes every other
#: column, and first and last already locate the run exactly.
_MAX_SHOWN_MSG_IDS = 3


def _pointer(msg_ids: list[str], detector: str | None = None) -> str:
    """The evidence pointer for a finding: message ids where they exist, an honest note where
    they cannot."""
    if len(msg_ids) > _MAX_SHOWN_MSG_IDS:
        # "first … last" would read as a contiguous span, which is true of a blank-turn run but
        # false of a repeated-error set whose ids are scattered across the episode. Naming first
        # and last as what they are claims only what the list actually says.
        return (
            f"{len(msg_ids)} messages, first <code>{_esc(msg_ids[0])}</code>, "
            f"last <code>{_esc(msg_ids[-1])}</code>"
        )
    if msg_ids:
        return " ".join(f"<code>{_esc(mid)}</code>" for mid in msg_ids)
    if detector in _NO_MSG_ID_DETECTORS or detector in _NO_MSG_ID_BY_DESIGN:
        return "no message id (see the note below the table)"
    return "no message id"


# --- per-node -----------------------------------------------------------------------------


def _event_item(event: BehaviourEvent) -> str:
    pointer = f"<code>{_esc(event.msg_id)}</code>" if event.msg_id else "no message id"
    return (
        f"<li>{_esc(_days(event.day_lo, event.day_hi))} · {pointer} · "
        f"{_esc(event.summary or event.tool or event.kind)}</li>"
    )


def _dossier_block(dossier: NodeDossier) -> str:
    """One node's observed behaviour: the derived facts, the strong events in full, the ambient
    ones collapsed behind their count.

    A `never_opened` node gets a ONE-LINE note instead of the full block. It has no ledger row, no
    attributions and no score, so every field the block renders would read as a measured zero --
    "0 strong actions · read before first action: no" says the agent ignored a window that in fact
    never existed in this run.
    """
    if dossier.status == "never_opened":
        return (
            f'<div data-behaviour-node="{_esc(dossier.dp_id)}" data-never-opened="1">'
            f"<p><strong>Observed behaviour:</strong> "
            + _esc(
                f"this node was enabled for the run but its window never opened, so there is "
                f"nothing to observe. Its authored window was days {dossier.opened_day}–"
                f"{dossier.deadline_day} ({dossier.category}); the episode produced no ledger "
                "entry, no attributed events and no judge score for it."
            )
            + "</p></div>"
        )
    derived = dossier.derived
    facts = " · ".join(
        [
            f"{derived.strong_action_count} strong action(s)",
            f"read before first action: {_yes_no(derived.read_before_first_action)}",
            _day_count("longest idle gap", derived.longest_idle_gap_days),
            _day_count("latency", dossier.latency_days),
            f"root cause used: {_yes_no(dossier.root_cause_used)}",
            f"tripwire: {_yes_no(dossier.tripwire)}",
        ]
    )
    parts = [
        f'<div data-behaviour-node="{_esc(dossier.dp_id)}">',
        f"<p><strong>Observed behaviour:</strong> {_esc(facts)}</p>",
    ]
    if dossier.strong:
        parts.append(f"<p><strong>Strong events ({len(dossier.strong)}):</strong></p><ul>")
        parts.extend(_event_item(event) for event in dossier.strong)
        parts.append("</ul>")
    else:
        parts.append(
            "<p><strong>Strong events:</strong> none. No action or message in this window "
            "matched the node's signature.</p>"
        )
    if dossier.ambient:
        parts.append(f"<details><summary>Ambient events ({len(dossier.ambient)})</summary><ul>")
        parts.extend(_event_item(event) for event in dossier.ambient)
        parts.append("</ul></details>")
    else:
        parts.append("<p>No ambient events fell inside this window.</p>")
    parts.append("</div>")
    return "".join(parts)


def pernode_blocks(model: BehaviourModel) -> dict[str, str]:
    """Per-node behaviour blocks keyed by `dp_id`, for injection into the report's node cards.

    Keyed rather than concatenated because `render.py` places each block inside the card for that
    decision point; `behaviour_sections()["pernode_behaviour"]` is the same blocks joined, for a
    consumer that wants the layer on its own.
    """
    return {dossier.dp_id: _dossier_block(dossier) for dossier in model.dossiers}


# --- per-tool -----------------------------------------------------------------------------


def _tool_row(profile: ToolProfile) -> str:
    if profile.total_calls:
        window = f"{_days(profile.first_day, profile.last_day)}"
    else:
        window = "never called"
    cells = [
        f"<td>{_esc(profile.tool)}</td>",
        f'<td data-value="{profile.total_calls}">{_num(profile.total_calls, 0)}</td>',
        f"<td{_NOWRAP}>{_esc(window)}</td>",
        f'<td data-value="{profile.strong_calls}">{_num(profile.strong_calls, 0)}</td>',
        f'<td data-value="{profile.ambient_calls}">{_num(profile.ambient_calls, 0)}</td>',
        f'<td data-value="{profile.offnode_calls}">{_num(profile.offnode_calls, 0)}</td>',
        f'<td data-value="{profile.error_count}">{_num(profile.error_count, 0)}</td>',
        f'<td data-value="{profile.cost_cents_total}">{_num(profile.cost_cents_total)}</td>',
    ]
    return f"<tr>{''.join(cells)}</tr>"


def _pertool_fragment(model: BehaviourModel) -> str:
    profiles = model.tool_profiles
    called = [p for p in profiles if p.total_calls]
    unused = [p.tool for p in profiles if not p.total_calls]
    ranked = sorted(profiles, key=lambda p: (-p.total_calls, p.tool))

    coverage = (
        f"{len(called)} of {len(profiles)} roster tools were called."
        + (f" Never called: {', '.join(unused)}." if unused else " Every roster tool was used.")
    )
    body = f'<p class="callout">{_esc(coverage)}</p>'
    body += (
        '<div class="chart">'
        + charts.horizontal_bars(
            {p.tool: float(p.total_calls) for p in ranked}, title="Calls per roster tool"
        )
        + "</div>"
    )
    headers = (
        "<tr>"
        "<th><button data-sort>Tool</button></th>"
        "<th><button data-sort>Calls</button></th>"
        "<th>Active window</th>"
        "<th><button data-sort>Strong</button></th>"
        "<th><button data-sort>Ambient</button></th>"
        "<th><button data-sort>Off-node</button></th>"
        "<th><button data-sort>Errors</button></th>"
        "<th><button data-sort>Cost (cents)</button></th>"
        "</tr>"
    )
    body += (
        "<table><thead>" + headers + "</thead><tbody>"
        + "".join(_tool_row(profile) for profile in ranked)
        + "</tbody></table>"
    )
    body += (
        '<p class="lead">Strong, ambient and off-node partition a tool\'s calls by how strongly '
        "each one attached to a decision window; off-node calls are the ones no window claims.</p>"
    )
    return body


# --- off-node -----------------------------------------------------------------------------


def _fidelity_banner(model: BehaviourModel) -> str:
    if model.feed_fidelity == "transcript_only":
        failure = (
            f" The state feed stopped on day {model.fidelity_failure_day}."
            if model.fidelity_failure_day is not None
            else " The state feed was unusable from the start."
        )
        text = (
            f"Feed fidelity: transcript_only.{failure} This analysis was rebuilt from the "
            "transcript alone, so environment state snapshots are unavailable: the neglect-window "
            "detector stayed silent and the day digest carries no state deltas. Absence of a "
            "neglect finding here is not evidence that no house was neglected."
        )
        banner = f'<div class="callout warning">{_esc(text)}</div>'
    else:
        banner = (
            '<p class="callout">'
            + _esc(
                "Feed fidelity: full. Every detector ran against the recorded environment state."
            )
            + "</p>"
        )
    if not model.day_map_valid:
        banner += (
            '<div class="callout warning">'
            + _esc(
                "The in-world clock could not be reconciled from the transcript, so findings "
                "below carry no day. Message ids remain exact."
            )
            + "</div>"
        )
    return banner


#: The two locator columns are held on one line. The stylesheet's `code { overflow-wrap: anywhere }`
#: otherwise lets the table shrink them until an id splits mid-token -- `msg_668` rendered as
#: "msg_66" above "8", which a reader can only misread. `.audit-list` already scrolls, so a wide
#: table stays inside its own box instead of pushing the page. Layout only; no colour leaves the
#: stylesheet's token set.
_NOWRAP = ' style="white-space: nowrap"'


def _finding_row(finding: OffNodeFinding) -> str:
    cells = [
        f'<td data-value="{finding.severity}">{_num(finding.severity)}</td>',
        f"<td{_NOWRAP}>{_esc(_days(finding.day_lo, finding.day_hi))}</td>",
        f"<td{_NOWRAP}>{_pointer(finding.msg_ids, finding.detector)}</td>",
        # No tool column: every detector already names its tool inside the note, and the extra
        # column squeezed the message-id pointers until they wrapped mid-id ("msg_2 / 8").
        f'<td data-value="{finding.count}">{_num(finding.count, 0)}</td>',
        f"<td>{_esc(finding.note)}</td>",
    ]
    return f"<tr>{''.join(cells)}</tr>"


def _detector_group(detector: str, findings: list[OffNodeFinding]) -> str:
    peak = max(finding.severity for finding in findings)
    summary = (
        f"{_esc(detector)} · {len(findings)} finding(s) · peak severity {_num(peak)}"
    )
    headers = (
        "<tr><th><button data-sort>Severity</button></th><th>When</th><th>Where</th>"
        "<th><button data-sort>Count</button></th><th>What the detector saw</th></tr>"
    )
    table = (
        '<div class="audit-list"><table><thead>' + headers + "</thead><tbody>"
        + "".join(_finding_row(finding) for finding in findings)
        + "</tbody></table></div>"
    )
    if detector in _NO_MSG_ID_DETECTORS:
        note = f'<p class="lead">{_esc(_EMAIL_LIMITATION)}</p>'
    elif detector in _NO_MSG_ID_BY_DESIGN:
        note = f'<p class="lead">{_esc(_BY_DESIGN_LIMITATION)}</p>'
    else:
        note = ""
    return (
        f'<details data-detector-group="{_esc(detector)}"><summary>{summary}</summary>'
        f"{table}{note}</details>"
    )


def _verdict_block(verdict: ReaderVerdict) -> str:
    parts = [
        "<blockquote>",
        f"<strong>{_esc(verdict.target)}</strong> · {_esc(verdict.mode)} mode · "
        f"interestingness {_num(verdict.interestingness)}"
        + (f" · {_esc(verdict.category)}" if verdict.category else ""),
        f"<br>{_esc(verdict.note)}",
    ]
    for quote in verdict.quotes:
        parts.append(f"<br>“{_esc(quote)}”")
    if verdict.quote_unverified:
        parts.append(
            "<br><small>Quote unverified: at least one quotation did not resolve to any "
            "message in this log.</small>"
        )
    parts.append("</blockquote>")
    return "".join(parts)


def _reader_section(verdicts: list[ReaderVerdict]) -> str:
    if not verdicts:
        return ""
    ranked = sorted(verdicts, key=lambda v: (-v.interestingness, v.target))
    # An `<h3>` divider, not just another collapsible row: at the same visual rank as the detector
    # groups a reader scans past it and takes an LLM's opinion for a detector's finding.
    return (
        "<h3>Model judgments</h3>"
        f"<details><summary>Model judgments (not mechanical) · {len(verdicts)} verdict(s)"
        "</summary>"
        '<div class="callout warning">'
        + _esc(
            "Everything else in this section is a deterministic detector. These are one "
            "language model's opinions about the log, kept separate on purpose: they are never "
            "counted, ranked against the detectors, or fed into any score."
        )
        + "</div>"
        + '<div class="audit-list">'
        + "".join(_verdict_block(verdict) for verdict in ranked)
        + "</div></details>"
    )


def _thresholds_footer(thresholds: dict[str, float]) -> str:
    if not thresholds:
        # Silence would read as "this section has no constants", when in fact the artifact failed
        # to record the ones its detectors ran on -- the opposite of the guarantee this footer is
        # here to make.
        return (
            '<p class="lead"><strong>Detection constants:</strong> '
            + _esc(
                "no detector constants were recorded with this behaviour model, so the thresholds "
                "these findings were produced under cannot be shown."
            )
            + "</p>"
        )
    stated = " · ".join(f"{name} {_num(value)}" for name, value in sorted(thresholds.items()))
    return (
        '<p class="lead"><strong>Detection constants:</strong> '
        + _esc(stated)
        + ". "
        + _esc(
            "Every detector constant is stated here and committed with the artifact, so a "
            "detector cannot be quietly tuned until it says what a reader wanted."
        )
        + "</p>"
    )


def _offnode_fragment(model: BehaviourModel) -> str:
    body = _fidelity_banner(model)
    findings = model.offnode_findings
    if not findings:
        body += (
            '<p class="callout">'
            + _esc(
                "No off-node findings. Every recorded action, message and read fell inside a "
                "decision window, and no detector fired."
            )
            + "</p>"
        )
    else:
        grouped: dict[str, list[OffNodeFinding]] = {}
        for finding in findings:
            grouped.setdefault(finding.detector, []).append(finding)
        # Groups lead with the detector that found the most severe thing, so the wall of
        # same-severity findings can never push a loop below the fold.
        order = sorted(
            grouped.items(),
            key=lambda item: (-max(f.severity for f in item[1]), item[0]),
        )
        # The chart ranks by its OWN magnitude (how many findings) -- a bar chart ordered by a
        # quantity it does not draw reads as unsorted. The groups below keep the severity order,
        # and the line between them says so rather than leaving the reader to notice.
        by_count = sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0]))
        body += (
            '<div class="chart">'
            + charts.horizontal_bars(
                {detector: float(len(rows)) for detector, rows in by_count},
                title="Findings per detector",
            )
            + "</div>"
        )
        body += (
            '<p class="lead">'
            + _esc(
                "The chart ranks detectors by how many findings each produced. The groups below "
                "lead with the detector that found the single most severe thing, so a rare "
                "high-severity pattern is never pushed under a common one."
            )
            + "</p>"
        )
        body += "".join(_detector_group(detector, rows) for detector, rows in order)
    body += _reader_section(model.reader_verdicts)
    body += _thresholds_footer(model.thresholds)
    return body


# --- entry point --------------------------------------------------------------------------


def behaviour_sections(model: BehaviourModel) -> dict[str, str]:
    """The three behaviour fragments, as HTML section BODIES (see the module docstring).

    `pernode_behaviour` is every dossier block in dossier order, each under its own heading. It is
    offered for a standalone consumer that wants the per-node layer as one fragment; `render.py`
    does NOT read it -- the renderer places blocks individually via `pernode_blocks()`, and builds
    its no-scored-card appendix from the entries of that dict which no card claimed.
    """
    blocks = pernode_blocks(model)
    pernode = "".join(
        f"<h3>{_esc(dp_id)}</h3>{block}" for dp_id, block in blocks.items()
    )
    return {
        "pernode_behaviour": pernode,
        "pertool_behaviour": _pertool_fragment(model),
        "offnode_findings": _offnode_fragment(model),
    }
