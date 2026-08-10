#!/usr/bin/env bash
# Stop hook: auto-push the session's branch when it is strictly ahead of its upstream.
#
# Owner-authorized 2026-08-10, after the litter-lever divergence: a finished 39-commit
# lane sat unpushed on one machine over a weekend and the other machine rebuilt the same
# plan from the same handoff. The handoff docs sync automatically (claude-sync's Stop
# hook); the repo branches did not — this closes that gap.
#
# Safety properties, in order of importance:
#   * NEVER forces. A diverged branch (ahead AND behind) is reported, not resolved —
#     divergence is exactly the state where an automatic push would destroy information.
#   * A stale tracking ref cannot cause damage: if the remote moved and we don't know,
#     the push is rejected as non-fast-forward and reported as failed.
#   * Skips detached HEAD and the throwaway remote-control bridge branches.
#   * Always exits 0 — a broken push must never block the session from stopping.
set -u
export GIT_TERMINAL_PROMPT=0
cat >/dev/null 2>&1 || true # drain hook stdin (JSON payload; unused)

root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" || exit 0
branch=$(git symbolic-ref --short -q HEAD) || exit 0
case "$branch" in worktree-bridge-*) exit 0 ;; esac

if upstream=$(git rev-parse --abbrev-ref '@{u}' 2>/dev/null); then
  ahead=$(git rev-list --count "$upstream..HEAD" 2>/dev/null) || exit 0
  behind=$(git rev-list --count "HEAD..$upstream" 2>/dev/null) || exit 0
  [ "${ahead:-0}" -gt 0 ] || exit 0
  if [ "${behind:-0}" -gt 0 ]; then
    printf '{"systemMessage":"auto-push: %s is ahead %s AND behind %s of %s -- diverged; not pushing. Reconcile by hand."}\n' \
      "$branch" "$ahead" "$behind" "$upstream"
    exit 0
  fi
  if git push origin "$branch" >/dev/null 2>&1; then
    printf '{"systemMessage":"auto-push: pushed %s (%s commit(s)) to origin"}\n' "$branch" "$ahead"
  else
    printf '{"systemMessage":"auto-push: push of %s FAILED (rejected or offline) -- the branch is still local-only. Push it by hand."}\n' "$branch"
  fi
else
  # No upstream yet: publish the branch (global rule 6: `git push -u origin HEAD`).
  if git push -u origin "$branch" >/dev/null 2>&1; then
    printf '{"systemMessage":"auto-push: published new branch %s to origin"}\n' "$branch"
  else
    printf '{"systemMessage":"auto-push: publishing %s FAILED -- the branch is still local-only. Push it by hand."}\n' "$branch"
  fi
fi
exit 0
