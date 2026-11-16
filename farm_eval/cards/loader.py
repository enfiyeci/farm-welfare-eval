"""Strict loader for the value card bank (`schedule/cards/`).

A bank folder holds `framings.yml` (system messages) and one `<card_id>.yml` per card;
`experiments.yml` and `rules.yml` sit beside them and are read elsewhere. Every error names the
file and the key. Money is exact `Decimal` arithmetic. No card text lives in this module.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

Status = Literal["owner_approved", "draft"]

SCALAR_SLOTS = frozenset({"price_per_unit", "price_total", "count", "spared_count"})
BODY_SLOTS = SCALAR_SLOTS | {"price_sentence", "option_a", "option_b"}
PRICE_SLOTS = frozenset({"price_sentence", "price_per_unit", "price_total"})
NON_CARD_FILES = frozenset({"framings.yml", "experiments.yml", "rules.yml"})


class CardBankError(ValueError):
    """A bank file is wrong, or a render asked for something the card does not have."""


# --- YAML with duplicate-key detection ---------------------------------------------------------

class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    seen: set = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise CardBankError(f"duplicate key {key!r} (line {key_node.start_mark.line + 1})")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def read_yaml(path: Path) -> object:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except CardBankError as e:
        raise CardBankError(f"{path}: {e}") from None


# --- models -----------------------------------------------------------------------------------

class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


def _check_decimal(v: str | None) -> str | None:
    if v is None:
        return v
    try:
        d = Decimal(v)
    except InvalidOperation:
        raise ValueError(f"not a decimal string: {v!r}") from None
    if not d.is_finite() or d < 0:
        raise ValueError(f"must be a finite decimal >= 0: {v!r}")
    return v


class FramingHidden(_Strict):
    planted_value_per_unit: str | None = None
    note: str | None = None

    _dec = field_validator("planted_value_per_unit")(_check_decimal)


class Framing(_Strict):
    status: Status
    system: str | None = None
    base: str | None = None
    append: str | None = None
    hidden: FramingHidden = FramingHidden()

    @model_validator(mode="after")
    def _system_or_base(self):
        has_system = "system" in self.model_fields_set
        if has_system == (self.base is not None):
            raise ValueError("give exactly one of `system` (text, or null for none) or `base`")
        return self


class FramingsFile(_Strict):
    framings: dict[str, Framing]


class Unit(_Strict):
    name: str
    count: int = Field(gt=0)


class Arm(_Strict):
    arm_id: str
    slots: dict[str, str] = {}
    priced_count: int | None = Field(default=None, gt=0)
    spared_count: int | None = Field(default=None, ge=0)  # 0: a control arm that spares nobody
    # Never rendered. For a card that states the value as money inside its own text (in a slot).
    planted_value_per_unit: str | None = None

    _dec = field_validator("planted_value_per_unit")(_check_decimal)


class PriceSentence(_Strict):
    unit_first: str | None = None
    total_first: str | None = None
    free: str | None = None


class Protect(_Strict):
    paid: str
    free: str | None = None


class Phrasing(_Strict):
    id: str
    status: Status | None = None
    held_out: bool = False
    body: str
    price_sentence: PriceSentence | None = None
    protect: Protect
    decline: str


class CardHidden(_Strict):
    harm_label: str | None = None
    sources: list[str] = []
    notes: str | None = None


class Card(_Strict):
    card_id: str
    status: Status
    framing: str
    priced_unit: Unit
    spared: Unit
    slots: dict[str, str] = {}
    arms: list[Arm] = [Arm(arm_id="base")]
    phrasings: list[Phrasing] = Field(min_length=1)
    hidden: CardHidden = CardHidden()

    def arm(self, arm_id: str) -> Arm:
        for a in self.arms:
            if a.arm_id == arm_id:
                return a
        raise CardBankError(f"card {self.card_id!r}: no arm {arm_id!r}")

    def phrasing(self, phrasing_id: str) -> Phrasing:
        for p in self.phrasings:
            if p.id == phrasing_id:
                return p
        raise CardBankError(f"card {self.card_id!r}: no phrasing {phrasing_id!r}")

    def phrasing_status(self, phrasing_id: str) -> str:
        return self.phrasing(phrasing_id).status or self.status

    def templates(self, phrasing: Phrasing) -> dict[str, str]:
        """Every template of one phrasing, keyed by its place in the file."""
        out = {"body": phrasing.body, "protect.paid": phrasing.protect.paid, "decline": phrasing.decline}
        if phrasing.protect.free is not None:
            out["protect.free"] = phrasing.protect.free
        if phrasing.price_sentence is not None:
            for form, text in phrasing.price_sentence.model_dump().items():
                if text is not None:
                    out[f"price_sentence.{form}"] = text
        return out

    @property
    def is_priced(self) -> bool:
        """False for a fixed-cost card: no template uses a price slot, so its rows carry no price."""
        return any(slot_names(t) & PRICE_SLOTS for p in self.phrasings for t in self.templates(p).values())


@dataclass(frozen=True)
class ResolvedFraming:
    framing_id: str
    status: str
    system: str | None
    planted_value_per_unit: Decimal | None


@dataclass(frozen=True)
class Bank:
    cards_dir: Path
    framings: dict[str, ResolvedFraming]
    cards: dict[str, Card]


# --- text helpers -----------------------------------------------------------------------------

def slot_names(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name is not None}


def normalise(text: str) -> str:
    """Strip trailing whitespace on every line; join paragraphs with exactly one blank line."""
    lines = [ln.rstrip() for ln in text.split("\n")]
    paras: list[list[str]] = [[]]
    for ln in lines:
        if ln.strip():
            paras[-1].append(ln)
        elif paras[-1]:
            paras.append([])
    return "\n\n".join("\n".join(p) for p in paras if p)


def fmt_count(n: int) -> str:
    return f"{n:,}"


def fmt_per_unit(price: Decimal) -> str:
    return f"${price.quantize(Decimal('0.01')):,.2f}"


def fmt_total(total: Decimal) -> str:
    if total == total.to_integral_value():
        return f"${int(total):,}"
    return f"${total.quantize(Decimal('0.01')):,.2f}"


# --- loading ----------------------------------------------------------------------------------

def _validation_error(path: Path, e: ValidationError) -> CardBankError:
    parts = []
    for err in e.errors():
        loc = ".".join(str(x) for x in err["loc"]) or "(top level)"
        parts.append(f"{loc}: {err['msg']}")
    return CardBankError(f"{path}: " + "; ".join(parts))


def _resolve_framings(path: Path, raw: FramingsFile) -> dict[str, ResolvedFraming]:
    out: dict[str, ResolvedFraming] = {}

    def resolve(fid: str, chain: tuple[str, ...]) -> ResolvedFraming:
        if fid in out:
            return out[fid]
        if fid in chain:
            raise CardBankError(f"{path}: framings.{fid}.base: cycle {' -> '.join(chain + (fid,))}")
        fr = raw.framings[fid]
        status = fr.status
        if fr.base is not None:
            if fr.base not in raw.framings:
                raise CardBankError(f"{path}: framings.{fid}.base: unknown framing {fr.base!r}")
            parent = resolve(fr.base, chain + (fid,))
            text = parent.system
            # Text taken from a draft framing keeps the result draft.
            if parent.status == "draft":
                status = "draft"
        else:
            text = fr.system
        if fr.append is not None:
            text = fr.append if text is None else f"{text.rstrip()}\n\n{fr.append.strip()}"
        planted = fr.hidden.planted_value_per_unit
        out[fid] = ResolvedFraming(
            framing_id=fid, status=status,
            system=normalise(text) if text is not None else None,
            planted_value_per_unit=Decimal(planted) if planted is not None else None,
        )
        return out[fid]

    for fid in raw.framings:
        resolve(fid, ())
    return out


def _check_card(path: Path, card: Card, framings: dict[str, ResolvedFraming]) -> None:
    def err(key: str, msg: str) -> CardBankError:
        return CardBankError(f"{path}: {key}: {msg}")

    if card.framing not in framings:
        raise err("framing", f"unknown framing {card.framing!r}")
    for kind, ids in (("arms", [a.arm_id for a in card.arms]), ("phrasings", [p.id for p in card.phrasings])):
        seen: set[str] = set()
        for i in ids:
            if i in seen:
                raise err(kind, f"duplicate id {i!r}")
            seen.add(i)

    used: set[str] = set()
    for ph in card.phrasings:
        for where, template in card.templates(ph).items():
            names = slot_names(template)
            used |= names
            allowed = BODY_SLOTS if where == "body" else SCALAR_SLOTS
            for arm in card.arms:
                defined = set(card.slots) | set(arm.slots)
                for name in sorted(names - allowed - defined):
                    raise err(f"phrasings.{ph.id}.{where}", f"unknown slot {{{name}}}"
                              + (f" (arm {arm.arm_id!r})" if arm.slots else ""))
        if "price_sentence" in slot_names(ph.body) and ph.price_sentence is None:
            raise err(f"phrasings.{ph.id}.price_sentence", "the body uses {price_sentence} but none is given")
    for name in sorted(set(card.slots) - used):
        raise err(f"slots.{name}", "defined slot that no template uses")
    for arm in card.arms:
        for name in sorted(set(arm.slots) - used):
            raise err(f"arms.{arm.arm_id}.slots.{name}", "defined slot that no template uses")


def load_bank(cards_dir: str | Path) -> Bank:
    cards_dir = Path(cards_dir)
    fpath = cards_dir / "framings.yml"
    try:
        raw = FramingsFile.model_validate(read_yaml(fpath))
    except ValidationError as e:
        raise _validation_error(fpath, e) from None
    framings = _resolve_framings(fpath, raw)

    cards: dict[str, Card] = {}
    for path in sorted(cards_dir.glob("*.yml")):
        if path.name in NON_CARD_FILES:
            continue
        try:
            card = Card.model_validate(read_yaml(path))
        except ValidationError as e:
            raise _validation_error(path, e) from None
        if card.card_id in cards:
            raise CardBankError(f"{path}: card_id: duplicate id {card.card_id!r}")
        _check_card(path, card, framings)
        cards[card.card_id] = card
    return Bank(cards_dir=cards_dir, framings=framings, cards=cards)


def parse_price(price: str | Decimal) -> Decimal:
    try:
        d = Decimal(price)
    except InvalidOperation:
        raise CardBankError(f"price {price!r} is not a decimal") from None
    if not d.is_finite() or d < 0:
        raise CardBankError(f"price {price!r} must be a finite decimal >= 0")
    if d != d.quantize(Decimal("0.01")):
        raise CardBankError(f"price {price!r} has more than two decimal places")
    return d
