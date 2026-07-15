from __future__ import annotations

import html
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from string import Template

from farm_eval.report import charts


_TEMPLATE_DIR = Path(__file__).with_name("templates")
_NARRATIVE_HEADINGS = {
    "executive_summary",
    "behavioral_portrait",
    "odd_behaviors",
    "node_verdicts",
    "dispositions",
    "cross_run",
}


def parse_narrative(markdown: str | None) -> dict[str, str]:
    if not markdown:
        return {}
    matches = list(re.finditer(r"(?m)^##[ \t]+([a-z][a-z0-9_]*)[ \t]*$", markdown))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1)
        if name not in _NARRATIVE_HEADINGS:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[name] = markdown[match.end() : end].strip()
    return sections


def _narrative_html(value: str | None) -> str:
    if not value:
        return '<div class="placeholder">✍️ write me</div>'
    escaped = html.escape(value)
    blocks = []
    for block in re.split(r"\n\s*\n", escaped):
        lines = block.splitlines()
        if lines and all(line.lstrip().startswith(("- ", "* ")) for line in lines):
            items = "".join(f"<li>{line.lstrip()[2:]}</li>" for line in lines)
            blocks.append(f"<ul>{items}</ul>")
        elif lines and all(re.match(r"^\d+\.\s", line.lstrip()) for line in lines):
            items = "".join(f"<li>{re.sub(r'^\d+\.\s*', '', line.lstrip())}</li>" for line in lines)
            blocks.append(f"<ol>{items}</ol>")
        else:
            blocks.append(f"<p>{'<br>'.join(lines)}</p>")
    return "".join(blocks)


def _fmt(value: object, digits: int = 2) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float)):
        return f"{value:,.{digits}f}" if isinstance(value, float) else f"{value:,}"
    return str(value)


def _metric(label: str, value: object, note: str = "") -> str:
    return f'<div class="metric"><span>{html.escape(label)}</span><strong>{html.escape(_fmt(value))}</strong><small>{html.escape(note)}</small></div>'


def _chart(svg: str) -> str:
    return f'<div class="chart">{svg}</div>'


def _section(section_id: str, number: int, title: str, lead: str, body: str) -> str:
    return (
        f'<section id="{section_id}"><p class="eyebrow">Section {number}</p><h2>{html.escape(title)}</h2>'
        f'<p class="lead">{html.escape(lead)}</p>{body}</section>'
    )


def _executive(model: dict, analysis: dict, narrative: dict[str, str]) -> str:
    scores = model.get("scores", {})
    nodes = model.get("judge", {}).get("node_scores", {})
    top = sorted(nodes.items(), key=lambda item: item[1])[:3]
    comparisons = analysis.get("comparisons", [])
    deltas = "".join(
        f'<span class="chip">vs {html.escape(str(row.get("prior_label", row.get("prior_sha256", "prior")))[0:24])}: '
        f'{_fmt(row.get("headline_delta"))}</span>' for row in comparisons
    ) or '<span class="chip">Single-run report</span>'
    tripwires = scores.get("tripwires_observed", 0)
    verdict = "No tripwire gate fired." if not tripwires else f"{_fmt(tripwires, 0)} tripwire gate(s) fired."
    body = (
        '<div class="metric-grid">'
        + _metric("Welfare headline", scores.get("welfare_headline"), "0–10, node mean")
        + _metric("Layer-1 state", scores.get("welfare_state"), "0–1 endpoint score")
        + _metric("Tripwires", tripwires, "lower is better")
        + _metric("Frame-slip addresses", analysis.get("out_of_world_address_count"), "strict session-handoff count")
        + "</div>"
        + f'<p class="callout">{html.escape(verdict)}</p><p>{deltas}</p>'
        + ("<h3>Top three score findings</h3><ol>" + "".join(f"<li>{html.escape(node)} — {_fmt(score)}</li>" for node, score in top) + "</ol>" if top else "")
        + '<h3>Human conclusion</h3>' + _narrative_html(narrative.get("executive_summary"))
    )
    return _section(
        "executive-verdict", 1, "Executive verdict",
        "The headline summarizes welfare decision quality; Layer-1 and tripwires provide independent checks on the run.", body,
    )


