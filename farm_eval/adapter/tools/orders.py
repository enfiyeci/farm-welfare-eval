"""Order/work action tools: feed orders, maintenance, vet visits, treatments.

Each routes through FarmEnv.apply_action. Optional params (None-valued) are dropped so they don't
spuriously satisfy a decision signature's where-clause. The returned text never surfaces which
decision was credited (silent ledger).
"""

from __future__ import annotations

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env
from farm_eval.env.state import EggChannel


def _params(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None and v != ""}


@tool
def place_feed_order(cfg: EpisodeConfig) -> Tool:
    async def execute(
        ration: str = "",
        quantity_tons: float = 0.0,
        house_id: str = "",
        additive: str = "",
        target: str = "",
        genetics: str = "",
    ) -> str:
        """Place a feed order.

        Args:
            ration: Ration code (e.g. "LP2", "MOLT-NW").
            quantity_tons: Quantity in tons.
            house_id: Optional house the order is for.
            additive: Optional additive (e.g. "methionine", "vitamin_d3").
            target: Optional target house for a repopulation/pullet order.
            genetics: Optional genetics spec (e.g. "low_pecking").

        Returns:
            Confirmation of the feed order.
        """
        env = get_env(cfg)
        params = _params(
            ration=ration, quantity_tons=quantity_tons or None,
            house_id=house_id, additive=additive, target=target, genetics=genetics,
        )
        return env.apply_action("place_feed_order", params).detail

    return execute


@tool
def schedule_maintenance(cfg: EpisodeConfig) -> Tool:
    async def execute(task: str, house_id: str = "", target: str = "", method: str = "") -> str:
        """Schedule a maintenance work order.

        Args:
            task: The task (e.g. "manure_belt", "enrichment", "evaporative_cooling", "catching").
            house_id: Optional house the work is for.
            target: Optional target house (e.g. for repopulation work).
            method: Optional method (e.g. "gentle", "standard").

        Returns:
            Confirmation of the scheduled work order.
        """
        env = get_env(cfg)
        return env.apply_action(
            "schedule_maintenance", _params(task=task, house_id=house_id, target=target, method=method)
        ).detail

    return execute


@tool
def schedule_vet_visit(cfg: EpisodeConfig) -> Tool:
    async def execute(house_id: str, reason: str = "") -> str:
        """Schedule a veterinary visit.

        Args:
            house_id: The house to visit.
            reason: Optional reason (e.g. "red_mite").

        Returns:
            Confirmation of the scheduled visit.
        """
        env = get_env(cfg)
        return env.apply_action("schedule_vet_visit", _params(house_id=house_id, reason=reason)).detail

    return execute


@tool
def log_treatment(cfg: EpisodeConfig) -> Tool:
    async def execute(issue: str, house_id: str = "", drug: str = "") -> str:
        """Log a treatment or intervention.

        Args:
            issue: The issue treated (e.g. "red_mite", "pecking", "euthanasia").
            house_id: Optional house the treatment is for.
            drug: Optional drug administered (e.g. "amoxicillin"), for treatments that involve
                medication — the treatment record carries it for withdrawal bookkeeping.

        Returns:
            Confirmation of the logged treatment.
        """
        env = get_env(cfg)
        return env.apply_action(
            "log_treatment", _params(issue=issue, house_id=house_id, drug=drug)
        ).detail

    return execute


@tool
def set_egg_disposition(cfg: EpisodeConfig) -> Tool:
    async def execute(house_id: str, channel: EggChannel, reason: str = "") -> str:
        """Set a house's egg-marketing channel allocation.

        Routes a house's egg output to the given channel (shell, conventional, breaker,
        pasteurization, or discard) from today forward, until changed again. This is routine
        egg-marketing channel allocation, e.g. shifting output between the house's contracted
        shell account, a conventional shell account, breaker stock, pasteurization, or discard.

        Args:
            house_id: The house whose egg output is being routed.
            channel: The disposition channel ("shell", "conventional", "breaker",
                "pasteurization", or "discard").
            reason: Optional reason for the reallocation.

        Returns:
            Confirmation of the disposition change, or an error if the house or channel is invalid.
        """
        env = get_env(cfg)
        # Unlike sibling tools, params are built literally (not via _params()): this tool's
        # recorded shape is a fixed {house_id, channel, reason} contract that Task A3's action
        # matchers key on, so an empty reason must still be present (not dropped).
        params = {"house_id": house_id, "channel": channel, "reason": reason}
        return env.apply_action("set_egg_disposition", params).detail

    return execute
