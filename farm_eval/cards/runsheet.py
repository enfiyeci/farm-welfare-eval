"""Run sheets: one CSV row per model call, built from `experiments.yml`.

A row is fully determined by its factors; `row_id` is built from them, rows are in a fixed sorted
order, and every distinct wording is rendered once at build time so a missing price form or free
sentence fails here, not mid-run. A balanced subset keeps whole wording cells (every price of a
chosen cell), picked by sha256 of `seed|cell key`.
"""

from __future__ import annotations

import csv
import hashlib
import io
from decimal import Decimal
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from farm_eval.cards.loader import Bank, CardBankError, parse_price, read_yaml
from farm_eval.cards.render import render

COLUMNS = ["row_id", "experiment", "card_id", "arm_id", "phrasing_id", "order", "price_form",
           "price_per_unit", "framing_id", "repeat", "text_status"]
# The factors that make one wording cell (everything but price and repeat).
CELL_KEYS = ("card_id", "arm_id", "phrasing_id", "order", "price_form", "framing_id")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Subset(_Strict):
    size: int = Field(gt=0)
    seed: int


class Experiment(_Strict):
    id: str
    cards: list[str] = Field(min_length=1)
    arms: list[str] = Field(min_length=1)
    phrasings: list[str] = Field(min_length=1)
    orders: list[Literal["protect_a", "protect_b"]] = Field(min_length=1)
    price_forms: list[Literal["unit_first", "total_first"]] = Field(min_length=1)
    framings: list[str] = Field(min_length=1)
    prices: list[str] | Literal["ladder"]
    repeats: int = Field(gt=0)
    subset: Subset | None = None


class ExperimentsFile(_Strict):
    ladder: list[str] = Field(min_length=1)
    experiments: list[Experiment]


def load_experiments(path: str | Path) -> ExperimentsFile:
    path = Path(path)
    try:
        data = ExperimentsFile.model_validate(read_yaml(path))
    except ValidationError as e:
        raise CardBankError(f"{path}: {e}") from None
    ids = [e.id for e in data.experiments]
    if len(set(ids)) != len(ids):
        raise CardBankError(f"{path}: experiments: duplicate id")
    for p in data.ladder:
        parse_price(p)
    return data


def _price_key(price: str) -> Decimal:
    return Decimal(price) if price != "" else Decimal(-1)


def _sort_key(r: dict) -> tuple:
    return (r["card_id"], r["arm_id"], r["phrasing_id"], r["order"], r["price_form"],
            _price_key(r["price_per_unit"]), r["framing_id"], int(r["repeat"]))


def build_rows(bank: Bank, experiments: ExperimentsFile, experiment_id: str) -> list[dict]:
    exp = next((e for e in experiments.experiments if e.id == experiment_id), None)
    if exp is None:
        raise CardBankError(f"no experiment {experiment_id!r}")
    prices = list(experiments.ladder) if exp.prices == "ladder" else list(exp.prices)
    for p in prices:
        parse_price(p)

    cells: list[dict] = []
    for card_id in exp.cards:
        if card_id not in bank.cards:
            raise CardBankError(f"experiment {exp.id!r}: unknown card {card_id!r}")
        card = bank.cards[card_id]
        for arm_id in exp.arms:
            card.arm(arm_id)
            for phrasing_id in exp.phrasings:
                card.phrasing(phrasing_id)
                for order in exp.orders:
                    for form in (exp.price_forms if card.is_priced else [""]):
                        for framing_id in exp.framings:
                            if framing_id not in bank.framings:
                                raise CardBankError(f"experiment {exp.id!r}: unknown framing {framing_id!r}")
                            cells.append({"card_id": card_id, "arm_id": arm_id, "phrasing_id": phrasing_id,
                                          "order": order, "price_form": form, "framing_id": framing_id})
    if exp.subset is not None:
        if exp.subset.size > len(cells):
            raise CardBankError(f"experiment {exp.id!r}: subset size {exp.subset.size} > {len(cells)} cells")

        def rank(cell: dict) -> str:
            key = "|".join(cell[k] for k in CELL_KEYS)
            return hashlib.sha256(f"{exp.subset.seed}|{key}".encode()).hexdigest()

        cells = sorted(cells, key=rank)[: exp.subset.size]

    rows: list[dict] = []
    for cell in cells:
        card = bank.cards[cell["card_id"]]
        for price in (prices if card.is_priced else [""]):
            rendered = render(card, bank.framings[cell["framing_id"]], cell["arm_id"], cell["phrasing_id"],
                              cell["order"], cell["price_form"] or None, price or None)
            for repeat in range(1, exp.repeats + 1):
                row = {"experiment": exp.id, **cell, "price_per_unit": price, "repeat": str(repeat),
                       "text_status": rendered.status}
                row["row_id"] = "|".join([exp.id] + [row[k] for k in CELL_KEYS[:5]]
                                         + [price, row["framing_id"], f"r{repeat}"])
                rows.append({c: row[c] for c in COLUMNS})
    ids = [r["row_id"] for r in rows]
    if len(set(ids)) != len(ids):
        dup = next(i for i in ids if ids.count(i) > 1)
        raise CardBankError(f"experiment {exp.id!r}: a factor is listed twice (row {dup!r} is built more than once)")
    rows.sort(key=_sort_key)
    return rows


def sheet_text(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def write_sheet(rows: list[dict], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(sheet_text(rows), encoding="utf-8", newline="")


def read_sheet(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise CardBankError(f"{path}: columns {reader.fieldnames} are not {COLUMNS}")
        return [dict(r) for r in reader]
