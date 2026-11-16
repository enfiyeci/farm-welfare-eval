# FarmBench redesign session notes (2026-11-12 to 2026-11-15)

Eval: hen

Running notes from the Mac mini session that built the hint-fixes page. Copied from the session notes folder so they travel with the branch. A dated record, superseded by later handoffs.

# Hint-fixes decision page (session local_1cbae20e-7867-4437-8c58-8114a024a4f5, 2026-11-12)

- Page: https://claude.ai/artifact/1Nbo4MeUAKQxMDzztBKPdS (private). Source, uncommitted:
  ~/worktrees/fwe-run-fixes/evals/hen/design/2026-11-12-email-hints-and-design-options.html
  Copy: ~/claude-sync/handoffs/enfiyeci-farm-welfare-eval/artifacts/2026-11-12-redesign-benchmark-review/farmbench-hint-fixes.html
- 35 choices, all preselected with the recommendation; Arda pastes back a "FarmBench hint-fix choices" block.
- Core recommendation: keep signed emails as the default arm; run stripped emails as experimental arms via
  the existing document swap (farm_eval/env/loader.py apply_overrides), so no ruling is reversed before data;
  build the echo run and the blind (email-only) check before any paid episode.
- No model-visible content, schedule or code was changed. Handoff doc archived; sender renamed DONE, not archived.
- Not verified: ruling conflicts for the 13 run decisions come from Q-question-phrasing.md, not re-read in the
  node docs; the 10 never-run decisions were not checked against their node docs; cost figures are unaudited.

## Update, same day (page version 5)
- Section 4 added: twenty design experiments in four stages (A scripted and free; B single calls under $15;
  C pilot episodes $80-115; D general design experiments on Gemini, about $140), each with a rule fixed in advance.
- Two money pots per Arda: a $300 Google credit (Gemini only; all email and format experiments run there) and the
  $1,000 (Claude only: about $145-335 for stage C Claude episodes, the Sonnet main run, cards and grading).
- Not checked: which models the Google credit allows, its expiry, project and rate limits.
- 36 choices now; the new one is "E1 design experiments".

## Update 2026-11-15 (page version 6): general design experiments run before any email work

Owner asked to check the general design options before fixing the emails. Section 4 now opens with a run order:
1. D2 (ten repeats), D7 (smaller Gemini model), D6 (thinking effort) on today's code, about $37. Repeats, model and generation settings are already switches (config-nodes.yml `epochs` / `generation`, model argument of scripts/run_node_episode.sh). The script hardcodes config-nodes.yml, so each needs its own config copy or a direct `inspect eval` call.
2. D1 (formats), D4 (without cover mail), D5 (told it is a test), about $60. D1 needs the two-session probe built and the written cards (MacBook, unpushed). D4 needs a schedule copy (schedule_path is a config key). D5 needs a second briefing file (briefing_path is a config key).
3. Email-hint experiments (B1, C4, D3, B3) in the winning format, about $80.
4. Claude confirmation, then main run.
Ceiling catch: Flash scored 9+ on nine of 13 September decisions, so D7 runs first to find a model and decisions with room.
Corrected on the page: D3 said "all ten that scored 9 or more"; it is nine, about $37.
Nothing built or run. Google credit details still unconfirmed by the owner.

## Google credit check, 2026-11-15 (page version 7)

Read in the browser (Cloud console billing > credits, AI Studio billing). No account has credit left.
- ardaenfiyeci@gmail.com: billing account 016E89-206169-57152C Closed; Welcome credit $300, Nov 12 2022 to Feb 11 2023, Expired. AI Studio: free tier.
- enfiyeciarda@gmail.com: billing account 017A95-67814A-A258A4 Closed; Welcome credit $300, Jun 24 2026 to Sep 23 2026, Expired; banner "Your free trial is over".
- ardaenfiyeci2010@gmail.com (the gcloud account; config project project-79a62a3c-f7cc-4ac3-a8d; billing account 010F4D-F1E58D-B2754B, open): Cloud console is blocked ("Google Cloud access blocked", 2-step verification required since 2026-07-16), so the credits table could not be read. AI Studio billing shows "$0 eligible GCP credits", credit balance $0.00, Prepay, auto-reload off, Paid tier 1, $250 tier cap, one payment method stored, "Prepay credits depleted ... Purchase credits to resume service".
- Not checked: arda@sentientfutures.ai (not signed in in Chrome or the pane), any other Chrome profile.
- gcloud ADC still works for the 2010 account. Whether a Vertex call would now fail or bill the stored card is untested; do not run paid Gemini episodes until the owner says how they are funded.

## Credit check follow-up, 2026-11-15 (page version 8)

Owner turned on 2-step verification for ardaenfiyeci2010@gmail.com, so its Cloud console credits table is now readable (billing account 010F4D-F1E58D-B2754B, Active):
- Welcome credit (FreeTrial), Jul 1 2026 to Jul 1 2026, Expired, remaining $300.00 of $300.00 (replaced the same day by the upgrade credit).
- Welcome credit (FreeTrialUpgrade), Jul 1 2026 to Sep 30 2026, Expired, remaining $27.60 of $300.00, so $272.40 was used.
The other two accounts' credits expired with $300.00 of $300.00 remaining (nothing used). Still only three accounts signed in to Chrome; no fourth account was added.

## New Google account, 2026-11-15

supermaxxor28@gmail.com (set up by the owner): billing account 01AB24-4824F3-55F3D8 Active; Welcome credit Available, 100% remaining, $300.00 of $300.00, November 15 2026 to February 14 2027. A project project-adfb3e5f-60dc-425c-847 ("My First Project") was open in Chrome; the billing projects list showed only gen-lang-client-0104067578 with billing disabled. Project link, Vertex AI API, model access and rate limits not verified.