def _glossary() -> str:
    terms = [
        ("Welfare headline", "The mean of enabled per-decision node scores on a 0–10 scale."),
        ("Node", "One authored welfare decision opportunity, usually identified by a DP code."),
        ("Tripwire", "A severe behavior that gates the headline when observed."),
        ("Layer-1", "The deterministic endpoint welfare-state score, separate from judged decision quality."),
        ("Eval-awareness", "A validity diagnostic for test suspicion or frame slips; it is not part of the welfare headline."),
        ("Mechanical ledger", "Harness-side action matching. A lapsed row can still receive judged credit for valid communication."),
    ]
    body = '<div class="callout">Read the headline first, then use node cards and the audit appendix to test whether the summary is trustworthy.</div>'
    body += "<details><summary>Glossary</summary><dl>" + "".join(f"<dt><strong>{term}</strong></dt><dd>{definition}</dd>" for term, definition in terms) + "</dl></details>"
    return _section("how-to-read", 2, "How to read this report", "The page moves from a plain-language result to team detail and then audit evidence.", body)


def _cross_run(analysis: dict, narrative: dict[str, str]) -> str:
    comparisons = analysis.get("comparisons", [])
    if not comparisons:
        body = '<p class="callout">No prior logs were supplied. Add <code>--vs prior.eval</code> to populate paired deltas.</p>'
    else:
        blocks = []
        for row in comparisons:
            label = str(row.get("prior_label", row.get("prior_sha256", "prior run")))
            blocks.append(f"<h3>Cross-run delta · compared with {html.escape(label)}</h3>")
            blocks.append(_chart(charts.delta_bars(row.get("node_deltas", {}), title=f"Node score deltas vs {label}")))
            dimension_rows = "".join(
                f'<tr><td>{html.escape(name)}</td><td data-value="{value}">{value:+.2f}</td></tr>'
                for name, value in sorted(row.get("dimension_deltas", {}).items())
            )
            blocks.append('<table><thead><tr><th><button data-sort>Dimension</button></th><th><button data-sort>Delta</button></th></tr></thead><tbody>' + dimension_rows + "</tbody></table>")
        body = "".join(blocks)
        body += '<h3>Why these values moved · paired evidence</h3>' + _narrative_html(narrative.get("cross_run"))
    return _section("cross-run", 3, "Cross-run comparison", "Positive deltas mean this run scored higher than the named prior run; they do not prove that the harness caused the change.", body)


def _behavioral(narrative: dict[str, str]) -> str:
    return _section("behavioral-portrait", 4, "Behavioral portrait", "This human-written layer explains the operator's identity, arc, tone, beliefs, and timeline with receipts.", _narrative_html(narrative.get("behavioral_portrait")))


def _oddities(narrative: dict[str, str]) -> str:
    return _section("odd-behaviors", 5, "Odd-behavior spotlights", "Anomalies belong here even when they do not affect the welfare headline.", _narrative_html(narrative.get("odd_behaviors")))


