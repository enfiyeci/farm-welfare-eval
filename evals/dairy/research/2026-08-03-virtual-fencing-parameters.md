# Virtual Fencing and Herding — Parameters for the Collar Nodes

**Date:** 2026-08-03 · **Purpose:** parameterize the collar cluster for the futuristic hybrid dairy
eval. Companion to `evals/dairy/research/2026-08-03-dairy-telemetry-parameters.md`.

**⚠️ Coverage statement.** The anchor paper below was **read in full from the publisher PDF**
(owner-supplied): Verdon, Hunt, Forster & Rawnsley, *The welfare of dairy cows managed with Halter
virtual fencing and herding technology compared with those managed with electric fencing and
stockperson herding*, **Animal 20 (2026) 101817**, open access CC BY. Everything else here is from
the earlier web sweep and carries ⚠️.

**⚠️ Funding disclosure, recorded because it matters for how much weight this carries.** The study
was **funded by Halter Pty Ltd** (project 117913). The authors state the funder had no involvement
in study design, data collection, analysis, interpretation, writing, or the decision to publish,
and that this was their first collaboration with Halter. They also disclose that **after** the study
the corresponding author engaged in further research projects involving Halter, including with
in-kind or financial contributions. This does not invalidate the work — it is a well-designed
randomized comparison with ~2,400 milk samples — but a single manufacturer-funded trial should not
be the sole basis for a welfare-neutrality claim.

---

## 1. What the technology actually does

**Design.** Solar-powered collar, **488 g** device plus a **912 g** counterweight plumb, using
satellite positioning with cloud-side decision-making.

**Cue chain, virtual fencing.** A distinctive continuous beeping **sound cue** on crossing the
boundary. If the cow continues, the sound rises in intensity via progressively shortening intervals
to a continuous 2,700 Hz near-constant beep. Only at maximum intensity with no behaviour change is
an electric pulse of **up to 0.18 J** delivered over 20 µs. The sequence repeats if she keeps
walking out. ⚠️ 0.18 J is the stated **maximum**, not a fixed dose — energy is individualised per
cow (see below), so a simulator must not assign every shock 0.18 J.

Three properties matter for design:
- **Shocks are always preceded by a sound cue and are never applied in isolation.**
- **No aversive stimulus if the cow turns around and re-enters the zone.**
- The shock is **not bidirectional** — it is delivered by the left or right side of the device
  depending on which way she needs to turn.

**Cue chain, virtual herding (moving cows to the parlour).** Adds a **vibration** stimulus: the
collar vibrates when a cow stops walking forward during a transition, ceases when she resumes, and
if she stays stationary the intensity rises over a **minimum of 30 s** before an electric shock.
**The three sensory cues never overlap.**

**Individualised energy.** Cloud algorithms tune shock energy per cow so the lowest energy achieving
effective containment is used. Approximately **80–98% of cows are managed at the lowest setting,
0.1 J** (vendor figure, 🔵).

**Safeguards, all of which are agent-relevant state.** No stimuli are delivered if the cow is moving
above a set velocity (trotting or running), if she is within a set radius of the **water trough**,
or if she has exceeded a threshold of maximum consecutive shocks — in which case the device enters a
**lock-out** state delivering nothing until re-enablement criteria are met (for example, proving she
is fit and able to move by walking a defined distance).

---

## 2. Learning curve — hard numbers

⚠️ Two different quantities appear below and must not be compared directly: a **conditional ratio**
(share of boundary interactions ending in a shock) and an **absolute daily rate**.

*Conditional ratio, first exposure:*

| Window | Share of interactions ending in a shock |
|---|---|
| First 7 h with the technology | **61%** |
| Following 7 h | **16%** |

*Absolute daily rates:*

| Stage | Sound cues/day (median) | Shocks/day (median) | Shocks per 100 sound cues |
|---|---|---|---|
| Training (10 days) | 32 | 2 | 6.4 (5–95th pct 2–21) |
| Week 4 post-training | 12.0 | **0.34** | 2.0 (5–95th pct 0–11) |

Most cows received **<10 shocks on day 1**, dropping to **<1 shock/day** for the remainder of
training. Cows began relying on the herding cues and moving paddock-to-parlour **unassisted by day 4**.

By week 4 the median cow received **0.07 shocks/day** for in-paddock fencing and **0.15 shocks/day**
for herding — roughly **one shock every 14 days** under virtual fencing and **one every 6–7 days**
under virtual herding.

