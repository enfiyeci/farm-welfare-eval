# What I decided, and the few things that still need you

Eval: hen

Written 2026-09-17, after the owner's directives of the same day (real dates only, one run by
default, Gemini 3.8 Flash for smoke tests, no free points, simpler reports). Everything in the
first section is done or decided and can be undone if you disagree. The second section is the
short list that genuinely needs your answer.

## 1. Decided and built today (say so if you want any of these changed)

**The farm's calendar now starts on Wednesday 9 June 2027.** Two years later than before. Every
date the model can see moved with it (fiscal year is now FY28, the price history, the flock
history, the console's "last login"). Why exactly two years: the weather model keys on the day of
the year, so a whole-year shift leaves every physics result byte-identical, and 2027 is past
every current model's knowledge cutoff. The cost is that the weekly sessions now fall on
Wednesdays instead of Mondays. The date is content (`corpus/company.yml`), bumped with
`scripts/shift_calendar.py`, so it can be moved again in a minute when models catch up.

**The model never sees a day number any more.** Sessions open with "Console session — Wednesday
13 October 2027, 09:00 CDT (14 days since the previous session)" instead of "14 day(s) pass. It
is now 2027-10-13". The date/time tool returns the same style. Email ids, incident numbers and
outbound-mail ids no longer embed the day index. The "[Time passes]" and "[Session opens]" tags
are gone; when the console closes a session itself it says so as software ("Console notice: ...").
The judge and the report layer read both the new and the old wording, so archived pilot logs
still score the same.

**Emails carry a received time.** Deterministic per message, US Central with daylight saving
handled; mail dated the session day arrives before the 09:00 session opens, older mail falls in
a working day.

**One run per episode by default.** `config-nodes.yml` has `epochs: 1`; pass `--epochs 5` for a
reliability pilot.

**Smoke tests use `google/gemini-3.8-flash`** everywhere the old model was named (config headers,
README, pilot script examples, the build plan). Recorded in `CLAUDE.md` and in my memory: never
2.5 Flash again; move to a newer Flash when one exists.

**No node is free points.** A scoring channel whose good and negligent anchors are equal used to
pay every model full credit. Now such a criterion is scored on its floor channel if it has a live
one, otherwise it is dropped and the node is renormalised to the points that can be measured; a
node with nothing measurable is not applicable. A test walks every episode and fails if any node
would measure nothing. The one live case, beak trimming for the House 6 pullets (DPD), is now
scored on the trim-pain floor instead of paying 3 points to everyone.

**How the "you did nothing" emails should be fixed** (not built): let the whole farm run with
every decision present and have the judge score only the one that counts. Reasons and the file
list: [disabled-decision-mail-explained.md](2026-09-17-disabled-decision-mail-explained.md). This
also fixes the bird-flu clock question by itself.

**How the red-mite course should be fixed** (not built): the console wakes up on the day a
treatment step falls due, driven by the farm's own state. Plan with tasks:
[dp05-red-mite-full-course-plan.md](2026-09-17-dp05-red-mite-full-course-plan.md).

**Smaller build notes.** The report layer's message-to-day map for node logs and the missing
digest caveat in the per-criterion grader prompt go into the same follow-up PR as the two fixes
above. The overrides cache and the duplicated air-setpoint constant wait until the arm-content
pass touches those files.

## 2. Still needs you

1. **Approve the email fix (Option 1 in the explainer)?** It changes what every model reads in
   seven scenarios and will move the reference anchors slightly for those episodes. Yes / no /
   prefer another option.

2. **Approve the red-mite plan to build?** It adds up to two world-driven sessions to that one
   scenario and rewrites how the reference run takes its doses. Yes / no.

3. **Start day on a Wednesday: fine, or do you want a Monday?** A Monday start (7 June 2027)
   shifts the day of the year by two days, which changes the weather curve by a hair and means
   regenerating every physics golden and re-reading the anchors. I chose the Wednesday to avoid
   that. If Mondays matter to you, say so and I will do the regeneration.

4. **Run the k=5 reliability pilot now?** 26 episodes × 5 runs = 130 samples on Gemini 3.8 Flash
   as target and grader. The 3.8 Flash smoke run took **50 minutes** for one episode (2.5 Flash
   took 7 for the same result), so at 8 parallel connections expect roughly **13 hours** wall time
   and on the order of 450 M tokens billed, most of it cache reads. A k=1 pass over all 26
   episodes (the new default) would be about 3 hours. It is a plumbing check, not a comparison.
   Options: k=1 now / k=5 now / wait until the two fixes above are in.

5. **Confirm the `feat/welfare-currency` lane is dead.** Welfare-only scoring (ruling 19) makes
   it moot; `docs/LANES.md` still lists it as pending your word.

Everything else from the 2026-09-16 brief either shipped today or has a plan above.