def _tool_analytics(model: dict, analysis: dict) -> str:
    usage = analysis.get("tool_usage", {})
    combined = {**usage.get("reads_by_type", {}), **usage.get("actions_by_type", {})}
    grouped: dict[str, Mapping[str, float]] = {"this run": combined}
    for index, row in enumerate(analysis.get("comparisons", []), start=1):
        prior_usage = row.get("prior_tool_usage", {})
        prior_combined = {**prior_usage.get("reads_by_type", {}), **prior_usage.get("actions_by_type", {})}
        if prior_combined:
            grouped[f"prior {index}"] = prior_combined
    bucket_points = [{"day": row.get("day", 0), "value": row.get("total", 0)} for row in usage.get("calls_by_bucket", [])]
    read_points = [{"day": row.get("day", 0), "value": row.get("reads", 0)} for row in analysis.get("engagement", {}).get("reads_by_bucket", [])]
    day_index = model.get("run", {}).get("day_index", 0)
    body = '<div class="two-col">'
    body += _chart(charts.grouped_horizontal_bars(grouped, title="Tool calls by type and run"))
    body += _chart(charts.line_chart({"all calls": bucket_points}, title="Tool calls over in-world time"))
    body += "</div>"
    body += _chart(charts.line_chart({"reads": read_points}, title="Engagement: reads over time", marker_day=day_index / 2 if day_index else None))
    body += f'<p class="callout">Strict out-of-world session-handoff addresses: <strong>{_fmt(analysis.get("out_of_world_address_count"), 0)}</strong>.</p>'
    return _section("tool-analytics", 6, "Tool usage and engagement analytics", "These charts show what the operator did and whether its attention persisted through the episode.", body)


def _welfare(model: dict, analysis: dict) -> str:
    harm = model.get("environment", {}).get("welfare_endpoint_harm", {})
    channel_scores = model.get("judge", {}).get("welfare_state_channels", {})
    normalized_harm = {
        channel: max(0.0, min(1.0, 1.0 - float(goodness)))
        for channel, goodness in channel_scores.items()
        if isinstance(goodness, (int, float))
    }
    series = analysis.get("observed_welfare_series", {})
    body = '<div class="callout warning"><strong>Layer-1 constraint:</strong> harm accumulators are final snapshots, not daily values. The comparable bars below are endpoint harm burdens (1 minus each scorer-normalized channel goodness); raw accumulators retain different units and are listed separately.</div>'
    body += _chart(charts.horizontal_bars(normalized_harm, title="Normalized endpoint harm burden by channel", scale_max=1.0))
    raw_rows = "".join(f"<tr><td>{html.escape(channel)}</td><td>{_fmt(value, 3)}</td></tr>" for channel, value in harm.items())
    body += f'<details><summary>Raw final harm accumulators</summary><table><thead><tr><th>Channel</th><th>Final accumulator (native unit)</th></tr></thead><tbody>{raw_rows}</tbody></table></details>'
    preferred = [key for key in ("ammonia_ppm", "birds_alive", "footpad_affected_pct", "panting_fraction", "red_mite_signs") if series.get(key)]
    if preferred:
        body += "<h3>Approximate observations from tool results</h3>"
        body += '<p class="lead">Each point is a value the model actually saw in a flock-report or sensor result. Lines connect sparse observations only.</p>'
        for metric in preferred:
            by_house: dict[str, list[dict]] = {}
            for point in series[metric]:
                by_house.setdefault(str(point.get("house_id", "unknown")), []).append({"day": point.get("day", 0), "value": point.get("value", 0)})
            body += _chart(charts.line_chart(by_house, title=f"Observed {metric.replace('_', ' ')}"))
    else:
        body += '<p class="callout">No flock-report or sensor result samples were available for the approximate observed series.</p>'
    return _section("welfare-state", 7, "Welfare state (Layer-1)", "Endpoint harm channels show accumulated outcomes; sparse observation charts show only what the operator read during the run.", body)


def _node_verdicts(value: str | None) -> dict[str, str]:
    verdicts: dict[str, str] = {}
    if not value:
        return verdicts
    for line in value.splitlines():
        match = re.match(r"\s*[-*]?\s*([A-Z][A-Z0-9_]+)\s*:\s*(.+)", line)
        if match:
            verdicts[match.group(1)] = match.group(2).strip()
    return verdicts


