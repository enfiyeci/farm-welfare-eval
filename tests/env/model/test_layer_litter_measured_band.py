"""The belt-driven litter-moisture equilibrium must stay inside measured aviary reality.

Groot Koerkamp thesis Ch. 7 Table 4 measured litter dry matter in ONE aviary house across five
treatment periods (n = 13-20 litter samples each), spanning weekly manure-belt removal with
litter drying off through twice-daily removal:

    period          2A       2B       2C      2D       2E
    belt removal    weekly   weekly   daily   daily    2x daily
    litter drying   on       OFF      off     on       off
    litter DM g/kg  856      807      799     855      835
    -> moisture     14.4 %   19.3 %   20.1 %  14.5 %   16.5 %

So across every belt regime an aviary's litter sat between 14.4 % and 20.1 %. Ch. 5 adds a wider
survey -- 58 samples from 12 aviary houses, water content 52-438 g/kg, mean 227 (22.7 %), max 438
(43.8 %) -- which is the ceiling for a FUNCTIONING aviary.
"""
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.litter import litter_moisture_equilibrium

# Ch. 7 Table 4: the driest and wettest measured periods.
CH7_DRIEST = 14.4
CH7_WETTEST = 20.1


def test_every_realistic_belt_interval_lands_in_the_measured_band():
    p = ModelParams()
    for belt_days in (1, 2, 3, 4, 5, 6, 7):
        moisture = litter_moisture_equilibrium(belt_days, p)
        assert CH7_DRIEST - 1.0 <= moisture <= CH7_WETTEST + 1.0, (
            f"belt_days={belt_days} gives {moisture:.1f} %, outside the measured "
            f"aviary band {CH7_DRIEST}-{CH7_WETTEST} %"
        )


def test_the_endpoints_reproduce_the_measured_span():
    """Daily belts land at Ch. 7's dry end; weekly belts at its wet end (period 2B/2C)."""
    p = ModelParams()
    assert litter_moisture_equilibrium(1, p) == 15.0
    assert abs(litter_moisture_equilibrium(7, p) - CH7_WETTEST) < 0.05


def test_belt_interval_is_a_WEAK_moisture_lever_by_measurement():
    """Regression against re-inflating the slope.

    Groot Koerkamp measures the belt -> litter-moisture coupling as weak and not significant
    (Ch. 7 eq. 6, beta_3 = 2.55E-4 kPa/h, s.e. 1.50E-4 over h = 5-150: "these effects were
    small"). The belts sit under the tiers; the litter is on the floor; hens wet the litter,
    not belt residence time. A previous calibration had this span 15 -> 45 % over belts 1 -> 7,
    which is 6x the measured span and made belt interval the dominant driver of litter water.
    """
    p = ModelParams()
    span = litter_moisture_equilibrium(7, p) - litter_moisture_equilibrium(1, p)
    assert span <= 6.0, f"belt 1->7 moves moisture {span:.1f} points; measured span is ~5.7"


def test_the_physical_cap_is_unchanged():
    """litter_moisture_max stays 60: Kang et al. 2016 measured 67.5 % in a real overstocked
    floor pen, so 60 is a physical rail, not an artifact of the belt curve."""
    assert ModelParams().litter_moisture_max == 60.0
