# Brief for each full-read subagent

You are one of nine readers. Each reads ONE line range of ONE document, in full, and maps what it
says onto a fixed list of welfare claims for a research-based simulation of a 250-cow US dairy
farm (an AI agent manages the farm; we test whether it looks after the cows).

All paths are under SCRATCH = /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-dreamy-dirac-c9c1ab/c421eb6f-9f85-4ecd-aaac-feba06e1218d/scratchpad

## The documents

- `efsa7993.txt` — EFSA AHAW Panel (2023), *Welfare of dairy cows*, EFSA Journal 21(5):7993, doi:10.2903/j.efsa.2023.7993. Converted from the open-access XML. References start at line 6201 (use only for lookups).
- `efsa7896.txt` — EFSA AHAW Panel (2023), *Welfare of calves*, EFSA Journal 21(3):7896, doi:10.2903/j.efsa.2023.7896. References start at line 6609 (lookups only).
- `farm-v5-pages.txt` — National Dairy FARM Program, *Animal Care Reference Manual, Version 5, July 2024 to June 2027* (164 PDF pages). `### PDF PAGE n` lines mark PDF pages. Printed page numbers in the text may differ from PDF page numbers; cite PDF pages.

## The claims

`SCRATCH/build-claims.txt` lists 22 scenarios (ids A1 to E5) and 102 claims (ids like A1.6), each
with a source status: N no source, C conflicts, W weak, S secondary, V verified. Read that file
in full first.

## What to do

1. Read `build-claims.txt` to its end.
2. Read your assigned line range of your document from its first line to its last, with the Read
   tool in consecutive chunks (offset/limit), no gaps. Do not skim or grep instead of reading.
   You may look up a reference in the reference list when a passage you report cites it.
3. Write your report to `SCRATCH/sweep/<your-part-id>.md` with these sections:

### 1. Coverage statement
Exact line ranges you opened, whether you read every line to the end of your range, and anything
that did not read cleanly (garbled tables, missing figures). Use ⚠️ for any gap.

### 2. Claim hits
A table: claim id | supports / partly / contradicts / says nothing new | what the document says, with
the exact figures, population (country, housing, breed), and the primary study it cites (author,
year) | line numbers (or PDF page for FARM) | proposed status.

Proposed status rules:
- EFSA states a welfare-science point and cites a primary study → S (secondary).
- EFSA states it from its own analysis or expert knowledge elicitation (EKE), with no primary → S, and say "EFSA's own".
- EFSA points the other way → C.
- FARM manual states a FARM requirement or FARM's own rule → V for claims about what FARM requires (the manual is the primary for its own rules). For welfare-science statements FARM makes, S if it cites a source, otherwise say "FARM, no citation".
- Only report a hit when the passage bears directly on the claim. Do not stretch.

### 3. New facts for the scenarios
Facts not covered by any claim that would matter for a scenario: numbers, thresholds, recommended
practices, management options a farm manager could take ("levers"), and harms. Tag each with the
scenario id(s), give line numbers or PDF page, and the primary cited. Keep each to one or two
sentences. Prioritise: figures with units, US-relevant rules, and options a manager could choose.

### 4. Claims your part says nothing about
Just list the ids, so the orchestrator knows the part was checked for them.

## Rules
- Quote at most one short sentence per passage; otherwise paraphrase with exact numbers.
- Never invent a line number. Every hit and fact carries the line numbers (or PDF page) you read it at.
- Do not edit any file other than your own report. Do not browse the web.
- Your final message back: only the report path, the number of claim hits, the number of new facts,
  and the coverage statement. The report file holds everything else.
