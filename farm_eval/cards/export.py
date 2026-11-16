"""Export every distinct rendered prompt (system message, then card) to markdown for reading."""

from __future__ import annotations

from farm_eval.cards.loader import Bank, CardBankError
from farm_eval.cards.render import ORDERS, PRICE_FORMS, render

_KEY = ("card_id", "arm_id", "phrasing_id", "order", "price_form", "price_per_unit", "framing_id")


def _render_row(bank: Bank, r: dict):
    card = bank.cards[r["card_id"]]
    return render(card, bank.framings[r["framing_id"]], r["arm_id"], r["phrasing_id"], r["order"],
                  r["price_form"] or None, r["price_per_unit"] or None)


def _markdown(title: str, prompts: dict, skipped: list[str]) -> str:
    out = [f"# Card wordings: {title}", "",
           f"{len(prompts)} distinct prompts. Text marked draft has not been read by the owner.", ""]
    for i, ((system, user), info) in enumerate(prompts.items(), start=1):
        out += [f"## Prompt {i}", "", f"status: {info['status']}; rows: {info['rows']}", "",
                "Used by: " + "; ".join(info["keys"]), "", "### System message", ""]
        out += (["```text", system, "```"] if system is not None else ["(no system message)"])
        out += ["", "### Card", "", "```text", user, "```", ""]
    if skipped:
        out += ["## Not available", ""] + [f"- {s}" for s in skipped] + [""]
    return "\n".join(out)


def _add(prompts: dict, rendered, key: str) -> None:
    info = prompts.setdefault((rendered.system, rendered.user),
                              {"status": rendered.status, "rows": 0, "keys": []})
    info["rows"] += 1
    if key not in info["keys"]:
        info["keys"].append(key)


def export_markdown(bank: Bank, rows: list[dict], *, title: str) -> str:
    """Each distinct rendered prompt in a run sheet once, with its row count and status."""
    prompts: dict = {}
    for r in rows:
        key = ", ".join(f"{k} {r[k] or '-'}" for k in _KEY)
        _add(prompts, _render_row(bank, r), key)
    return _markdown(title, prompts, [])


def export_all_markdown(bank: Bank, *, ladder: list[str]) -> str:
    """Every phrasing, order and price form of every card at every ladder price (each arm, under
    the card's default framing). Combinations the card has no text for are listed, not rendered."""
    prompts: dict = {}
    skipped: list[str] = []
    for card_id, card in sorted(bank.cards.items()):
        framing = bank.framings[card.framing]
        for arm in card.arms:
            for ph in card.phrasings:
                for order in ORDERS:
                    for form in (PRICE_FORMS if card.is_priced else (None,)):
                        for price in (ladder if card.is_priced else (None,)):
                            key = (f"card_id {card_id}, arm_id {arm.arm_id}, phrasing_id {ph.id}, order {order}, "
                                   f"price_form {form or '-'}, price_per_unit {price or '-'}, framing_id {card.framing}")
                            try:
                                rendered = render(card, framing, arm.arm_id, ph.id, order, form, price)
                            except CardBankError as e:
                                skipped.append(f"{key}: {e}")
                                continue
                            _add(prompts, rendered, key)
    return _markdown("all cards", prompts, skipped)
