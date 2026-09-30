"""B1 — the episode context: EnvState lives in the Inspect store; FarmEnv binds to it."""

from pathlib import Path

from inspect_ai import Task
from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import Generate, TaskState, solver

from farm_eval.adapter.context import EpisodeConfig, get_env, load_resources
from farm_eval.adapter import context as ctx

FIX = Path(__file__).resolve().parents[1] / "fixtures"
CFG = EpisodeConfig(
    corpus_path=str(FIX / "corpus"), schedule_path=str(FIX / "schedule"), episode_end_day=400, seed=1
)


def test_load_resources_caches_by_path():
    ctx._resources.clear()
    a = load_resources(CFG)
    b = load_resources(CFG)
    assert a is b  # same cached (corpus, schedule) tuple — loaded once
    assert a[1].decision_points  # schedule parsed


def test_double_start_does_not_duplicate_day0_events():
    # get_env rebuilds a fresh FarmEnv each call; start() must be idempotent against the persisted
    # EnvState, not a transient instance flag, or day-0 events re-fire on re-entry/replay.
    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            get_env(CFG).start()
            get_env(CFG).start()  # a second fresh wrapper — must NOT re-fire day-0 events
            env = get_env(CFG)
            state.metadata["mailbox"] = len(env.state.mailbox)
            state.metadata["event_log"] = len(env.state.event_log)
            return state

        return solve

    log = inspect_eval(
        Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none"
    )[0]
    md = log.samples[0].metadata
    assert md["mailbox"] == 1  # the single day-0 email, delivered once
    assert md["event_log"] == 1


def test_get_env_binds_store_and_persists_mutation():
    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            env = get_env(CFG)
            env.start()
            result = env.apply_action(
                "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5}
            )
            state.metadata["addressed"] = result.addressed_dps
            env2 = get_env(CFG)  # a second accessor in the same sample sees the SAME state
            state.metadata["same_state"] = env2.state is env.state
            return state

        return solve

    log = inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model", display="none")[0]
    assert log.status == "success"
    sample = log.samples[0]
    assert sample.metadata["addressed"] == ["DP_PLACEHOLDER_1"]
    assert sample.metadata["same_state"] is True
    # The welfare/ledger state persisted into the .eval store (serialized EnvState).
    env_state = sample.store["EpisodeStore:env_state"]
    assert env_state is not None
    ledger = env_state["ledger"]
    addressed = [e for e in ledger if e["dp_id"] == "DP_PLACEHOLDER_1"]
    assert addressed and addressed[0]["status"] == "addressed"


# --- C3: an arm with ablation_overrides must not reload the corpus on every tool call -----------
# get_env rebuilds a FarmEnv per tool call; with overrides set, load_resources used to bypass its
# cache and re-read + re-validate + re-apply the whole corpus each time (~0.28 s per call). The
# overridden load is now cached under its own key (paths + the frozen overrides), never under the
# pristine baseline's.


_DOC_ID = sorted(ctx.load_corpus(CFG.corpus_path).documents)[0]   # read once, before any counting


def _ablation_cfg(tmp_path, body="ABLATED BODY", name="variant.md"):
    doc_id = _DOC_ID
    variant = tmp_path / name
    variant.write_text(body, encoding="utf-8")
    cfg = EpisodeConfig(corpus_path=CFG.corpus_path, schedule_path=CFG.schedule_path, episode_end_day=400,
                        seed=1, ablation_overrides={doc_id: str(variant)})
    return cfg, doc_id


def _count_corpus_loads(monkeypatch):
    calls = {"n": 0}
    real = ctx.load_corpus

    def counting(path):
        calls["n"] += 1
        return real(path)

    monkeypatch.setattr(ctx, "load_corpus", counting)
    return calls


def test_overridden_load_is_cached_by_overrides(tmp_path, monkeypatch):
    cfg, doc_id = _ablation_cfg(tmp_path)
    ctx._resources.clear()
    calls = _count_corpus_loads(monkeypatch)
    try:
        a = load_resources(cfg)
        b = load_resources(cfg)
        assert a is b and calls["n"] == 1
        assert a[0].documents[doc_id] == "ABLATED BODY"
        # a different override set is a different entry, and the baseline stays pristine
        other, _ = _ablation_cfg(tmp_path, body="OTHER BODY", name="other.md")
        assert load_resources(other)[0].documents[doc_id] == "OTHER BODY"
        assert load_resources(CFG)[0].documents[doc_id] != "ABLATED BODY"
        assert calls["n"] == 3
        # an arm's overrides (the `overrides=` argument) share the entry of an equal config set
        assert load_resources(CFG, overrides=dict(cfg.ablation_overrides)) is a
        assert calls["n"] == 3
    finally:
        ctx._resources.clear()


def test_two_tool_calls_under_overrides_load_the_corpus_once(tmp_path, monkeypatch):
    cfg, _ = _ablation_cfg(tmp_path)
    ctx._resources.clear()
    calls = _count_corpus_loads(monkeypatch)

    @solver
    def drive():
        async def solve(state: TaskState, generate: Generate) -> TaskState:
            get_env(cfg).start()
            get_env(cfg).apply_action(
                "adjust_setpoint", {"house_id": "H_SENSOR", "system": "ventilation", "value": 2.5})
            get_env(cfg).current_day()
            return state

        return solve

    try:
        log = inspect_eval(Task(dataset=[Sample(input="go")], solver=drive()), model="mockllm/model",
                           display="none")[0]
        assert log.status == "success", log.error
        assert calls["n"] == 1
    finally:
        ctx._resources.clear()
