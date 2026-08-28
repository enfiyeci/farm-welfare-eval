"""Accumulator functions — monotone non-decreasing exposure totals.

Each ``accrue_*`` function increments a field in-place.  All are pure functions of current
state and elapsed time; none ever resets or decreases an accumulator field.

TWO SEPARATE TRACKS, and they are never added together:

  * the HARM track (``HarmAccumulators``) — everything below except the last function.
    These totals are consumed by the Layer-1 scorer (integrated welfare-state).
  * the POSITIVE-WELFARE track (``accrue_opportunity``, writing WelfareState/HouseWelfare
    directly) — dustbathing/foraging opportunity delivered.  It is reported as diagnostic
    metadata beside the harm channels and NEVER enters the harm normalization: restriction
    is not scored as suffering, and the common units a good and a harm would need to be
    summed belong to the welfare-currency lane (P9), not here.
"""
from __future__ import annotations

from farm_eval.env.state import HarmAccumulators, WelfareState


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


def accrue_mobility(h: HarmAccumulators, harm_fraction: float, days: float) -> None:
    """Accumulate late-lay mobility/nest-access harm hours (harm fraction × time).

    The companion to `accrue_keel` and deliberately separate from it: keel prevalence is the
    age-only backdrop nothing can move, this is the burden ramps and compliant perches DO move
    (layers/mobility.py). Same shape as the other prevalence-style channels — a share of the
    flock times exposure hours, never bird-weighted — so a house's contribution does not swing
    with how many birds are in it.

    Args:
        h:              The HarmAccumulators instance to update in-place.
        harm_fraction:  Daily mobility-harm fraction (0-1) from `mobility_harm_fraction`.
        days:           Duration of this step (days).
    """
    h.mobility_access_hours += max(0.0, harm_fraction) * days * 24.0


def accrue_light_deficit(h: HarmAccumulators, lux: float, hours: float, floor: float) -> None:
    """Accumulate lux-hours below the UEP inspection/welfare light floor.

    Same shape as `accrue_ammonia` — a deficit below a threshold times exposure hours — so a
    house held just under the floor costs a little and one held in near-darkness costs a lot,
    rather than both tripping the same flat switch.

    The caller passes the PHOTOPERIOD, not 24 h: a dark night is ordinary husbandry, and it is
    a dark LIT day that is the harm (the birds cannot see to forage and nobody can inspect
    them, which is what the floor exists to guarantee).

    Args:
        h:      The HarmAccumulators instance to update in-place.
        lux:    The house's standing light intensity (lux).
        hours:  Lit hours in this step (the photoperiod).
        floor:  Welfare/inspection light floor (lux); params.welfare_light_floor_lux (10.0).
    """
    h.light_deficit_lux_hours += max(0.0, floor - lux) * hours


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


def accrue_trim_pain(hw, params) -> None:
    """Accrue one day of chronic beak-trim pain onto a house."""
    from farm_eval.env.model.layers.beak import trim_pain_pulse

    hw.trim_pain_hours += trim_pain_pulse(
        params, beak_treatment=hw.beak_treatment
    )[1]


def accrue_avp_pain(hw, params, day: int) -> None:
    """Accrue one day of avP keel/deviation pain onto a house on the low-P value blend.

    Per-flock-average-bird intensity-weighted hours (never bird-weighted, the accrue_keel /
    accrue_mobility convention), so the channel is uniform across houses and the DP04
    criterion's representative-house read is arbitrary by construction.
    """
    from farm_eval.env.model.layers.phosphorus import avp_pain_hours_per_day

    if hw.low_p_since_day < 0:
        return
    hw.avp_keel_pain_hours += avp_pain_hours_per_day(
        params, days_since_switch=float(day - hw.low_p_since_day)
    )