def _nodes(model: dict, narrative: dict[str, str]) -> str:
    judge = model.get("judge", {})
    scores = judge.get("node_scores", {})
    variance = judge.get("node_variance", {})
    ledger = {row.get("dp_id"): row for row in model.get("environment", {}).get("ledger", [])}
    recognition = judge.get("recognition", {})
    node_evidence = judge.get("node_evidence", {})
    verdicts = _node_verdicts(narrative.get("node_verdicts"))
    cards = []
    for node, score in scores.items():
        row = ledger.get(node, {})
        category, status = row.get("category", "unavailable"), row.get("status", "unavailable")
        cue = recognition.get(node, {}).get("inspected")
        variance_text = variance.get(node)
        criterion_rows = []
        for item in node_evidence.get(node, []):
            rubric = html.escape(str(item.get("rubric", ""))) or "Rubric unavailable"
            sample_rows = []
            for sample in item.get("samples", []):
                accepted = bool(sample.get("accepted"))
                label = "accepted" if accepted else "discarded"
                quote = html.escape(str(sample.get("quote", ""))) or "No quote"
                reason = f'<br><small>{html.escape(str(sample.get("discard_reason", "")))}</small>' if not accepted else ""
                sample_rows.append(
                    f'<blockquote><strong>Sample {int(sample.get("sample_index", 0)) + 1} · {label} · raw {_fmt(sample.get("score"))}</strong><br>'
                    f'{quote}<br><small>{html.escape(str(sample.get("message_id", "")))}</small>{reason}</blockquote>'
                )
            criterion_rows.append(
                f'<details><summary>{html.escape(str(item.get("criterion", "criterion")))} · validated median {_fmt(item.get("score"))}</summary>'
                f'<p><strong>Criterion reference rubric:</strong> {rubric}</p>'
                f'{"".join(sample_rows)}</details>'
            )
        detail = [
            f"<p><strong>Mechanical status:</strong> {html.escape(str(status))}; <strong>category:</strong> {html.escape(str(category))}; <strong>cue inspected:</strong> {_fmt(cue)}.</p>",
            f'<p><strong>Mechanical evidence:</strong> {html.escape(json.dumps(row.get("agent_action"), ensure_ascii=False, sort_keys=True)) if row.get("agent_action") else "No matched tool action; judged communication may still support credit."}</p>',
            '<div><strong>Judged evidence and criterion rationale:</strong>' + ("".join(criterion_rows) if criterion_rows else '<p>Not serialized for this node; consult the authored decision register and source log.</p>') + '</div>',
            f'<p><strong>Model-vs-harness verdict:</strong> {html.escape(node)}: {html.escape(verdicts.get(node, "✍️ write me"))}</p>',
        ]
        if variance_text:
            detail.append(f"<p><strong>Judge range:</strong> {_fmt(variance_text.get('min'))}–{_fmt(variance_text.get('max'))}</p>")
        search = html.escape(f"{node} {category} {status} {verdicts.get(node, '')}".lower(), quote=True)
        cards.append(f'<details data-node-card data-search="{search}"><summary>{html.escape(node)} · {_fmt(score)} · {html.escape(str(status))}</summary>{"".join(detail)}</details>')
    body = _chart(charts.node_score_strip(scores, variance=variance, title="Scores across enabled decision nodes"))
    if not variance:
        body += '<p class="lead">The log contains aggregate node scores but no per-node judge samples, so the strip shows points without variance whiskers.</p>'
    body += '<div class="node-tools"><label>Filter nodes <input data-node-filter type="search" placeholder="DP, category, verdict"></label><button data-expand="all">Expand all</button><button data-expand="none">Collapse all</button></div>'
    body += "".join(cards) if cards else '<p class="callout">No node scores were serialized.</p>'
    if not narrative.get("node_verdicts"):
        body += '<div class="placeholder">✍️ write me — add <code>## node_verdicts</code> with <code>DP_ID: verdict</code> lines.</div>'
    return _section("per-node", 8, "Per-node cards", "Each card pairs the judged score with the mechanical ledger; disagreement between them can be legitimate and should be reviewed.", body)


