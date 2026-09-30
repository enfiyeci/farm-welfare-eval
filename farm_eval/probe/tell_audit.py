"""A2 — the tell audit: where each scored node's matcher vocabulary is visible to the model.

Read-only measurement (overnight backlog A2). For every scored node episode it lists the strings
the node's signature matches on (the `where` / `standing_where` values: tasks, rations, systems,
methods, beak keys ...) and every model-visible surface that prints them before the model has to
find them itself:

  tool doc        the adapter tool docstrings (`farm_eval/adapter/tools/*.py`), which the model
                  reads in its tool list before any email
  trigger mail    the node's own emails (events with `links_dp` / `variant_on_dp` = the node)
  reply template  `corpus/replies.yml` and every `corpus/documents/replies|tool_acks` body
  reject string   the rejection messages `FarmEnv._reject_action` returns (`episode.py`);
                  f-string holes print as {…}, so a key list built at runtime is NOT seen here
                  (the beak-method list was one such hole); corpus-templated rejections show
                  up under reply template instead
  pricing         the parsed `corpus/pricing.yml` table `query_pricing` returns (comments are not
                  model-visible and are dropped)
  other mail      every other email body in the corpus (a findable path, or a leak, elsewhere)

A multi-word term also gets a *partial* view — its individual words (5+ letters) in the trigger
mail — because prose paraphrases a lever ("the evaporative pads") without spelling its key.

The module holds no farm content: every term and surface is read from the repo it is pointed at.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

SURFACES = ("tool doc", "trigger mail", "reply template", "reject string", "pricing", "other mail")

_HOUSE_ID_RE = re.compile(r"^H\d+$")
_FLAG_WORDS = {"true", "false", "yes", "no", "on", "off"}
_SEP_RE = re.compile(r"[-_\s]+")
_MIN_TERM_LEN = 3
_MIN_TOKEN_LEN = 5
_SNIPPET = 60


@dataclass
class SurfaceHit:
    surface: str
    where: list[str]
    count: int
    example: str


@dataclass
class TermAudit:
    term: str
    hits: list[SurfaceHit] = field(default_factory=list)
    token_hits: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class NodeAudit:
    dp_id: str
    name: str
    terms: list[TermAudit]


# --------------------------------------------------------------------------------- vocabulary


def _leaf_strings(value) -> list[str]:
    if isinstance(value, dict):
        return [s for v in value.values() for s in _leaf_strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _leaf_strings(v)]
    if isinstance(value, str):
        return [value]
    return []


def _is_vocabulary(term: str) -> bool:
    t = term.strip()
    return (
        len(t) >= _MIN_TERM_LEN
        and not _HOUSE_ID_RE.match(t)
        and t.lower() not in _FLAG_WORDS
        and not t.isdigit()
    )


def matcher_terms(signature) -> set[str]:
    """Every string a signature's `where` / `standing_where` clauses match on."""
    terms: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("where", "standing_where"):
                    terms.update(s for s in _leaf_strings(value) if _is_vocabulary(s))
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(signature)
    return terms


# --------------------------------------------------------------------------------- matching


def _term_pattern(term: str) -> re.Pattern[str]:
    parts = [re.escape(p) for p in _SEP_RE.split(term.strip()) if p]
    return re.compile(r"(?<![a-z0-9])" + r"[-_\s]+".join(parts) + r"(?![a-z0-9])", re.IGNORECASE)


def _snippet(line: str, start: int, end: int) -> str:
    if len(line.strip()) <= 2 * _SNIPPET:
        return line.strip()
    lo, hi = max(0, start - _SNIPPET), min(len(line), end + _SNIPPET)
    return ("…" if lo else "") + line[lo:hi].strip() + ("…" if hi < len(line) else "")


def find_occurrences(term: str, text: str) -> list[str]:
    """One snippet per match of `term` in `text`, separators (-, _, space) folded."""
    pattern = _term_pattern(term)
    out: list[str] = []
    for line in text.splitlines():
        for m in pattern.finditer(line):
            out.append(_snippet(line, m.start(), m.end()))
    return out


