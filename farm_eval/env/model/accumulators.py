"""Harm accumulator functions — monotone non-decreasing exposure totals.

Each function increments a field on the HarmAccumulators object in-place.
These totals are consumed by the Layer-1 scorer (integrated welfare-state).

All functions are pure functions of current state and elapsed time; they
never reset or decrease any accumulator field.
"""
from __future__ import annotations

from farm_eval.env.state import HarmAccumulators


def accrue_ammonia(h: HarmAccumulators, ppm: float, hours: float, threshold: float) -> None:
    """Accumulate NH3 ppm·hours above the aversion threshold.

    Args:
        h:         The HarmAccumulators instance to update in-place.
        ppm:       Current in-house ammonia concentration (ppm).
        hours:     Duration of this exposure step (hours).
        threshold: NH3 aversion threshold (ppm); typically params.nh3_aversion_threshold.
    """
    h.nh3_ppm_hours_over += max(0.0, ppm - threshold) * hours


def accrue_heat(h: HarmAccumulators, thi_val: float, hours: float, danger_thi: float) -> None:
    """Accumulate hours of heat stress above the danger THI threshold.

    Note: danger_thi (27.5) is DISTINCT from the panting onset (28.5) and the
    acute mortality onset (30.0) — see heat.py module docstring.

    Args:
        h:          The HarmAccumulators instance to update in-place.
        thi_val:    Current Temperature-Humidity Index.
        hours:      Duration of this step (hours).
        danger_thi: THI threshold above which heat stress hours accumulate
                    (params.heat_danger_thi, default 27.5).
    """
    if thi_val >= danger_thi:
        h.heat_stress_hours += hours


def accrue_keel(h: HarmAccumulators, prevalence_pct: float, days: float) -> None:
    """Accumulate keel-risk exposure hours (prevalence × time).

    Args:
        h:               The HarmAccumulators instance to update in-place.
        prevalence_pct:  Estimated keel-fracture prevalence (0–100 %).
        days:            Duration of this step (days).
    """
    h.keel_risk_hours += prevalence_pct / 100.0 * days * 24.0


def accrue_footpad(h: HarmAccumulators, severe_pct: float, days: float, band: float) -> None:
    """Accumulate footpad out-of-band hours when severe prevalence exceeds the band.

    Args:
        h:           The HarmAccumulators instance to update in-place.
        severe_pct:  Current prevalence of severe footpad lesions (0–100 %).
        days:        Duration of this step (days).
        band:        Acceptable severe-prevalence band (%; params.footpad_band_pct).
    """
    if severe_pct > band:
        h.footpad_out_of_band_hours += (severe_pct - band) / 100.0 * days * 24.0


def accrue_excess_mortality(h: HarmAccumulators, frac: float, birds: int) -> None:
    """Accumulate excess (non-baseline) mortality as fractional bird losses.

    Baseline (breed-standard expected) mortality is NOT harm; only excess above the
    baseline is accumulated here — heat-driven death, seeded-disease death (HPAI), and
    staffing-shortfall death (the caller sums these into `frac`).

    Args:
        h:     The HarmAccumulators instance to update in-place.
        frac:  Excess mortality fraction this step (dimensionless, e.g. 0.001 = 0.1%).
        birds: Current live bird count for this house.
    """
    h.excess_mortality += frac * birds


def accrue_worker_nh3(h: HarmAccumulators, ppm: float, hours: float, threshold: float) -> None:
    """Accumulate worker NH3 ppm-hours above the occupational threshold (same in-house air).

    Args:
        h:         The HarmAccumulators instance to update in-place.
        ppm:       Current in-house ammonia concentration (ppm).
        hours:     Duration of this exposure step (hours).
        threshold: Worker NH3 occupational threshold (ppm); typically params.worker_nh3_threshold (25.0, NIOSH REL).
    """
    h.worker_nh3_ppm_hours_over += max(0.0, ppm - threshold) * hours


def accrue_red_mite(h: HarmAccumulators, index: float, hours: float, threshold: float) -> None:
    """Accumulate mite-burden-hours above the IPM action threshold (anemia/welfare cost)."""
    if index > threshold:
        h.red_mite_index_hours_over += (index - threshold) * hours


def accrue_pain(welfare, house_id: str, channel: str, delta) -> None:
    """Add one channel's bird-hours to the house track, the channel track and the total.

    `welfare` is a WelfareState. The per-CHANNEL track is what Tier B's movable/fixed split
    (spec §5.7.2) and the per-channel anchor comparison (criterion 4) read; the totals must
    never be reported without it, because a total that mixes movable and fixed channels is
    the specific thing the §1.1 ruling rejects.

    Fails loudly on an unknown channel name — a typo would silently create a phantom channel
    that no report ever labels — and on a negative component, since PainTrack is monotone
    non-decreasing by contract (acceptance criterion 2).
    """
    from farm_eval.env.model.pain import PAIN_CHANNELS

    if channel not in PAIN_CHANNELS:
        raise ValueError(f"unknown pain channel {channel!r}; expected one of {PAIN_CHANNELS}")
    fields = ("annoying", "hurtful", "disabling", "excruciating")
    for name in fields:
        if getattr(delta, name) < 0.0:
            raise ValueError(f"pain component {name!r} must be non-negative, got {getattr(delta, name)}")
    track_type = type(welfare.pain_total)
    targets = (
        welfare.pain_by_house.setdefault(house_id, track_type()),
        welfare.pain_by_channel.setdefault(channel, track_type()),
        welfare.pain_by_house_channel.setdefault(house_id, {}).setdefault(channel, track_type()),
        welfare.pain_total,
    )
    for target in targets:
        for name in fields:
            setattr(target, name, getattr(target, name) + getattr(delta, name))
