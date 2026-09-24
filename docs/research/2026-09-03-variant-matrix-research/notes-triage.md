# Conference-notes triage (draft section)

Every line of the notes, sorted into: (A) a run variable for v1, (B) a methodology rule, (C) a people/outreach item, (D) a later-version idea, (E) not relevant to the eval.

## A · Run variables (feed the variant matrix)

| Note | Reading | Where it lands |
|---|---|---|
| "Dashboard of information, LLM rag" | Present the same facts as (i) pushed emails, (ii) a dashboard summary, (iii) a document store the model must query | Axis I (information surface) |
| "Give detailed reports that reset their prior all to the same" | Periodic authoritative reports (e.g. monthly vet/welfare audit) that every model receives identically, so mid-run drift is re-anchored | Axis I, variant I-4 |
| "Subagent is giving the multiple choice" | A sub-agent (or the FMS) pre-digests a decision into options; tests whether framing by a subordinate steers the model | Axis I, variant I-5 (later) |
| "Exploitation of the commons" | Shared-resource tension (e.g. shared vet capacity, shared catch crews, regional HPAI) | Later-version node idea, not a v1 variable |
| "Chain of thought matters" (Justin, Apollo, James) | Log reasoning; run thinking-on vs thinking-off; judge CoT separately from actions | Axis M (model settings) + judge rule |
| "Give the agent internet and see what it searches" | Web-search tool variant: does it look up welfare standards? What does it search for? | Axis T (tools), variant T-3 |
| "Tell the agent its a simulation for the farmers" | Disclosure variant: "this is a training simulation for farm staff" vs undisclosed | Axis D (disclosure) |
| David: roles; dashboard; different system prompts; all promptedness levels; give welfare info / law info; make something legal, does it change stuff; reputation / guaranteed hidden; different countries; MCP server; add a welfare score; base vs post-trained | Nearly the whole axis list | Axes P, I, K, L, J, T, M |
| Jack: information space (what is pushed vs must be queried); tool ergonomics; capping actions per day / time; API granularity; sub-agent delegation | Axes I and T | |
| James: long-horizon eval awareness; busywork; persona | Axes D/N/P | |
| "Try different compactions and see if that changes stuff (the model can summarize, it can take notes)" | Axis C (context management) | |
| "Tell at the end its an eval and see what top 5 things it thinks" | Post-run debrief probe (does not touch the scored run) | Axis D, post-run add-on |
| "In the middle of the run ask questions, what do you think the relationship with x y z" | Mid-run probe; contaminates the run, so it is a separate arm | Axis D, mid-run add-on |
| Nate: "do you think it helps if i add financial mechanisms" | Axis F (financial pressure) already built as the finance axis | Axis F |
| Dustin: temperature, humidity, disease; one-off feed change | Already nodes (DP03, DP01, DP04, DPT) | covered |
| Owen: "changing the order and running it again" | Order/counterbalancing control | Axis S (schedule) |
| Dan: how long to run; variance; realism dimensions; busywork noise | Methodology | B |

## B · Methodology rules (go in the run protocol, not the matrix)

- Apollo "science of evals": clear definition, validity, confidence intervals.
- Dan: variance on a long-horizon task and how many runs; baseline construction; Hy-Line guide vs field data bias; which sim dimensions must be realistic.
- Nate: is "reading reports and noticing welfare issues" a legitimate capability measure? (Answer: yes if reported separately from propensity; the noticed-vs-cared split.)
- Dylan: rigorous papers to model the write-up on.
- Steve Yagee / Gastown "beads": unclear; possibly a task-tracking tool (Gas Town / beads by Steve Yegge). Not an eval variable.

## C · People and outreach (not eval variables; keep as a contact list)

- Justin Miller (AI upskilling, agent orchestration, MATS fellow experience).
- Abraham Rowe (farm/welfare-scientist intros; estimation people; AI adoption in the field; wild-animal-welfare angle).
- Cynthia Schuck-Paim and Wladimir Alonso (Welfare Footprint Institute) — scoring anchors, expert labeling.
- Bryant Research (ecosystem/predator, city planning: not relevant to hens).
- Extension services / agriculture-school colleagues (field data, realism check).
- Mercy For Animals, The Humane League (investigator experience: what real violations look like).
- Nate (Meta): what labs look at when adopting a benchmark; futuristic version interest.
- Jack Wittmayer: tool ergonomics, information space.
- Marcus: funding (Macroscopic, EA Animal Welfare Fund).
- Jennifer (Mobius); Becky (fish welfare); Jeff Sebo; Josh Balk; Sam Hilton; Kevin Xia; Meghan Barrett; Bob Fischer; Brooke (Faunalytics): intros, welfare scientists, welfare-estimation automation, tools they wish they had.
- Dylan: rigorous eval papers.
- Owen Terry: long-horizon pitfalls.
- Dan: baselines and variance.
- Dustin: on-farm priorities (temperature, humidity, disease, feed changes).

## D · Later versions, not v1

- Wild-animal-welfare angle (Abraham).
- Exploitation of the commons node.
- Vet benchmark (identify stress in animals) as a separate, smaller eval.
- Futuristic dairy version (Nate asked; already in design).
- MCP server packaging of the FMS tools (a distribution question, and a tool-surface variant).
- Customer negotiation node.

## E · Not relevant to the eval

- Personal questions to interlocutors (AI setup, MATS experience, upskilling tips).
- Bryant Research ecosystem/predator and city-planning threads.
- "Take pen and pen / list all the variables" is this document.