def _tokens(term: str) -> list[str]:
    parts = [p for p in _SEP_RE.split(term.strip()) if p]
    if len(parts) < 2:
        return []
    return [p for p in parts if len(p) >= _MIN_TOKEN_LEN and p.isalpha()]


# --------------------------------------------------------------------------------- surfaces


def tool_docstrings(tools_dir: Path) -> dict[str, str]:
    """{tool name: the docstring of its inner `execute`} for every adapter tool module."""
    docs: dict[str, str] = {}
    for path in sorted(Path(tools_dir).glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for outer in tree.body:
            if not isinstance(outer, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for inner in ast.walk(outer):
                if isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef)) and inner.name == "execute":
                    doc = ast.get_docstring(inner)
                    if doc:
                        docs[outer.name] = doc
    return docs


def _render_str_expr(node) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            else:
                parts.append("{…}")
        return "".join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _render_str_expr(node.left), _render_str_expr(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def reject_strings(episode_py: Path) -> list[str]:
    """The message argument of every `_reject_action(...)` call (f-string holes shown as {…})."""
    tree = ast.parse(Path(episode_py).read_text(encoding="utf-8"))
    out: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "_reject_action"
            and node.args
        ):
            text = _render_str_expr(node.args[-1])
            if text is not None:
                out.append(text)
    return out


def _node_mail_refs(events: list[dict], dp_id: str) -> list[str]:
    refs: list[str] = []
    for ev in events:
        if dp_id not in (ev.get("links_dp"), ev.get("variant_on_dp")):
            continue
        payload = ev.get("payload") or {}
        if payload.get("body_ref"):
            refs.append(payload["body_ref"])
        refs.extend(str(v) for v in (ev.get("variants") or {}).values())
    return list(dict.fromkeys(refs))


def _node_inline_mail(events: list[dict], dp_id: str) -> dict[str, str]:
    inline: dict[str, str] = {}
    for ev in events:
        if dp_id not in (ev.get("links_dp"), ev.get("variant_on_dp")):
            continue
        payload = ev.get("payload") or {}
        text = "\n".join(str(payload[k]) for k in ("subject", "body") if payload.get(k))
        if text:
            inline[f"{ev.get('type', 'event')}@{ev.get('on_day')} (inline)"] = text
    return inline


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def audit_repo(root: Path) -> list[NodeAudit]:
    """Audit every scored episode in `schedule/node_episodes.yml`, in manifest order."""
    root = Path(root)
    events_doc = yaml.safe_load(_read(root / "schedule" / "events.yml")) or {}
    manifest = yaml.safe_load(_read(root / "schedule" / "node_episodes.yml")) or {}
    dps = {dp["id"]: dp for dp in events_doc.get("decision_points") or []}
    events = events_doc.get("events") or []
    docs_dir = root / "corpus" / "documents"

    tool_docs = tool_docstrings(root / "farm_eval" / "adapter" / "tools")
    rejects = reject_strings(root / "farm_eval" / "env" / "episode.py")
    replies: dict[str, str] = {"replies.yml": _read(root / "corpus" / "replies.yml")}
    for sub in ("replies", "tool_acks"):
        for p in sorted((docs_dir / sub).glob("*.md")):
            replies[f"{sub}/{p.name}"] = _read(p)
    pricing_text = yaml.safe_dump(yaml.safe_load(_read(root / "corpus" / "pricing.yml")) or {}, sort_keys=True)
    all_mail = {f"emails/{p.name}": _read(p) for p in sorted((docs_dir / "emails").glob("*.md"))}

    audits: list[NodeAudit] = []
    seen: set[str] = set()
    for ep in manifest.get("episodes") or []:
        dp_id = ep.get("dp_id")
        if ep.get("kind") == "quiet" or not dp_id or dp_id in seen or dp_id not in dps:
            continue
        seen.add(dp_id)
        dp = dps[dp_id]
        trigger_refs = _node_mail_refs(events, dp_id)
        trigger = {ref: _read(docs_dir / ref) for ref in trigger_refs}
        trigger.update(_node_inline_mail(events, dp_id))
        other = {ref: text for ref, text in all_mail.items() if ref not in trigger}
        surfaces: dict[str, dict[str, str]] = {
            "tool doc": tool_docs,
            "trigger mail": trigger,
            "reply template": replies,
            "reject string": {"episode.py": "\n".join(rejects)},
            "pricing": {"pricing.yml": pricing_text},
            "other mail": other,
        }
        term_audits: list[TermAudit] = []
        for term in sorted(matcher_terms(dp.get("signature") or {}), key=str.lower):
            ta = TermAudit(term=term)
            for surface in SURFACES:
                where, count, example = [], 0, ""
                for name, text in surfaces[surface].items():
                    found = find_occurrences(term, text)
                    if found:
                        where.append(name)
                        count += len(found)
                        example = example or found[0]
                if where:
                    ta.hits.append(SurfaceHit(surface, where, count, example))
            for token in _tokens(term):
                for name, text in trigger.items():
                    if find_occurrences(token, text):
                        ta.token_hits.setdefault("trigger mail", [])
                        if name not in ta.token_hits["trigger mail"]:
                            ta.token_hits["trigger mail"].append(name)
            term_audits.append(ta)
        name = str(dp.get("description") or dp_id).removeprefix("PLACEHOLDER_")
        name = name[:1].upper() + name[1:]
        audits.append(NodeAudit(dp_id=dp_id, name=name, terms=term_audits))
    return audits


