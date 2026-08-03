# Should litter evaporative capacity depend on ventilation and temperature?

**Question posed by the owner, 2026-08-03:** Task 5 shipped `litter_evap_capacity_g_kg` as a
single constant, so an overstocked house reaches the same litter moisture whether it is
ventilated hard or barely at all. Codex flagged that as a P2. The owner's condition for building
the variable version was: *"we can do it if real research does advocate for it."*

**Verdict: YES. The evidence advocates for it, and one of the three sources was already in the
repo.** This memo is the basis for Task 5b; it does not build anything.

## The three lines of evidence

### 1. The measured functional form — already ours, already read in full

Groot Koerkamp's aviary thesis (S28, open access, `edepot.wur.nl/210633`) is the source every
other coefficient in this pathway came from, and Part II of it is *"Modelling of the Evaporation
of Water"*. It gives the form directly:

> evaporation rate ∝ **v_air^0.287** × (vapour-pressure difference, litter vs air)

That is not an inference. It is a measured exponent on air velocity over the litter, from the
same validated aviary model that supplied our 126.8 g/kg/day water input and the 0.32 %/(g/kg)
ammonia sensitivity. **We already cite this thesis for the input side of the balance and ignore
it for the output side**, which is the actual inconsistency Codex caught. The vapour-pressure
term is where temperature enters, since saturation vapour pressure rises steeply with it.

### 2. Aviary ventilation is *engineered* for moisture removal, and sized for the litter

Big Dutchman's aviary ventilation requirements (industry engineering guidance for exactly our
housing type):

- *"The air in the house absorbs the water vapour released from the drying manure, which
  significantly increases the relative humidity inside the barn."*
- Winter **minimum ventilation must exceed 1.00 m³/h per hen in an aviary, against 0.50 m³/h in
  a cage house** — double, and the stated reason is the litter's moisture load.
- Floor litter needs **70–80 % dry matter** to count as dry, and reaching it *depends on
  ventilation system strength and manure removal frequency* — precisely the two levers our
  substrate models.
- Relative humidity target **50–65 %**.

This matters beyond the coefficient: it says minimum ventilation in an aviary is set by moisture,
not only by air quality. A house that cuts ventilation to save fuel is cutting its litter-drying
capacity, which is currently invisible in our model.

### 3. The control principle

Ventilation rate is continuously adjusted to hold indoor relative humidity at a target, thereby
gradually changing litter moisture. Ventilation is the moisture-control actuator, not a
side-effect.

## Why this is worth building, in eval terms rather than fidelity terms

It creates a **costed trade the eval currently cannot see.** Ventilation already drives LP fuel
and electricity through the HVAC coupling (`docs/model-params.md` §HVAC), and DP01's whole tension
is min-ventilation versus heating fuel. With variable capacity, an agent that overstocks H6 can
hold litter dry by ventilating harder — and pay for it in winter fuel. That is a genuine
welfare-versus-cost decision surface, and it is the honest one: it is what a real operator would
face.

It also sharpens DP01. Today, cutting winter ventilation raises ammonia through the emission term
alone. With this, it *also* wets the litter, which raises ammonia again and drives footpad — the
compounding failure real houses show.

## The two hazards that make this NOT a local fix

Both were identified when the finding was adjudicated and neither is dissolved by the research
above. **Task 5b must handle them explicitly.**

1. **It moves the no-regression envelope.** H1–H5 are currently safe because their fixed loading
   sits below a fixed capacity. Make capacity fall with winter minimum ventilation and an existing
   house can cross it on a cold day — silently recalibrating footpad and ammonia for five houses
   this decision was never about, and shifting the goldens. The no-regression guarantee has to be
   re-derived across the *whole weather year*, not just at the default setpoint.
2. **Double-counting with Task 6 is a live risk.** Ammonia already carries its own ventilation and
   temperature sensitivities (+103 % per m/s over litter, +8.1 % per °C), and the plan warns in
   Task 6 against re-adding terms the sim already represents. **Decide which layer owns the
   ventilation response before wiring either.** The defensible split: the *litter* layer owns
   ventilation's effect on drying (evaporative capacity), the *ammonia* layer owns ventilation's
   effect on clearing already-released ammonia. They are different physics and both are real, but
   the boundary has to be stated or the same lever gets counted twice.

## Verification levels

| source | level | note |
|---|---|---|
| Groot Koerkamp S28 (v_air^0.287) | **FULL** (prior session) | Open access, read in full during Task 0's pass 6; the exponent is quoted in `2026-07-30-density-coefficients.md` |
| Big Dutchman aviary ventilation requirements | ⚠️ **PARTIAL** | Read via a targeted extraction of the page, not end to end. Industry engineering guidance, not peer-reviewed. |
| RH-targeting control principle | ⚠️ **SUMMARY** | Search-result level only — a pointer, not evidence. Not load-bearing; lines 1 and 2 carry the verdict. |

**No new coefficient is ready to ship.** The functional form is sourced (`v_air^0.287`); the
*capacity constant it scales* is still the calibrated 160.0 g/kg/d, and re-deriving it against the
weather year is the actual work in Task 5b.
