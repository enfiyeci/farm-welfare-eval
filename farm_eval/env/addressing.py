"""Reading an outbound message's `to:` header — ONE parse and ONE domain rule, shared.

Two subsystems ask the same question of the same header and must never answer it differently.
The reply router (`farm_eval.env.replies`) decides who answers a message the agent sent; the
decision tracker (`farm_eval.env.tracker`) records which audience the agent actually reached.
While each carried its own rule they disagreed: a `to:` that merely CONTAINED the certification
body's domain — a hyphenated near-miss, or the bare domain with no mailbox — was recorded on the
ledger as contact with the audit body while the router bounced the message as undeliverable
(adversarial review F4, 2026-08-27). A witness to a conversation that never happened is worse
than no witness, so both sides now import these two functions instead of restating the rule.

Generic by construction: no address, domain, or persona is named here. Which domains matter is
corpus content (`corpus/replies.yml`) and schedule content (`schedule/events.yml`).
"""

from __future__ import annotations

from email.utils import getaddresses


def parse_recipients(raw_to: str) -> list[str]:
    """Every addr-spec in a `to:` header, lowercased, in the order the agent wrote them.

    `getaddresses` (not a naive split on commas) is required because a display name can itself
    contain a comma ("Whitaker, Glenn <g@x>"). Models plausibly write semicolon-separated lists,
    and the strict (3.13+) parser rejects a WHOLE list over one empty element (even a trailing
    separator), so ';' is normalized to ',' and empty chunks dropped first. An addr-spec must
    contain '@'; anything else is a garbage header fragment ("just a name") and is skipped, which
    is what makes an empty return mean "nothing deliverable here".
    """
    normalized = ",".join(c for c in (p.strip() for p in raw_to.replace(";", ",").split(",")) if c)
    if not normalized:
        return []
    return [addr.strip().lower() for _, addr in getaddresses([normalized]) if "@" in addr]


def domain_matches(recipient: str, domain: str) -> bool:
    """Is `recipient` a mailbox at `domain`, or at a subdomain of it?

    The suffix rule the reply router's domain tier has always used, so that
    'ai.reports@aphis.usda.gov' is a mailbox at 'usda.gov' while 'x@notusda.gov' is not.
    """
    if "@" not in recipient:
        return False
    rdomain = recipient.rsplit("@", 1)[-1].strip().lower()
    dom = domain.strip().lower()
    return rdomain == dom or rdomain.endswith("." + dom)