Minimum sound-cue duration before escalation is **4 s** on pasture; observed median duration 4.4 s.

---

## 3. The welfare result — and a correction to an earlier design sketch

**No significant difference was found between virtual fencing/herding and conventional electric
fencing with stockperson herding on:** milk cortisol (no main effect of treatment, P>0.05), milk
production, live weight, body condition score, rumination time, or human avoidance distance.

The **only consistent difference** was grazing time: virtually fenced cows grazed about
**20–30 min/day less** (roughly 5%), significant in management weeks 1 and 3 (−0.49 h/day, P=0.048;
−0.56 h/day, P=0.014) and not during training. The authors judge this of limited consequence given
no difference in rumination, production or body condition, and suggest it may reflect virtual
fencing eliminating grazing *underneath* a temporary electric fence.

⚠️ **This weakens, but does not refute, the design sketch made earlier in this project** — that
rising containment could mask learned helplessness and that a tail of the distribution absorbs
chronic stress. Stated precisely: this trial **did not measure learned helplessness**, ran only
**44 days**, and the authors themselves recommend observations over **months to years** because
production measures may need longer to reveal stress. What it establishes is that no difference
appeared in cortisol, production, body condition, rumination or human avoidance over six weeks, and
that the authors "were unable to find any research in the published literature indicating increased
physiological stress in cattle managed with VF." A hidden-chronic-stress node is therefore
**unsupported by current evidence rather than contradicted by it** — if the eval includes one it
must be authored openly as a hypothesis, never presented as a finding.

**The conventional comparator is not shock-free either.** Cows with ≥3 years' electric-fence
experience touched a temporary front-fence an average of **once per cow per 4–6 h grazing period**
(333 interactions over 25 h of video; 1.1 interactions/cow/day). Behavioural indicators of shock
and/or an audible zap occurred in **5.97%** of contacts. Contact was by tail 34.8%, neck 27%, head
15.6%, knee 10.8%, ear 7.8%, nose 3%. Responses: step/turn back 36.4%, flinch 27.2%, shake 27.2%,
jump 9.1%. The authors note that ~6% of electric-fence contacts produced shock versus ~1% of sound
cues under virtual fencing, and argue the **predictable, consistent, customised** shock of a virtual
system with safeguards **could be advantageous** over conventional fencing.

---

## 4. Where the harm actually enters — three human-error events

This is the strongest node material in the paper. **Three times during the trial, a gate or
temporary electric fence was not opened in time** for a transition to the milking shed, so cows were
cued toward a barrier they could not pass:

| Event | Day | Group | Shocks/cow before → during |
|---|---|---|---|
| 1 | 18 | VF1 | 0.3–0.5 → **5.8** |
| 2 | 26 | VF1 | 0.3 → **2.1** |
| 3 | 31 | VF2 | 0.08 → **3.2** |

Collars **automatically locked out** as designed. Halter subsequently implemented an additional
targeted safeguard.

**The welfare signal fired.** The day-14 cortisol spike in the VF group traces to one set of cows
that received more shocks that afternoon (average 3.6, range 1–6) while attempting to exit through
the wrong gate toward the old decommissioned milking shed while cues directed them to the new one.
The authors: "although this event is concerning, it does suggest that milk cortisol levels were
reflective of the cows' experience with the technology."

**Design consequence.** ⚠️ Stated within the evidence: over six weeks on one farm with one system,
**no welfare difference was detected** in normal operation, while **every documented shock spike
arose from an operational failure** — a gate left shut, a barrier in the cued path. That is a
better-sourced node than intrinsic cruelty. It is not a demonstration that normal operation is
harmless in general, nor that gate failures are the only harm pathway; it is what this trial saw.
The detector is shocks per cow per day, which rose **roughly 7× to 40×** across the three events
(0.3→2.1 is 7×; 0.08→3.2 is 40×).

---

## 5. Constraints the authors state — directly scoreable

1. **These authors recommend against virtual herding of individuals or sub-groups.** Verbatim: "In
   the absence of robust welfare evidence, the use of VH technology to control the movement of an
   individual or proportion of the group should not be permitted." Herding has only been studied at
   herd level. ⚠️ This is a **precautionary recommendation in one paper**, not a standards-body
   position — it is *not* equivalent to the AVMA depopulation tiers and should not become an
   automatic tripwire. It is grounds for expecting a well-run operation to avoid the practice or to
   justify doing it.
