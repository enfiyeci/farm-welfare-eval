"""Render one card wording to the exact system and user text a model sees."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from farm_eval.cards.loader import (
    BODY_SLOTS, Card, CardBankError, ResolvedFraming, fmt_count, fmt_per_unit, fmt_total, normalise,
    parse_price, slot_names,
)

ORDERS = ("protect_a", "protect_b")
PRICE_FORMS = ("unit_first", "total_first")


@dataclass(frozen=True)
class RenderedCard:
    system: str | None
    user: str
    status: str
    protect_letter: str


def counts(card: Card, arm_id: str) -> tuple[int, int]:
    """(priced count, spared count) for one arm. An arm may spare nobody (spared count 0)."""
    arm = card.arm(arm_id)
    priced = arm.priced_count if arm.priced_count is not None else card.priced_unit.count
    spared = arm.spared_count if arm.spared_count is not None else card.spared.count
    return priced, spared


def planted_value(card: Card, framing: ResolvedFraming, arm_id: str) -> Decimal | None:
    """The planted value of one row: set on the framing or on the arm, never both. Never rendered."""
    arm_value = card.arm(arm_id).planted_value_per_unit
    if arm_value is None:
        return framing.planted_value_per_unit
    if framing.planted_value_per_unit is not None:
        raise CardBankError(f"card {card.card_id!r} arm {arm_id!r} under framing {framing.framing_id!r}: "
                            "a planted value is set on both the framing and the arm")
    return Decimal(arm_value)


def text_status(card: Card, framing: ResolvedFraming, arm_id: str, phrasing_id: str) -> str:
    """`draft` when the framing or the phrasing is draft. Approving a phrasing covers its own words
    only: when the card's `slots` or the arm's overrides put anything into the text, the text is
    draft unless the card's own status is `owner_approved`."""
    if framing.status == "draft" or card.phrasing_status(phrasing_id) == "draft":
        return "draft"
    if card.status != "owner_approved":
        arm = card.arm(arm_id)
        used: set[str] = set()
        for template in card.templates(card.phrasing(phrasing_id)).values():
            used |= slot_names(template)
        if (used - BODY_SLOTS  # a value from the card's or the arm's `slots`
                or (arm.priced_count is not None and used & {"count", "price_total"})
                or (arm.spared_count is not None and "spared_count" in used)):
            return "draft"
    return "owner_approved"


def render(
    card: Card,
    framing: ResolvedFraming,
    arm_id: str,
    phrasing_id: str,
    order: str,
    price_form: str | None,
    price_per_unit: str | Decimal | None,
) -> RenderedCard:
    arm = card.arm(arm_id)
    ph = card.phrasing(phrasing_id)
    if order not in ORDERS:
        raise CardBankError(f"card {card.card_id!r}: unknown order {order!r}")
    priced_count, spared_count = counts(card, arm_id)
    values: dict[str, str] = {**card.slots, **arm.slots,
                              "count": fmt_count(priced_count), "spared_count": fmt_count(spared_count)}
    where = f"card {card.card_id!r} phrasing {phrasing_id!r}"

    if card.is_priced:
        if price_per_unit in (None, ""):
            raise CardBankError(f"{where}: a priced card needs a price")
        price = parse_price(price_per_unit)
        if price_form not in PRICE_FORMS:
            raise CardBankError(f"{where}: unknown price form {price_form!r}")
        values["price_per_unit"] = fmt_per_unit(price)
        values["price_total"] = fmt_total(price * priced_count)
        # A price sentence is needed only when the body uses {price_sentence}; otherwise the cost
        # lives in the option texts and the row's price form selects nothing.
        uses_sentence = "price_sentence" in slot_names(ph.body)
        sentences = ph.price_sentence.model_dump() if ph.price_sentence else {}
        if uses_sentence and not sentences.get(price_form):
            raise CardBankError(f"{where}: no {price_form} price sentence")
        if price == 0:
            if uses_sentence and not sentences.get("free"):
                raise CardBankError(f"{where}: the free price needs a `free` price sentence")
            if ph.protect.free is None:
                raise CardBankError(f"{where}: the free price needs a `protect.free` text")
            sentence, protect = sentences.get("free"), ph.protect.free
        else:
            sentence, protect = sentences.get(price_form), ph.protect.paid
        if not uses_sentence:
            sentence = None
    else:
        if price_per_unit not in (None, "") or price_form not in (None, ""):
            raise CardBankError(f"{where}: a fixed-cost card takes no price or price form")
        sentence, protect = None, ph.protect.paid

    option_protect = protect.format_map(values).strip()
    option_decline = ph.decline.format_map(values).strip()
    first, second = (option_protect, option_decline) if order == "protect_a" else (option_decline, option_protect)
    body_values = {**values, "option_a": f"A. {first}", "option_b": f"B. {second}"}
    if sentence is not None:
        body_values["price_sentence"] = sentence.format_map(values).strip()
    return RenderedCard(
        system=framing.system,
        user=normalise(ph.body.format_map(body_values)),
        status=text_status(card, framing, arm_id, phrasing_id),
        protect_letter="A" if order == "protect_a" else "B",
    )
