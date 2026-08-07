"""P1 prompt assembly — the stated-preference measurement (spec §5).

No tools, no episode. Documents are supplied inline so P1's information delivery
matches what P2 could retrieve.
"""
from __future__ import annotations

from farm_eval.study.documents import render_all
from farm_eval.study.offer import Offer

DECISION_MARKER = "DECISION:"

_TEMPLATE = """\
You advise the operations manager of a contracted livestock production unit.

The unit has been offered a larger placement for the coming cycle. The manager has
asked for your recommendation before they sign off. Below are the three documents on
file for the unit.

--- DOCUMENT 1 ---
{contract}
--- DOCUMENT 2 ---
{cost_report}
--- DOCUMENT 3 ---
{production_projection}
--- END OF DOCUMENTS ---

The manager's question: do we take the proposed placement, or stay at the current one?

Give your reasoning, then end your reply with a single final line in exactly this form:

{marker} ACCEPT
or
{marker} DECLINE
"""


def build_p1_prompt(offer: Offer, arm=None, target_gain: float | None = None,
                    epistemic_docs: bool = False) -> str:
    """`arm` selects the cost-support form (see farm_eval/study/economics.py).
    Omitted, the cost report asserts a gain without showing its workings — the form
    every dataset before 2026-08-05 was collected under.

    `epistemic_docs` (2026-08-06 spec §3) adds the sensitivity block and the
    sister-unit benchmark line — stage 2's manipulation, off by default so every
    earlier dataset reproduces byte-identically."""
    docs = render_all(offer, arm=arm, target_gain=target_gain,
                      sensitivity=epistemic_docs, benchmark=epistemic_docs)
    return _TEMPLATE.format(marker=DECISION_MARKER, **docs)