def _judge_qa(model: dict) -> str:
    judge = model.get("judge", {})
    scores = model.get("scores", {})
    nodes = judge.get("node_scores", {})
    computed = sum(nodes.values()) / len(nodes) if nodes else None
    headline = scores.get("welfare_headline")
    math_ok = computed is not None and headline is not None and abs(computed - headline) < 1e-9
    discarded = judge.get("discarded_evidence", {})
    dimension_notes = judge.get("dimension_notes", [])
    criterion_notes = judge.get("criterion_notes", [])
    body = '<div class="metric-grid">'
    body += _metric("Headline math", "passes" if math_ok else "check", "equal node mean")
    body += _metric("Dimension discards", discarded.get("dimension_samples", len(dimension_notes)), "quote validation")
    body += _metric("Criterion discards", discarded.get("criteria", len(criterion_notes)), "node evidence")
    body += _metric("Forced advances", model.get("run", {}).get("forced_advances"), "solver backstop") + "</div>"
    sample_rows = []
    samples = judge.get("dimension_samples", [])
    dimension_ids = sorted({key for sample in samples for key in sample if sample.get(key) is not None})
    for dimension in dimension_ids:
        values = [float(sample[dimension]["score"]) for sample in samples if sample.get(dimension) is not None]
        if values:
            sample_rows.append(
                f"<tr><td>{html.escape(dimension)}</td><td>{len(values)}</td><td>{min(values):.2f}</td>"
                f"<td>{max(values):.2f}</td><td>{(max(values) - min(values)):.2f}</td></tr>"
            )
    body += '<details><summary>Judge sample variance</summary>'
    body += ('<table><thead><tr><th>Dimension</th><th>Surviving n</th><th>Min</th><th>Max</th><th>Range</th></tr></thead><tbody>' + "".join(sample_rows) + "</tbody></table>") if sample_rows else "<p>No dimension-sample variance was serialized.</p>"
    body += "</details>"
    notes = dimension_notes + criterion_notes
    body += '<details><summary>Discarded evidence audit</summary><div class="audit-list">'
    body += "".join(f'<blockquote><strong>{html.escape(str(note.get("dimension", note.get("dp_id", "evidence"))))}</strong>: {html.escape(str(note.get("reason", "")))}</blockquote>' for note in notes) or "<p>No discarded-evidence notes.</p>"
    body += "</div></details>"
    body += '<p class="callout warning">Trust call: quote discards reduce the evidence base. Validity-gate dimensions should be interpreted alongside their surviving sample count, not as standalone facts.</p>'
    return _section("judge-qa", 9, "Measurement integrity and judge QA", "This section checks the headline arithmetic and exposes evidence the quote validator rejected.", body)


def _history(history: Sequence[dict]) -> str:
    if not history:
        body = '<p class="callout">No history rows are available. Unless <code>--no-history-write</code> is used, generation records this run by log hash.</p>'
    else:
        headline = [{"day": index + 1, "value": row.get("headline", 0)} for index, row in enumerate(history)]
        series: dict[str, list[dict]] = {"headline": headline}
        dimension_names = [
            "welfare_decision_quality", "root_cause_reasoning", "proactive_monitoring",
            "epistemic_calibration", "eval_awareness",
        ]
        for name in dimension_names:
            series[name] = [
                {"day": index + 1, "value": row["dimensions"][name]}
                for index, row in enumerate(history) if name in row.get("dimensions", {})
            ]
        body = _chart(charts.line_chart(
            series, title="All pilot rounds: headline and key dimensions",
            x_key="day", y_key="value", break_gaps=True,
        ))
        rows = "".join(f'<tr><td>{index + 1}</td><td>{html.escape(str(row.get("date", "")))}</td><td>{html.escape(str(row.get("model", "")))}</td><td data-value="{row.get("headline", 0)}">{_fmt(row.get("headline"))}</td><td>{_fmt(row.get("tripwires"), 0)}</td></tr>' for index, row in enumerate(history))
        body += '<table><thead><tr><th>Round</th><th>Date</th><th>Model</th><th><button data-sort>Headline</button></th><th>Tripwires</th></tr></thead><tbody>' + rows + "</tbody></table>"
    return _section("all-rounds-trend", 10, "All-rounds trend", "The history file is keyed by log hash, so regenerating a run updates its row instead of duplicating it.", body)


