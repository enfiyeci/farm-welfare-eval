"""Dollar cost per node episode, prompt-cache diagnostics, and off-node action counts (B1/B2/B5).

Reads finished `.eval` logs only; it never calls a model. Prices are DATA: they live in
`scripts/model_prices.yml` (each model with its source URL and the date it was checked), never in
this module. Content-free: decision ids, tools and matchers come from the loaded schedule and the
recorded run.

Three layers, kept apart so the arithmetic is testable without a log:

- pure arithmetic: `RoleUsage`, `usage_cost`, `cache_diagnostics`, `prefix_changes`,
  `project_sweep`, `parse_probe_sessions`;
- transcript/ledger helpers: `action_split`, `action_message_positions`, `count_sessions`;
- the one Inspect-touching reader, `episodes_from_log`, and the markdown `render_markdown`.

Usage semantics. Inspect's `ModelUsage.input_tokens` is the UNCACHED ("fresh") input and
`input_tokens_cache_read` the cached part. Whether `reasoning_tokens` is already inside
`output_tokens` depends on the provider (Google reports thinking separately; OpenAI-style
providers fold it in), so the price table says per model whether reasoning is billed on top.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

import yaml

from farm_eval.analysis.attribute import attribute_events
from farm_eval.env.clock import SESSION_HEADER_PREFIX
from farm_eval.env.loader import Schedule
from farm_eval.report.reliability import _error_cause

# A call can only hit the implicit cache if the previous request was at least this long: Gemini's
# documented implicit-caching minimum is 1,024 tokens (Flash) to 4,096 (Pro); 4,096 is used so a
# "full miss" is never claimed on a prefix the provider may simply not cache.
MIN_CACHEABLE_PREFIX_TOKENS = 4096


# --- price table ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Rate:
    name: str
    input_per_mtok: float
    cached_input_per_mtok: float
    output_per_mtok: float
    cache_write_per_mtok: float = 0.0
    valid_from: str | None = None
    valid_until: str | None = None


@dataclass(frozen=True)
class ModelPrice:
    model: str
    source: str
    checked: str
    rates: tuple[Rate, ...]
    bill_reasoning_as_extra_output: bool = False
    notes: str = ""

    def rate(self, name: str | None) -> Rate | None:
        """The named rate; a model with ONE rate serves it for any name (it has no periods)."""
        for r in self.rates:
            if r.name == name:
                return r
        return self.rates[0] if len(self.rates) == 1 else None


def load_prices(path: str | Path) -> dict[str, ModelPrice]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    out: dict[str, ModelPrice] = {}
    for model, spec in (data.get("models") or {}).items():
        spec = spec or {}
        for key in ("source", "checked", "rates"):
            if not spec.get(key):
                raise ValueError(f"price table {path}: model {model!r} has no {key!r}")
        rates = []
        for r in spec["rates"]:
            rates.append(Rate(
                name=str(r["name"]),
                input_per_mtok=float(r["input_per_mtok"]),
                cached_input_per_mtok=float(r["cached_input_per_mtok"]),
                output_per_mtok=float(r["output_per_mtok"]),
                cache_write_per_mtok=float(r.get("cache_write_per_mtok", 0.0)),
                valid_from=str(r["from"]) if r.get("from") is not None else None,
                valid_until=str(r["until"]) if r.get("until") is not None else None,
            ))
        out[model] = ModelPrice(
            model=model, source=str(spec["source"]), checked=str(spec["checked"]),
            rates=tuple(rates),
            bill_reasoning_as_extra_output=bool(spec.get("bill_reasoning_as_extra_output", False)),
            notes=str(spec.get("notes", "")).strip(),
        )
    return out


# --- usage arithmetic ----------------------------------------------------------------------

@dataclass(frozen=True)
class RoleUsage:
    fresh_input: int = 0
    cached_input: int = 0
    output: int = 0
    reasoning: int = 0
    cache_write: int = 0

    @property
    def total_input(self) -> int:
        return self.fresh_input + self.cached_input + self.cache_write

    @property
    def cache_hit_rate(self) -> float | None:
        return self.cached_input / self.total_input if self.total_input else None

    def __add__(self, other: "RoleUsage") -> "RoleUsage":
        return RoleUsage(
            self.fresh_input + other.fresh_input, self.cached_input + other.cached_input,
            self.output + other.output, self.reasoning + other.reasoning,
            self.cache_write + other.cache_write,
        )


def role_usage_from(mu: Any) -> RoleUsage:
    if mu is None:
        return RoleUsage()
    return RoleUsage(
        fresh_input=int(getattr(mu, "input_tokens", 0) or 0),
        cached_input=int(getattr(mu, "input_tokens_cache_read", 0) or 0),
        output=int(getattr(mu, "output_tokens", 0) or 0),
        reasoning=int(getattr(mu, "reasoning_tokens", 0) or 0),
        cache_write=int(getattr(mu, "input_tokens_cache_write", 0) or 0),
    )


def usage_cost(u: RoleUsage, rate: Rate, *, bill_reasoning_as_extra_output: bool) -> float:
    billed_output = u.output + (u.reasoning if bill_reasoning_as_extra_output else 0)
    return (
        u.fresh_input * rate.input_per_mtok
        + u.cached_input * rate.cached_input_per_mtok
        + u.cache_write * rate.cache_write_per_mtok
        + billed_output * rate.output_per_mtok
    ) / 1e6


def usage_cost_parts(u: RoleUsage, rate: Rate, *, bill_reasoning_as_extra_output: bool) -> dict[str, float]:
    """The same bill split into fresh input / cached input / output (for the 'what dominates' line)."""
    billed_output = u.output + (u.reasoning if bill_reasoning_as_extra_output else 0)
    return {
        "fresh_input": u.fresh_input * rate.input_per_mtok / 1e6,
        "cached_input": (u.cached_input * rate.cached_input_per_mtok + u.cache_write * rate.cache_write_per_mtok) / 1e6,
        "output": billed_output * rate.output_per_mtok / 1e6,
    }


# --- per-call cache diagnostics (B2) -------------------------------------------------------

@dataclass(frozen=True)
class CallUsage:
    fresh_input: int
    cached_input: int
    working_time: float | None
    errored: bool

    @property
    def prompt(self) -> int:
        return self.fresh_input + self.cached_input


@dataclass(frozen=True)
class CacheDiagnostics:
    calls: int                    # calls that returned usage
    full_misses: int              # zero cached tokens although the previous prompt was cacheable
    fresh_total: int
    fresh_in_full_misses: int
    median_fresh_on_hits: float | None
    median_wt_hit: float | None
    median_wt_miss: float | None
    cached_total: int = 0
    reprefilled_in_full_misses: int = 0   # tokens a miss re-read that the previous call had already sent

    @property
    def miss_fresh_share(self) -> float | None:
        return self.fresh_in_full_misses / self.fresh_total if self.fresh_total else None

    @property
    def hit_rate_if_misses_hit(self) -> float | None:
        """The cache-hit rate had every full miss read the previous prompt from cache."""
        total = self.cached_total + self.fresh_total
        return (self.cached_total + self.reprefilled_in_full_misses) / total if total else None


def _median(xs: list[float]) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def cache_diagnostics(calls: list[CallUsage], *, min_cacheable: int = MIN_CACHEABLE_PREFIX_TOKENS) -> CacheDiagnostics:
    """Classify each call against the PREVIOUS successful call's prompt size.

    A 'full miss' is a call with zero cached tokens whose predecessor's prompt was long enough to
    be cached: the whole context was re-read at the fresh price. Because the request prefix is
    checked separately (`prefix_changes`), a full miss on an unchanged prefix is provider-side.
    """
    prev_prompt: int | None = None
    misses: list[CallUsage] = []
    hits: list[CallUsage] = []
    used: list[CallUsage] = []
    reprefilled = 0
    for c in calls:
        if c.errored or c.prompt == 0:
            continue
        used.append(c)
        if prev_prompt is not None and prev_prompt >= min_cacheable:
            if c.cached_input == 0:
                misses.append(c)
                reprefilled += min(prev_prompt, c.prompt)
            else:
                hits.append(c)
        elif c.cached_input > 0:
            hits.append(c)
        prev_prompt = c.prompt
    return CacheDiagnostics(
        calls=len(used),
        full_misses=len(misses),
        fresh_total=sum(c.fresh_input for c in used),
        fresh_in_full_misses=sum(c.fresh_input for c in misses),
        median_fresh_on_hits=_median([c.fresh_input for c in hits]),
        median_wt_hit=_median([c.working_time for c in hits if c.working_time is not None]),
        median_wt_miss=_median([c.working_time for c in misses if c.working_time is not None]),
        cached_total=sum(c.cached_input for c in used),
        reprefilled_in_full_misses=reprefilled,
    )


@dataclass(frozen=True)
class RequestShape:
    """What one request sent, as comparable fingerprints: one per message, plus tools and config."""
    messages: list[str]
    tools: str
    config: str


def prefix_changes(requests: list[RequestShape]) -> list[tuple[int, str]]:
    """(request index, what changed) wherever a request is NOT the previous request plus appended
    messages: a changed tool list, a changed generate config, or an earlier message rewritten or
    dropped. An empty list means every request's prefix is byte-stable, which is what a prompt
    cache needs from the harness side."""
    out: list[tuple[int, str]] = []
    for i in range(1, len(requests)):
        prev, cur = requests[i - 1], requests[i]
        if cur.tools != prev.tools:
            out.append((i, "tools"))
        if cur.config != prev.config:
            out.append((i, "config"))
        n = min(len(prev.messages), len(cur.messages))
        first = next((j for j in range(n) if prev.messages[j] != cur.messages[j]), None)
        if first is None and len(cur.messages) < len(prev.messages):
            first = len(cur.messages)
        if first is not None:
            out.append((i, f"message@{first}"))
    return out


def _fingerprint(obj: Any) -> str:
    dumped = obj.model_dump(exclude_none=True) if hasattr(obj, "model_dump") else obj
    return hashlib.sha256(json.dumps(dumped, sort_keys=True, default=str).encode()).hexdigest()


def request_shape(event: Any) -> RequestShape:
    return RequestShape(
        messages=[_fingerprint(m) for m in (event.input or [])],
        tools=_fingerprint([_fingerprint(t) for t in (event.tools or [])]),
        config=_fingerprint({"config": event.config, "tool_choice": str(event.tool_choice)}),
    )


# --- actions: scored node vs everything else (B5) and where the scored action sits (B6) ----

@dataclass(frozen=True)
class ActionSplit:
    total: int
    scored: int
    other_node: int              # strongly attributed to another decision, not the scored one
    unattributed: int            # strongly attributed to no decision at all
    first_scored_action: int | None   # index into the actions list
    ledger_rows: int = 0              # a ledger holding only the scored node cannot tell 'other' from 'none'
    unattributed_tools: tuple[tuple[str, int], ...] = ()   # most common tools among 'none', descending

    @property
    def off_node(self) -> int:
        return self.other_node + self.unattributed


def action_split(actions: list[dict], ledger: list[dict], schedule: Schedule, dp_id: str | None) -> ActionSplit:
    """Split the run's state-changing actions by the decision they strongly belong to, using the
    same attribution rules as the behaviour report (`farm_eval.analysis.attribute`). Each row is
    attributed on its own, so identical rows can never be confused with one another."""
    owners: list[set[str]] = []
    for row in actions:
        attributions, _ = attribute_events([row], [], [], list(ledger), schedule)
        owners.append({a.dp_id for a in attributions if a.strength == "strong"})
    scored_idx = [i for i, o in enumerate(owners) if dp_id is not None and dp_id in o]
    return ActionSplit(
        total=len(actions), scored=len(scored_idx),
        other_node=sum(1 for o in owners if o and (dp_id is None or dp_id not in o)),
        unattributed=sum(1 for o in owners if not o),
        first_scored_action=scored_idx[0] if scored_idx else None,
        ledger_rows=len(ledger),
        unattributed_tools=tuple(Counter(
            str(row.get("tool")) for row, o in zip(actions, owners) if not o
        ).most_common()),
    )


def _values_equal(a: Any, b: Any) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return float(a) == float(b)
    return a == b


def _args_cover(params: dict, arguments: dict) -> bool:
    """A recorded action's params are the call's arguments minus dropped empty optionals, so every
    recorded key must be present in the call with an equal value."""
    return all(k in arguments and _values_equal(v, arguments[k]) for k, v in params.items())


def action_message_positions(actions: list[dict], messages: list) -> list[int | None]:
    """0-based index of the assistant message whose tool call produced each recorded action.

    Actions are recorded in call order, so the alignment is monotone: each action claims the next
    unclaimed call (at or after the previous claim) with the same tool whose arguments cover the
    recorded params. Rejected calls never reached the action list and are skipped over."""
    calls: list[tuple[int, str, dict]] = []
    for i, m in enumerate(messages):
        if getattr(m, "role", None) == "assistant":
            for tc in getattr(m, "tool_calls", None) or []:
                calls.append((i, tc.function, dict(tc.arguments or {})))
    out: list[int | None] = []
    cursor = 0
    for row in actions:
        found = None
        for k in range(cursor, len(calls)):
            msg_i, fn, args = calls[k]
            if fn == row.get("tool") and _args_cover(row.get("params") or {}, args):
                found = k
                break
        if found is None:
            out.append(None)
            continue
        out.append(calls[found][0])
        cursor = found + 1
    return out


def _message_text(m: Any) -> str:
    text = getattr(m, "text", None)
    if text is None:
        content = getattr(m, "content", "")
        text = content if isinstance(content, str) else ""
    return text or ""


def count_sessions(messages: list) -> int:
    """Console sessions the model worked through: every session opens with the console header
    (the opening digest, each `end_day` result, and each forced-advance notice carry it)."""
    return sum(1 for m in messages if SESSION_HEADER_PREFIX in _message_text(m))


# --- one row per sample --------------------------------------------------------------------

@dataclass
class EpisodeCost:
    log: str
    sample_id: str
    episode_id: str
    dp_id: str | None
    scored: bool
    status: str                   # "ok" | "errored"
    error: str | None
    target_model: str | None
    grader_model: str | None
    target: RoleUsage
    grader: RoleUsage
    target_calls: int
    grader_calls: int
    wall_s: float | None
    sessions: int
    messages: int
    tool_calls: int
    cache: CacheDiagnostics
    prefix_changes: list[tuple[int, str]] = field(default_factory=list)
    actions: ActionSplit | None = None
    first_scored_message: int | None = None   # 1-based message position

    @property
    def first_scored_action_share(self) -> float | None:
        if self.first_scored_message is None or not self.messages:
            return None
        return self.first_scored_message / self.messages


def _role_of(event: Any) -> str:
    return "grader" if (getattr(event, "role", None) or "target") == "grader" else "target"


def episodes_from_log(
    log: Any, schedule: Schedule, *, target_model: str | None = None, grader_model: str | None = None,
    log_name: str = "",
) -> list[EpisodeCost]:
    roles = getattr(log.eval, "model_roles", None) or {}
    target_model = target_model or (roles["target"].model if "target" in roles else log.eval.model)
    grader_model = grader_model or (roles["grader"].model if "grader" in roles else None)
    rows: list[EpisodeCost] = []
    for s in log.samples or []:
        meta = s.metadata or {}
        model_events = [e for e in (s.events or []) if getattr(e, "event", None) == "model"]
        target_events = [e for e in model_events if _role_of(e) == "target"]
        grader_events = [e for e in model_events if _role_of(e) == "grader"]
        role_usage = getattr(s, "role_usage", None) or {}
        if role_usage:
            target_u = role_usage_from(role_usage.get("target"))
            grader_u = role_usage_from(role_usage.get("grader"))
        else:  # older logs: sum the events
            target_u = sum((role_usage_from(e.output.usage if e.output else None) for e in target_events), RoleUsage())
            grader_u = sum((role_usage_from(e.output.usage if e.output else None) for e in grader_events), RoleUsage())
        calls = [
            CallUsage(
                fresh_input=role_usage_from(e.output.usage if e.output else None).fresh_input,
                cached_input=role_usage_from(e.output.usage if e.output else None).cached_input,
                working_time=getattr(e, "working_time", None),
                errored=getattr(e, "error", None) is not None,
            )
            for e in target_events
        ]
        answered = [e for e in target_events if getattr(e, "error", None) is None and e.output and e.output.usage]
        messages = list(s.messages or [])
        env_state = (s.store or {}).get("EpisodeStore:env_state") or {}
        dp_id = meta.get("dp_id")
        scored = str(meta.get("scored", True)).lower() != "false"
        split = None
        first_msg = None
        actions = env_state.get("actions") or []
        if env_state:
            split = action_split(actions, env_state.get("ledger") or [], schedule, dp_id if scored else None)
            if split.first_scored_action is not None:
                pos = action_message_positions(actions, messages)[split.first_scored_action]
                first_msg = pos + 1 if pos is not None else None
        err = getattr(s, "error", None)
        rows.append(EpisodeCost(
            log=log_name, sample_id=str(s.id), episode_id=str(meta.get("episode_id", s.id)), dp_id=dp_id,
            scored=scored, status="errored" if err is not None else "ok",
            error=_error_cause(err) if err is not None else None,
            target_model=target_model, grader_model=grader_model,
            target=target_u, grader=grader_u,
            target_calls=len(answered), grader_calls=len(grader_events),
            wall_s=getattr(s, "total_time", None),
            sessions=count_sessions(messages), messages=len(messages),
            tool_calls=sum(len(getattr(m, "tool_calls", None) or []) for m in messages if getattr(m, "role", None) == "assistant"),
            cache=cache_diagnostics(calls),
            prefix_changes=prefix_changes([request_shape(e) for e in answered]),
            actions=split, first_scored_message=first_msg,
        ))
    return rows


def row_cost(row: EpisodeCost, prices: dict[str, ModelPrice], *, rate_name: str | None) -> tuple[float | None, float | None]:
    """($ target, $ grader) at the named rate; None where the model has no price on file."""
    def one(model: str | None, u: RoleUsage) -> float | None:
        mp = prices.get(model or "")
        if mp is None:
            return None if (u.total_input or u.output) else 0.0
        rate = mp.rate(rate_name)
        if rate is None:
            return None
        return usage_cost(u, rate, bill_reasoning_as_extra_output=mp.bill_reasoning_as_extra_output)
    return one(row.target_model, row.target), one(row.grader_model, row.grader)


# --- sweep projection ----------------------------------------------------------------------

def parse_probe_sessions(md: str) -> dict[str, tuple[int, bool]]:
    """{episode: (sessions the model works through, scored)} from a `probe_node_snapshots.py`
    report. The probe's 'runtime sessions (good arm)' list is the days the clock stops at AFTER
    the start, so the opening session is added. An episode whose `dp` is '-' is quiet (unscored)."""
    out: dict[str, tuple[int, bool]] = {}
    header: list[str] | None = None
    for line in md.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if "episode" not in header or "runtime sessions (good arm)" not in header or "dp" not in header:
            continue
        row = dict(zip(header, cells))
        m = re.search(r"\((\d+)\)\s*$", row["runtime sessions (good arm)"])
        if not m:
            continue
        out[row["episode"]] = (int(m.group(1)) + 1, row["dp"] not in ("-", ""))
    return out


@dataclass(frozen=True)
class SweepProjection:
    k: int
    episodes: int
    sessions: int
    usd: float
    wall_s: float                 # one connection, episodes back to back


def project_sweep(
    sessions: dict[str, tuple[int, bool]], *, target_usd_per_session: float, wall_s_per_session: float,
    grader_usd_per_scored_episode: float, k: int,
) -> SweepProjection:
    n_sessions = sum(n for n, _ in sessions.values())
    n_scored = sum(1 for _, scored in sessions.values() if scored)
    usd = n_sessions * target_usd_per_session + n_scored * grader_usd_per_scored_episode
    return SweepProjection(k=k, episodes=len(sessions), sessions=n_sessions * k, usd=usd * k,
                           wall_s=n_sessions * wall_s_per_session * k)


# --- markdown ------------------------------------------------------------------------------

def _fmt_usd(x: float | None) -> str:
    return "n/a" if x is None else f"${x:.2f}"


def _fmt_pct(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.0%}"


def _fmt_min(s: float | None) -> str:
    return "n/a" if s is None else f"{s / 60:.0f}"


def _rate_label(prices: dict[str, ModelPrice], model: str | None, rate_name: str) -> str:
    mp = prices.get(model or "")
    r = mp.rate(rate_name) if mp else None
    if r is None:
        return rate_name
    return f"{rate_name} (${r.input_per_mtok:g} fresh / ${r.cached_input_per_mtok:g} cached / ${r.output_per_mtok:g} output per 1M)"


def _rates_for(prices: dict[str, ModelPrice], model: str | None, rate_names: list[str] | None) -> list[str]:
    mp = prices.get(model or "")
    if mp is None:
        return []
    names = [r.name for r in mp.rates]
    return [n for n in names if rate_names is None or n in rate_names] or ([names[0]] if len(names) == 1 else [])


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _fmt_s(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.1f}"


def render_markdown(
    rows: list[EpisodeCost], prices: dict[str, ModelPrice], *, rate_names: list[str] | None = None,
    probe_sessions: dict[str, tuple[int, bool]] | None = None, ks: Iterable[int] = (1, 5),
) -> str:
    """Markdown report. Costs use each target model's own rates from the price table
    (`rate_names` narrows them); summaries and the sweep projection are grouped per target model."""
    lines: list[str] = []
    ok = [r for r in rows if r.status == "ok"]
    models = sorted({r.target_model for r in rows if r.target_model})

    lines.append("## Cost per episode")
    lines.append("")
    lines.append("$ total is target + grader at each of the target model's rates (see Price sources). "
                 "Fresh-input share is the share of the target bill spent on uncached input, at the first rate. "
                 "Wall time is the sample's total time.")
    lines.append("")
    lines.append("| episode | status | target model | $ target | $ grader | $ total, per rate | fresh-input share of $ "
                 "| cache hit | full cache misses | calls | sessions | wall (min) |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        names = _rates_for(prices, r.target_model, rate_names)
        first = names[0] if names else None
        t, g = row_cost(r, prices, rate_name=first) if first else (None, None)
        per_rate = []
        for rn in names:
            tt, gg = row_cost(r, prices, rate_name=rn)
            per_rate.append(f"{rn} {_fmt_usd(None if tt is None or gg is None else tt + gg)}")
        share = None
        mp = prices.get(r.target_model or "")
        rate = mp.rate(first) if (mp and first) else None
        if rate is not None and t:
            share = usage_cost_parts(r.target, rate, bill_reasoning_as_extra_output=mp.bill_reasoning_as_extra_output)["fresh_input"] / t
        status = "ok" if r.status == "ok" else f"errored: {r.error or ''}"
        lines.append(
            f"| {r.episode_id} | {_cell(status)} | {r.target_model} | {_fmt_usd(t)} | {_fmt_usd(g)} | {' · '.join(per_rate) or 'n/a'} "
            f"| {_fmt_pct(share)} | {_fmt_pct(r.target.cache_hit_rate)} | {r.cache.full_misses}/{r.cache.calls} "
            f"| {r.target_calls} | {r.sessions} | {_fmt_min(r.wall_s)} |"
        )
    lines.append("")

    for model in models:
        scored_ok = [r for r in ok if r.scored and r.target_model == model]
        errored = [r for r in rows if r.status == "errored" and r.target_model == model]
        names = _rates_for(prices, model, rate_names)
        if not names or not (scored_ok or errored):
            continue
        mp = prices[model]
        if scored_ok:
            lines.append(f"### {model}: scored, completed episodes (n={len(scored_ok)})")
            lines.append("")
            lines.append("| rate | mean $ target | mean $ grader | mean $ total | min | max | fresh-input share of target $ |")
            lines.append("|---|---|---|---|---|---|---|")
            for rn in names:
                costs = [row_cost(r, prices, rate_name=rn) for r in scored_ok]
                if any(t is None or g is None for t, g in costs):
                    lines.append(f"| {rn} | n/a (a grader model has no price at this rate) | | | | | |")
                    continue
                totals = [t + g for t, g in costs]
                tsum = sum(t for t, _ in costs)
                fresh = sum(usage_cost_parts(r.target, mp.rate(rn), bill_reasoning_as_extra_output=mp.bill_reasoning_as_extra_output)["fresh_input"]
                            for r in scored_ok)
                lines.append(
                    f"| {_rate_label(prices, model, rn)} | {_fmt_usd(mean(t for t, _ in costs))} "
                    f"| {_fmt_usd(mean(g for _, g in costs))} | {_fmt_usd(mean(totals))} | {_fmt_usd(min(totals))} "
                    f"| {_fmt_usd(max(totals))} | {_fmt_pct(fresh / tsum if tsum else None)} |"
                )
            lines.append("")
            wall = [r.wall_s for r in scored_ok if r.wall_s is not None]
            lines.append(f"Mean wall time {_fmt_min(mean(wall) if wall else None)} min; mean {mean(r.target_calls for r in scored_ok):.0f} "
                         f"target calls and {mean(r.sessions for r in scored_ok):.1f} sessions per episode.")
            lines.append("")
        if errored:
            burned = []
            for rn in names:
                costs = [row_cost(r, prices, rate_name=rn) for r in errored]
                if all(t is not None for t, _ in costs):
                    burned.append(f"{rn} {_fmt_usd(sum(t + (g or 0) for t, g in costs))}")
            wall = sum(r.wall_s or 0 for r in errored)
            lines.append(f"{model}: {len(errored)} errored sample(s) spent {' · '.join(burned) or 'n/a'} and "
                         f"{wall / 60:.0f} min with no score.")
            lines.append("")

        with_sessions = [r for r in scored_ok if r.sessions > 0]
        if probe_sessions and with_sessions:
            n_sess = sum(n for n, _ in probe_sessions.values())
            per_session_s = sum(r.wall_s or 0 for r in with_sessions) / sum(r.sessions for r in with_sessions)
            lines.append(f"### {model}: sweep projection")
            lines.append("")
            lines.append(f"{len(probe_sessions)} episodes and {n_sess} sessions per k=1 sweep, from the probe's runtime "
                         f"session counts (good arm, plus the opening session). Per-session target cost and wall time are "
                         f"the means over the {len(with_sessions)} scored episodes above; the grader is charged once per "
                         "scored episode. Wall time is back to back on one connection; divide by the concurrency you get.")
            lines.append("")
            lines.append("| rate | k | sessions | $ | wall (h, one connection) |")
            lines.append("|---|---|---|---|---|")
            for rn in names:
                costs = [row_cost(r, prices, rate_name=rn) for r in with_sessions]
                if any(t is None or g is None for t, g in costs):
                    continue
                per_session_usd = sum(t for t, _ in costs) / sum(r.sessions for r in with_sessions)
                grader_per_ep = mean(g for _, g in costs)
                for k in ks:
                    p = project_sweep(probe_sessions, target_usd_per_session=per_session_usd,
                                      wall_s_per_session=per_session_s, grader_usd_per_scored_episode=grader_per_ep, k=k)
                    lines.append(f"| {rn} | {k} | {p.sessions} | {_fmt_usd(p.usd)} | {p.wall_s / 3600:.1f} |")
            lines.append("")

    lines.append("## Where each episode spends its actions (B5, B6)")
    lines.append("")
    lines.append("State-changing actions only (reads excluded). 'Other decision' = strongly attributed to a "
                 "different decision on the ledger; 'none' = attributed to no decision (routine work such as "
                 "feed orders). A run whose ledger holds only the scored decision (ledger rows = 1, runs before "
                 "the 2026-09-22 'every decision on the ledger' change) cannot tell 'other' from 'none'. 'First "
                 "scored action' is the transcript message of the first action attributed to the scored decision; "
                 "'none' there means the node was decided without a matching action (by email, by declining, or "
                 "not at all).")
    lines.append("")
    lines.append("| episode | ledger rows | tool calls | actions | scored decision | other decision | none | off-node share "
                 "| top 'none' tools | first scored action (message / total) | transcript after it |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in ok:
        a = r.actions
        if a is None:
            continue
        off_share = a.off_node / a.total if a.total else None
        first = f"{r.first_scored_message} / {r.messages}" if r.first_scored_message else f"none / {r.messages}"
        after = None if r.first_scored_action_share is None else 1 - r.first_scored_action_share
        top = ", ".join(f"{tool} {n}" for tool, n in a.unattributed_tools[:3])
        lines.append(f"| {r.episode_id} | {a.ledger_rows} | {r.tool_calls} | {a.total} | {a.scored} | {a.other_node} | {a.unattributed} "
                     f"| {_fmt_pct(off_share)} | {top} | {first} | {_fmt_pct(after)} |")
    lines.append("")

    lines.append("## Prompt cache (B2)")
    lines.append("")
    lines.append("A full miss is a call that read zero cached tokens although the previous prompt was cacheable "
                 f"(>= {MIN_CACHEABLE_PREFIX_TOKENS} tokens). Prefix changes counts requests that were NOT the "
                 "previous request plus appended messages (tools, config, or an earlier message changed).")
    lines.append("")
    lines.append("'Hit rate if misses hit' assumes each full miss had read the previous call's prompt from cache; "
                 "'$ lost to misses' prices those re-read tokens at the fresh minus the cached rate (first rate).")
    lines.append("")
    lines.append("| episode | target model | cache hit | full misses | fresh input in full misses | hit rate if misses hit "
                 "| $ lost to misses | median fresh on hits | median call s (hit / miss) | prefix changes |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        c = r.cache
        wt = f"{_fmt_s(c.median_wt_hit)} / {_fmt_s(c.median_wt_miss)}"
        mp = prices.get(r.target_model or "")
        names = _rates_for(prices, r.target_model, rate_names)
        rate = mp.rate(names[0]) if (mp and names) else None
        lost = None if rate is None else c.reprefilled_in_full_misses * (rate.input_per_mtok - rate.cached_input_per_mtok) / 1e6
        lines.append(f"| {r.episode_id} | {r.target_model} | {_fmt_pct(r.target.cache_hit_rate)} | {c.full_misses}/{c.calls} "
                     f"| {_fmt_pct(c.miss_fresh_share)} | {_fmt_pct(c.hit_rate_if_misses_hit)} | {_fmt_usd(lost)} | {'n/a' if c.median_fresh_on_hits is None else f'{c.median_fresh_on_hits:.0f}'} "
                     f"| {wt} | {len(r.prefix_changes)} |")
    lines.append("")

    for model in models:
        scored_ok = [r for r in ok if r.scored and r.target_model == model]
        mp = prices.get(model)
        names = _rates_for(prices, model, rate_names)
        if not scored_ok or mp is None or not names:
            continue
        rate = mp.rate(names[0])
        lost = [r.cache.reprefilled_in_full_misses * (rate.input_per_mtok - rate.cached_input_per_mtok) / 1e6 for r in scored_ok]
        cached = sum(r.cache.cached_total for r in scored_ok)
        fresh = sum(r.cache.fresh_total for r in scored_ok)
        re_read = sum(r.cache.reprefilled_in_full_misses for r in scored_ok)
        changes = sum(len(r.prefix_changes) for r in scored_ok)
        lines.append(f"{model}, {len(scored_ok)} scored episodes: cache hit {_fmt_pct(cached / (cached + fresh) if cached + fresh else None)}, "
                     f"{_fmt_pct((cached + re_read) / (cached + fresh) if cached + fresh else None)} if every full miss had hit; "
                     f"full misses cost {_fmt_usd(mean(lost))} per episode on average at the {names[0]} rate "
                     f"(max {_fmt_usd(max(lost))}); {changes} prefix change(s) in all.")
        lines.append("")

    lines.append("## Price sources")
    lines.append("")
    for model in sorted({r.target_model for r in rows} | {r.grader_model for r in rows} - {None}):
        mp = prices.get(model or "")
        if mp is None:
            lines.append(f"- {model}: no price on file")
            continue
        lines.append(f"- {model}: {mp.source} (checked {mp.checked})" + (f". {mp.notes}" if mp.notes else ""))
    lines.append("")
    return "\n".join(lines)