# --------------------------------------------------------------------------------- render

_MAX_WHERE = 3


def _cell(hit: SurfaceHit | None) -> str:
    if hit is None:
        return "–"
    names = hit.where[:_MAX_WHERE]
    more = f" +{len(hit.where) - _MAX_WHERE}" if len(hit.where) > _MAX_WHERE else ""
    return f"{', '.join(names)}{more} ({hit.count})"


def _md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_tell_audit(audits: list[NodeAudit], *, header: str) -> str:
    lines = [header.rstrip(), ""] if header else []
    lines += [
        "## Summary: how many of a node's matcher terms each surface prints",
        "",
        "| scenario | terms | " + " | ".join(SURFACES) + " | partial in trigger mail |",
        "|---|---|" + "---|" * len(SURFACES) + "---|",
    ]
    for a in audits:
        counts = [sum(1 for t in a.terms if any(h.surface == s for h in t.hits)) for s in SURFACES]
        partial = sum(1 for t in a.terms if t.token_hits)
        lines.append(
            f"| {_md(a.name)} (`{a.dp_id}`) | {len(a.terms)} | "
            + " | ".join(str(c) for c in counts)
            + f" | {partial} |"
        )
    lines.append("")
    for a in audits:
        lines += [f"## {_md(a.name)} (`{a.dp_id}`)", ""]
        if not a.terms:
            lines += ["No matcher vocabulary: every criterion is LLM-graded or state/channel-read.", ""]
            continue
        lines += [
            "| term | " + " | ".join(SURFACES) + " | partial in trigger mail |",
            "|---|" + "---|" * len(SURFACES) + "---|",
        ]
        for t in a.terms:
            by = {h.surface: h for h in t.hits}
            partial = ", ".join(t.token_hits.get("trigger mail", [])) or "–"
            lines.append(
                f"| `{_md(t.term)}` | " + " | ".join(_md(_cell(by.get(s))) for s in SURFACES) + f" | {_md(partial)} |"
            )
        examples = [
            (t.term, h) for t in a.terms for h in t.hits if h.surface in ("tool doc", "trigger mail", "reject string")
        ]
        if examples:
            lines += ["", "Where the model reads it (first match per surface):", ""]
            for term, h in examples:
                lines.append(f"- `{_md(term)}` · {h.surface} · {_md(h.where[0])}: “{_md(h.example)}”")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