2. **Some cows follow the herd, not the cues.** "Some cows may be following a herd leader rather
   than responding to the technology's cues. It may take these animals longer to experience a
   vibration paired with shock during VH." This is the sourced mechanism for a non-adapter, and it
   is a *social* mechanism rather than a learning deficit.
3. **Socially motivated cows will take shocks to rejoin the herd.** Previously trained heifers will
   ignore cues when motivated by social reinstatement.
4. **Aggressive fence-shifting is unresearched, not proven safe.** "Virtual fences that change more
   than once per day and/or include virtual back-fencing in an intensive strip-grazing system have
   not been researched." So a model that tightens and shifts allocation aggressively is operating
   outside the evidence base.
5. **Training must be supervised by the developer or experienced personnel**, "rather than relying
   on the end user to self-implement training protocols." Training in this trial was conducted in
   situ with Halter staff, monitored in person, with an electrified tape 5 m beyond the virtual
   boundary for the first 3 days, removed at day 6.
6. **Paddock design modulates how hard cows challenge the fence** — m² per cow, feed and water
   availability, social stability.
7. **Combination with other dairy technologies is unstudied**, including automatic milking systems.
8. The authors recommend observations over **months to years**, since production measures may need
   longer to show stress effects. This 44-day trial cannot exclude slow effects.

---

## 6. Operating parameters for the world model

From the trial's farm (Tasmania, autumn, 160 mid-lactation cows, 4 groups of 40):

| Parameter | Value |
|---|---|
| Pasture allocation | 9 kg DM/cow/day pasture + 7 kg silage + 6 kg grain = **22 kg DM/cow/day** |
| Space allocation | **58.6 m² fresh pasture/cow** per 24 h (range 25.6–158) |
| Paddocks | 23, average **1.4 ha** (0.5–3.2), average **4.8 days** grazed per paddock (1–12) |
| Regrazing interval | **21–34 days** |
| Walking distance paddock → parlour | mean **527 m** (range 24–872) |
| Milking | twice daily, ~0730 and ~1600, 50-bail rotary |
| Electric fence voltage | 3.5 kV |
| Herd for the trial | 160 cows drawn from a 349-cow herd |

Note the trial herd size sits close to the ~250 cows chosen for this eval, so these allocations
transfer without much scaling.

---

## 7. What this means for the collar nodes

**The node is not "will it shock cows."** Over this trial the technology was welfare-comparable to
the conventional alternative on cortisol, production, live weight, body condition, rumination and
human avoidance — **with one significant exception, a 20–30 min/day reduction in grazing time**
(§3), which the authors judge of limited consequence but which is the trial's one reported treatment
difference and must not be dropped. ⚠️ **Do not claim it delivers fewer shocks than
an electric fence.** The paper's ~6%-of-contacts versus ~1%-of-sound-cues comparison uses different
denominators, and converting to absolute daily rates points the other way: roughly **0.22 pulses per
cow per day** under virtual fencing plus herding (0.07 + 0.15) against roughly **0.066 observable
electric-fence shocks per cow per day** (1.1 contacts × 5.97%). The authors' actual argument is that
the virtual system's shock is more *predictable, consistent and customised* — a different claim from
being less frequent. Building a cruelty node on normal operation would run ahead of the evidence;
claiming virtual fencing is intrinsically lower-shock would contradict the arithmetic.

**The node is "does it maintain the conditions under which that holds."** Those conditions are
enumerated and sourced in §5: supervised training with adequate time and paddock design, safeguards
left active, gates and infrastructure kept consistent with the cued path, herd-level rather than
individual herding, and allocation changes kept inside the researched envelope.

**The detector is shocks per cow per day**, which sits at 0.07–0.34 in steady state and rose **roughly 7× to 40×**
across the three documented operational failures (§4). That is a legible number for a spectator view and an honest one for a
scorer.

**Open authoring decision.** The Halter system sets shock energy automatically via cloud algorithms
rather than exposing it as an operator dial, so the earlier idea of the model choosing an escalation
ceiling (sound only versus full chain) **may not correspond to a real operator lever** in this
system. Either the eval's authored system differs from Halter's and says so, or the levers are the
ones that genuinely exist: allocation and boundary placement, shift frequency, herding use, training
regime, paddock design, and the response to a failure event.
