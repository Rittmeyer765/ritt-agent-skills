---
name: check-upstream
description: Check whether a tracked upstream (mattpocock/skills or the agent-skills-spec) has new changes, produce a review report, and never modify local skills automatically.
disable-model-invocation: true
---

Update checks are read-only. Nothing in this flow may touch `plugins/` — promoting an upstream idea into a local skill is always a manual edit after review.

## Procedure

Run from the ritt-agent-skills repository root:

1. **Check:** `python3 scripts/check_upstream.py [--source <name>]` — compares upstream HEAD against the accepted baseline in `upstream/<source>/LOCK.json`. Sources: `mattpocock` (default) and `agent-skills-spec`. Exit 0 = `UP_TO_DATE`, 1 = `UPDATE_AVAILABLE`, 2 = `NO_BASELINE` (e.g. agent-skills-spec has none yet), 3 = `UNVERIFIED`. Run once per source.
2. **On `UPDATE_AVAILABLE`:** import the candidate and diff it against the baseline:
   ```bash
   python3 scripts/import_upstream.py --revision <new-head-sha>
   python3 scripts/compare_upstream.py --candidate <new-head-sha>
   ```
3. **Summarize for review.** Read the comparison report in `reports/upstream/` and, for each added/modified tracked file, cross-reference `upstream/mattpocock/CUSTOMIZATIONS.json` to say which LOCAL skill might benefit. Present: what changed upstream, whether it is relevant, and a recommendation (ignore / port manually / track a new path).
4. **Only if the user explicitly accepts** the new baseline:
   ```bash
   python3 scripts/accept_upstream.py --revision <sha> --confirm <sha>
   ```

## Hard rules

- Never edit anything under `plugins/` during this flow.
- Never run `accept_upstream.py` without the user's explicit go-ahead in this conversation.
- If the user wants to port an upstream change, do it as a normal reviewed edit (plan-change → implement-change) and record it in `CUSTOMIZATIONS.json`.
