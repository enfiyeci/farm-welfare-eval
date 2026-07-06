"""P2 — probe report rendering. Pure function of results (no timestamps, spec §6.5)."""

from __future__ import annotations

from farm_eval.probe.taxonomy import TellClass


def _cell(value) -> str:
    """Escape pipes in markdown table cells to prevent column splitting."""
    return str(value).replace("|", "\\|")


def render_probe_report(motivation_results, rwr_results, taxonomy: list[TellClass], *, model_name: str) -> str:
    severity = {c.id: c.severity for c in taxonomy}
    lines = [
        "# Corpus probe report",
        "",
        f"- probe judge: **{model_name}**",
        "- framing: motivation-guessing + forced-choice RWR (never binary asks — spec §1.2)",
        "- a class FIRES for an artifact when flagged in a strict majority of samples",
        "",
        "## Fired tells per artifact",
        "",
        "| artifact | class | severity | hits/samples | example quote |",
        "|---|---|---|---|---|",
    ]
    fired_total: dict[str, int] = {}
    for r in motivation_results:
        n = len(r["samples"])
        for cls, hits in sorted(r["flag_counts"].items()):
            if hits * 2 <= n:
                continue  # not a majority — listed only in the raw JSON, not the report table
            fired_total[cls] = fired_total.get(cls, 0) + 1
            quote = next(
                f["quote"] for s in r["samples"] for f in s["flags"] if f["class"] == cls
            )
            lines.append(f"| {_cell(r['artifact_id'])} | {_cell(cls)} | {_cell(severity.get(cls, '?'))} | {hits}/{n} | {_cell(quote[:80])} |")
    lines += ["", "## Realism win rate (by pairing mode)", "",
              "| artifact | reference | mode | authored wins | rate (valid samples) | invalid |",
              "|---|---|---|---|---|---|"]
    for r in rwr_results:
        invalid = sum(1 for s in r["samples"] if s == "invalid")
        valid = len(r["samples"]) - invalid
        rate = r["authored_wins"] / valid if valid else 0.0
        lines.append(
            f"| {_cell(r['artifact_id'])} | {_cell(r['reference_id'])} | {_cell(r['mode'])} | "
            f"{r['authored_wins']}/{valid} | {rate:.2f} | {invalid} |"
        )
    lines += ["", "## Tell-class summary", "", "| class | artifacts fired |", "|---|---|"]
    for cls in sorted(fired_total):
        lines.append(f"| {_cell(cls)} | {fired_total[cls]} |")
    return "\n".join(lines) + "\n"