def _dispositions(narrative: dict[str, str]) -> str:
    return _section("dispositions", 11, "Disposition table", "Human owners record which findings to fix, accept, monitor, or validate in a later study.", _narrative_html(narrative.get("dispositions")))


def _repro(model: dict) -> str:
    source, run = model.get("source", {}), model.get("run", {})
    fields = [
        ("Log path", source.get("path")), ("Log SHA-256", source.get("sha256")), ("Status", source.get("status")),
        ("Target", run.get("target_model")), ("Grader", run.get("grader_model")), ("Branch", run.get("branch")),
        ("Commit", run.get("commit")), ("Dirty", run.get("dirty")), ("Started", run.get("started_at")),
        ("Completed", run.get("completed_at")), ("Runtime seconds", run.get("runtime_seconds")),
        ("Episode day", run.get("day_index")), ("Enabled nodes", ", ".join(run.get("node_set", []))),
    ]
    rows = "".join(f"<tr><th>{html.escape(label)}</th><td><code>{html.escape(_fmt(value))}</code></td></tr>" for label, value in fields)
    usage = html.escape(json.dumps(run.get("usage", {}), ensure_ascii=False, sort_keys=True))
    config = html.escape(json.dumps({
        "task_args": run.get("task_args", {}), "scorers": run.get("scorers", []),
        "eval_config": run.get("eval_config", {}),
    }, ensure_ascii=False, sort_keys=True))
    highlights = model.get("judge", {}).get("highlights", [])
    quotes = "".join(f'<blockquote id="quote-{index}"><strong>{html.escape(str(item.get("dimension", "")))}</strong> [{html.escape(str(item.get("message_id", "")))}]<br>{html.escape(str(item.get("quote", "")))}</blockquote>' for index, item in enumerate(highlights))
    body = f'<table><tbody>{rows}</tbody></table><details><summary>Token and cost metadata</summary><code>{usage}</code></details>'
    body += f'<details><summary>Evaluation configuration</summary><code>{config}</code></details>'
    body += f'<details><summary>Curated quote appendix</summary>{quotes or "<p>No highlights serialized.</p>"}</details>'
    return _section("reproducibility", 12, "Reproducibility and appendices", "These fields identify the exact run and preserve the judge's curated evidence locators.", body)


def render(
    report_model: dict,
    analysis: dict,
    *,
    narrative: str | None = None,
    history: Sequence[dict] | None = None,
) -> str:
    narrative_sections = parse_narrative(narrative)
    section_html = "".join(
        [
            _executive(report_model, analysis, narrative_sections), _glossary(), _cross_run(analysis, narrative_sections),
            _behavioral(narrative_sections), _oddities(narrative_sections), _tool_analytics(report_model, analysis),
            _welfare(report_model, analysis), _nodes(report_model, narrative_sections), _judge_qa(report_model),
            _history(list(history or [])), _dispositions(narrative_sections), _repro(report_model),
        ]
    )
    nav_items = [
        ("executive-verdict", "Verdict"), ("cross-run", "Comparison"), ("tool-analytics", "Engagement"),
        ("welfare-state", "Layer-1"), ("per-node", "Nodes"), ("judge-qa", "Judge QA"),
        ("all-rounds-trend", "Trend"), ("reproducibility", "Audit"),
    ]
    navigation = "".join(f'<a href="#{anchor}">{label}</a>' for anchor, label in nav_items)
    run = report_model.get("run", {})
    source = report_model.get("source", {})
    title = f"Pilot report · {run.get('target_model', 'unknown target')}"
    subtitle = f"{source.get('created', '')} · {source.get('status', 'unknown status')} · log {str(source.get('sha256', ''))[:12]}"
    template = Template((_TEMPLATE_DIR / "report.html").read_text())
    return template.substitute(
        title=html.escape(title), subtitle=html.escape(subtitle), navigation=navigation,
        sections=section_html, css=(_TEMPLATE_DIR / "style.css").read_text(),
        javascript=(_TEMPLATE_DIR / "report.js").read_text(),
    )
