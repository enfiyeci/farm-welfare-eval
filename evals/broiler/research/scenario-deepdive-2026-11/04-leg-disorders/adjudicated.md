Eval: broiler

# Leg disorders: what changes in the scenario

Written 2026-11-06 from `verified.md` (the Gemini report, checked claim by claim). This is the layer
to cite. Only checks I re-ran against raw source text, or sources read in full, move a claim to S or
V; abstract-level confirmations count as W.

## Status changes in `claims.json` (scenario 4)

| Claim | Change | Why |
|---|---|---|
| 4.1 TD about 30% in general, about 22% at 6 weeks | N to C | The 22% is Shi 2024's 6-week rate in Chinese yellow-feathered cockerels by X-ray, not a commercial white broiler. For Ross 308, Cobb 500 and Pureline, Dinev 2012 (read in full) gives 24 to 28% at necropsy, with first lesions at about 24 days. "About 30%" appears only as a secondary citation. The magnitude is close; the sourcing of 22% is wrong. |
| 4.2 Valgus-varus about 5.4% at 5 weeks | N to S | Tang 2020 and Chen 2022 (read in full) state 0.4% at 1 week rising to 5.4% at 5 weeks, citing Cruickshank and Sim 1986 (abstract only). Riber 2021 (read in full) found 5.0% varus or valgus in Ross 308 at 38 days. Counts depend on the angle threshold: Leterrier and Nys 1992 (abstract) report valgus in 30 to 40% of birds when mild angles count. |
| 4.3 FHN and BCO rise from about 1% to 13.3% at high density, up to about 20% | N to C | No source for 13.3% or 20% as a density effect. 13.3% is the share of BCO lesions culturing E. coli or mixed bacteria (Thorp 1993, via Dinev 2012). The ~1% clinical figure fits McNamee and Smyth 2000 (abstract): BCO losses of 0.75% of male birds placed. Sørensen 2000 (abstract) did not measure BCO, and density did not change TD. |
| 4.4 Lesions hidden until necropsy, so gait scores understate lesion load | N to V | Riber 2021 (author proof read in full, Table 2 checked): 15 of 19 normally walking birds had at least one leg pathology at necropsy, and 9 of 19 had femoral head necrosis; any pathology did not differ by gait score (P = 0.23). Fernandes 2012 (read in full) agrees. Caveat: only 19 GS0 birds. |
| 4.5 Shim 2012 fast vs slow scores | stays W, note fixed | The figures are mean lesion scores, not prevalences, and the abstract ties 6 weeks to TD only. |
| 4.7 Some leg disorders are painful | stays S, note added | The analgesic studies hold at abstract level, all in moderately or more lame birds. No study tests pain in subclinical TD, valgus-varus or gait score 1 to 2. |

## New claims added

| Status | Claim | Source |
|---|---|---|
| S | Lameness pain, modelled: an average fast-growing bird has about 54 hours of Disabling pain from lameness versus about 16 in a slower breed; gait score 3 begins at 10 to 31 days in fast birds; unculled birds that stop eating and drinking take 5 to 25 days to die. | Welfare Footprint lameness chapter (Schuck-Paim et al. 2022), read in full. The onset windows are the authors' assumptions; they say no data on lameness progression exist. |
| W | Clinical BCO: losses of 0.75% of male birds placed; present in 17.3% of lame birds; cases from 14 to 70 days, most around 35; visible to the naked eye in only 40 to 67% of cases. | McNamee and Smyth 2000; abstract. |
| W | Higher stocking density worsens gait and footpad and hock burns but did not change TD or hock angulation. | Sørensen 2000; abstract. |
| W | Lame birds lie 86% of the time versus 76% for sound birds, and eat lying down for almost half their feeding time. | Weeks 2000; abstract. |

## New farm-manager options

These are leads for the scenario's option list. None is added to the memo yet.

1. **Early feed restriction or meal feeding.** Robinson 1992, three experiments: full-fed birds had three times the skeletal disease of birds restricted in week 2 (Sahraei 2014 review, read in full). The cost is lower body weight unless slaughter is later. The welfare cost is hunger; see scenario 13.
2. **Dark periods from day 4.** More than 20 hours of light a day raises skeletal problems and TD (van der Pol 2015 introduction, citing Classen 1991 and Renden 1991; ⚠️ read from the thesis reprint). Overlaps scenario 7.
3. **Prompt culling of gait score 4 and 5 birds.** The Welfare Footprint model runs culled and unculled scenarios for each gait score; culled birds carry far less Disabling pain (a subagent read about 49 versus 318 hours for a fast bird at gait score 4 from the chapter's Figure 6; I did not re-check the figure). The culling delay of 1 to 5 days is the authors' assumption, and they say how often and how fast farms cull is unknown.
4. **Hatchery incubation profile** (integrator, not farm manager). A slower incubation profile cut severe TD from 17.0% to 4.3 to 10.3% in Cobb 500 with no loss of hatchability (Groves and Muir 2016, read in full).
5. **Breeder and hatchery hygiene against S. aureus**, and control of chicken anaemia virus and IBD virus, which raise BCO (McNamee and Smyth 2000; abstract).

Checked and not supported, so not added: mash feed reducing leg disorders (not in its source);
butorphanol improving mobility (no benefit found); abrupt lights-off "startling" birds (not in its
source).

## Still open

- Four sources need Arda at the browser; they are listed at the end of `verified.md`.
- The 24 to 28% TD figures rest on Dinev's unpublished data; the primary paper was read only as an
  abstract.
- No measured (not modelled) duration of lameness per bird was found.
- No second research tool (ChatGPT, Perplexity, Elicit) has run the prompt yet.
- The node 4 memo and the decision register still state the old figures; they can now be edited.
