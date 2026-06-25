"""Email read tools: the inbox is the one fixed authored artifact (not computed)."""

from __future__ import annotations

import json

from inspect_ai.tool import Tool, tool

from farm_eval.adapter.context import EpisodeConfig, get_env


@tool
def list_emails(cfg: EpisodeConfig) -> Tool:
    async def execute(unread_only: bool = False) -> str:
        """List emails in the inbox (id, date, sender, subject, unread flag).

        Args:
            unread_only: If true, list only unread emails.

        Returns:
            One JSON record per email (headers only; use read_email for the body).
        """
        env = get_env(cfg)
        return json.dumps(env.list_emails(unread_only=unread_only))

    return execute


@tool
def read_email(cfg: EpisodeConfig) -> Tool:
    async def execute(email_id: str) -> str:
        """Read the full body of an email and mark it read.

        Args:
            email_id: The id of the email to read (from list_emails).

        Returns:
            The full email as a JSON record, or an error if the id is unknown.
        """
        env = get_env(cfg)
        try:
            return json.dumps(env.read_email(email_id))
        except KeyError:
            return f"No email with id {email_id!r}."

    return execute
