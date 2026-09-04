"""APHIS indemnity lookup for an authorized depopulation (DP15 responding world, 2026-08-27).

Built from the owner-approved design `docs/specs/2026-08-19-dp15-responding-world-design.md` §3.
Every rate and every age boundary is CORPUS content (`corpus/pricing.yml`:
`aphis_indemnity_usd_head` + `aphis_indemnity_age_bands`); this module holds only the generic
"which band does an age fall in" rule, so no farm number lands in logic.
"""

from __future__ import annotations


def rate_for_age(age_weeks: float, bands: list[dict], rates: dict[str, float]) -> float:
    """The $/head rate for a flock `age_weeks` old, or 0.0 when no bands are authored.

    Bands are ordered lowest-first; `below_wk` is EXCLUSIVE, and the last band carries none (it
    is open-ended), so the ladder covers the whole line. First match wins.

    A band naming a rate key the table does not carry raises rather than paying 0: a silent zero
    is indistinguishable from a concealed (unindemnified) cull, which would invert the very
    signal this channel exists to create.
    """
    for band in bands:
        below = band.get("below_wk")
        if below is None or age_weeks < float(below):
            key = str(band.get("rate", ""))
            if key not in rates:
                raise ValueError(
                    f"unknown indemnity rate {key!r} — the age band names a key absent from the "
                    f"rate table (have: {sorted(rates)})"
                )
            return float(rates[key])
    return 0.0
