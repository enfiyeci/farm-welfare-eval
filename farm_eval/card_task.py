"""The value-card Inspect @task: one sample per run-sheet row, one turn, no tools, no grader.

    inspect eval farm_eval/card_task.py -T sheet=schedule/cards/runsheets/E7_noise_floor.csv --model <id>
    inspect eval farm_eval/card_task.py -T sheet=... -T responder=threshold_2.30 --model mockllm/model

Invoke by a relative path from the repo root (absolute task paths fail on Python 3.14). Inspect
chdirs into this file's folder, so data paths are anchored to the repo root with `from_root`.

Draft gate, in two places: a sheet with any draft row is refused at build unless
`allow_draft=True`, and the solver refuses a draft sample on any model API but `mockllm`, before
any generation. A draft text can therefore reach only the mock model or a scripted responder.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.model import ChatMessageAssistant, ChatMessageSystem, ChatMessageUser, GenerateConfig, ModelOutput
from inspect_ai.scorer import Score, Target, scorer
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.cards.loader import load_bank
from farm_eval.cards.parse import outcome, read_decision
from farm_eval.cards.render import counts, planted_value, render
from farm_eval.cards.responders import is_responder, respond
from farm_eval.cards.runsheet import read_sheet
from farm_eval.config_paths import from_root

MAX_RETRIES = 3
MOCK_API = "mockllm"


@solver
def card_solver(responder: str | None = None, seed: int = 0):
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        # Allow-list: anything that is not marked owner_approved counts as draft.
        if state.metadata.get("text_status") != "owner_approved" and state.model.api != MOCK_API:
            raise RuntimeError(
                f"sample {state.sample_id!r}: draft text may not be sent to {state.model} "
                f"(only {MOCK_API} or a scripted responder on {MOCK_API})"
            )
        if responder is None:
            return await generate(state)
        text = respond(responder, state.metadata, seed)
        name = f"scripted/{responder}"
        state.messages.append(ChatMessageAssistant(content=text, model=name))
        state.output = ModelOutput.from_content(model=name, content=text)
        return state

    return solve


@scorer(metrics=[])
def card_scorer():
    async def score(state: TaskState, target: Target) -> Score:
        out = state.output
        text = out.completion if out is not None else ""
        stop = str(out.stop_reason) if out is not None and out.stop_reason is not None else None
        d = read_decision(text, stop)
        return Score(
            value=outcome(d, state.metadata["protect_letter"]),
            answer=d.letter,
            metadata={"status": d.status, "flags": list(d.flags), "stop_reason": stop},
        )

    return score


@task
def card_task(
    sheet: str,
    allow_draft: bool = False,
    responder: str | None = None,
    seed: int = 0,
    max_tokens: int = 2000,
    cards_dir: str = "schedule/cards",
) -> Task:
    rows = read_sheet(from_root(sheet))
    bank = load_bank(from_root(cards_dir))
    if responder is not None and not is_responder(responder):
        raise ValueError(f"unknown scripted responder {responder!r}")
    drafts = [r["row_id"] for r in rows if r["text_status"] == "draft"]
    if drafts and not allow_draft:
        raise ValueError(f"{sheet}: {len(drafts)} rows carry draft text (first {drafts[0]!r}); "
                         "draft text needs allow_draft=True and may reach only mockllm or a scripted responder")
    samples = []
    for row in rows:
        card = bank.cards[row["card_id"]]
        framing = bank.framings[row["framing_id"]]
        r = render(card, framing, row["arm_id"], row["phrasing_id"], row["order"],
                   row["price_form"] or None, row["price_per_unit"] or None)
        if r.status != row["text_status"]:
            raise ValueError(f"{sheet}: row {row['row_id']!r} says {row['text_status']} but the text is "
                             f"now {r.status}; rebuild the sheet")
        priced, spared = counts(card, row["arm_id"])
        meta = {**row, "protect_letter": r.protect_letter, "priced_count": priced, "spared_count": spared,
                "held_out": card.phrasing(row["phrasing_id"]).held_out}
        planted = planted_value(card, framing, row["arm_id"])
        if planted is not None:
            meta["planted_value_per_unit"] = str(planted)
        if responder is not None:
            meta["scripted_responder"] = responder
        messages = ([ChatMessageSystem(content=r.system)] if r.system is not None else []) + [
            ChatMessageUser(content=r.user)]
        samples.append(Sample(id=row["row_id"], input=messages, metadata=meta))
    return Task(
        dataset=samples,
        solver=card_solver(responder=responder, seed=seed),
        scorer=card_scorer(),
        config=GenerateConfig(max_tokens=max_tokens, max_retries=MAX_RETRIES),
        # One provider error must not cancel the batch.
        fail_on_error=False,
    )
