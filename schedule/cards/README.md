# Value card bank

Eval: hen

This folder holds every model-visible text of the value card bank and the files that drive it: `framings.yml` (system messages), one `<card_id>.yml` per decision card, `experiments.yml` (the price ladder and each experiment's factors), `rules.yml` (the analysis numbers and each experiment's question and pass rule) and `runsheets/` (one CSV per experiment, one row per model call, built by `scripts/cards_build_sheets.py`). Code under `farm_eval/cards/` refers only to generic keys; all card text lives here. Any text marked `status: draft` has not been read by the owner and must not reach a paid model: `farm_eval/card_task.py` refuses a sheet with a draft row unless `allow_draft=True`, and even then sends a draft text only to `mockllm` or a scripted responder.