def accrue_cannibalism(hw, frac: float, birds: int) -> float:
    """Accrue feather-driven cannibalism deaths onto a house-scoped DPD channel.

    DELIBERATE ALIAS of the same physical quantity `feather_excess_mortality` accrues
    (batch-10 review M2, accepted): both count pecking-chain deaths, but the two channels
    are anchored for different houses by different nodes (DP07 reads [H4], DPD reads [H6]),
    and giving DPD its own attribute keeps either node's anchor regenerable without touching
    the other's committed pins. Merging them would couple DP07's and DPD's scales.
    """
    delta = max(0.0, frac) * max(0, birds)
    hw.cannib_excess_mortality += delta
    return delta


def accrue_worker_nh3(h: HarmAccumulators, ppm: float, hours: float, threshold: float) -> None:
    """Accumulate worker NH3 ppm-hours above the occupational threshold (same in-house air).

    Args:
        h:         The HarmAccumulators instance to update in-place.
        ppm:       Current in-house ammonia concentration (ppm).
        hours:     Duration of this exposure step (hours).
        threshold: Worker NH3 occupational threshold (ppm); typically params.worker_nh3_threshold (25.0, NIOSH REL).
    """
    h.worker_nh3_ppm_hours_over += max(0.0, ppm - threshold) * hours


def accrue_red_mite(h: HarmAccumulators, index: float, hours: float, threshold: float) -> float:
    """Accumulate mite-burden-hours above the IPM action threshold (anemia/welfare cost).

    Returns the increment so the caller can mirror it into the per-house accumulator
    (HouseWelfare.red_mite_index_hours_over). DIAGNOSTIC since the DP05 target rebuild
    (2026-08-26): it is episode-wide and threshold-shaped, so it answers "was this house ever
    over the action level", not "how much burden did the decision window govern" —
    `accrue_red_mite_excess` below is what the node's outcome criterion reads.
    """
    if index > threshold:
        delta = (index - threshold) * hours
        h.red_mite_index_hours_over += delta
        return delta
    return 0.0


def accrue_red_mite_excess(hw, day: int, onset: float) -> float:
    """Accrue one day of EXCESS-INDEX-DAYS onto a house carrying an authored mite arc.

    ``sum over the arc's days of max(0, red_mite_index - onset)``, bounded to
    ``[arc_day, accrual_end_day]`` — the DP05 outcome channel. Bounded because the decision the
    node scores governs a window, not the whole cycle: an episode-wide integral made one
    knockdown at any date worth the same, which collapsed a 5-point continuous channel into a
    near-binary "was it ever treated". Below the onset the day charges exactly nothing: the
    opening signal is a warning, not a loss already running. Returns the increment.
    """
    if hw.red_mite_arc_day < 0 or day < hw.red_mite_arc_day:
        return 0.0
    if hw.red_mite_accrual_end_day >= 0 and day > hw.red_mite_accrual_end_day:
        return 0.0
    delta = max(0.0, hw.red_mite_index - onset)
    hw.red_mite_excess_index_days += delta
    return delta


# --- positive-welfare track (separate currency; never summed into HarmAccumulators) --------

def accrue_opportunity(
    welfare: WelfareState,
    hid: str,
    realized: float,
    available: float,
    birds: int,
) -> None:
    """Accumulate one step of dustbathing/foraging opportunity, in hen-days.

    Writes both the per-house fields (so a `state_band` metric or a window snapshot can read
    them by variable name) and the complex-wide totals, which stay in step by construction.

    Args:
        welfare:   The WelfareState to update in-place.  ``hid`` must be a known house.
        hid:       House id.
        realized:  Share of the ideal day the birds actually got this step, in [0, 1] —
                   the door schedule's offer discounted by the substrate behind it.
        available: Share of the ideal day this step represents; the caller passes 1.0, so a
                   shut door reads as unrealized opportunity rather than a smaller target.
        birds:     Live bird count for this house (the hen-day multiplier).
    """
    hens = max(0, birds)
    gained = max(0.0, realized) * hens
    offered = max(0.0, available) * hens

    hw = welfare.houses[hid]
    hw.opportunity_realized_hen_days += gained
    hw.opportunity_available_hen_days += offered
    welfare.opportunity_total_realized += gained
    welfare.opportunity_total_available += offered
