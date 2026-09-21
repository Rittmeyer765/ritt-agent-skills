---
name: graphify-map
description: Navigate a codebase via Graphify's local code knowledge graph (Tree-sitter, no LLM) to get structural relationships and file:line citations. Use for "where is X defined/used", call/dependency paths, or impact of a change - as a READ-ONLY map, not a source of truth. Manual-only; requires the `graphify` CLI already installed.
compatibility: Requires the `graphify` CLI (official package `graphifyy`) on PATH. Optional; this adapter never installs it.
disable-model-invocation: true
---

> Manual-only adapter. It **never installs Graphify**, never runs `graphify install`, and never edits `AGENTS.md`, `CLAUDE.md`, settings, or hooks. Graphify's own installer would collide with this kit — do not use it.

Graphify builds a queryable graph of the code so you trace and cite instead of grepping. Treat it as a **derived map**, not memory and not ground truth.

## Procedure

Graphify has two operations — **build the graph, then query it**. Always go through the wrapper
`scripts/graphify_map.sh` (from this skill dir), never `graphify` directly.

1. **Build (code-only):** `scripts/graphify_map.sh build [path]` → runs `graphify extract <path> --code-only`
   (default path `.`). Only build when the user asks; **never** as a side effect of another task.
2. **Query:** `scripts/graphify_map.sh query "<question>"` → runs `graphify query "<question>" --budget ${GRAPHIFY_QUERY_BUDGET:-1500}`.
   Query logging is disabled by default (`GRAPHIFY_QUERY_LOG_DISABLE=1`); the budget caps the answer size (default 1500, override with `GRAPHIFY_QUERY_BUDGET`, validated to 100..100000). Navigation passthroughs `path`/`explain` are allowed explicitly when the task needs them.
3. **If `graphify` is missing:** the wrapper prints the official package (`graphifyy`) and **exits 3**.
   Stop and tell the user to install it manually (`uv tool install graphifyy==<pinned>`); never install it yourself.
4. **Refused (exit 4):** `install`, `hook(s)`, `mcp`/`serve`, document/media extraction, and any unknown op.
   Document, PDF, image, URL, MCP, or LLM/network modes require the user to run Graphify directly with
   explicit confirmation — this adapter stays code-only.

Exit codes: `2` usage · `3` graphify not installed (never installs) · `4` refused op.

## Using results

- `INFERRED` relationships are **hypotheses**, label them as such, never as facts.
- Confirm any consequential finding by reading the real file at the cited `file:line`.
- In Bazel projects, `bazel query` / `cquery` remain the source of truth; the graph is a hint.
- The graph does **not** replace `.agent/` memory — it is regenerable, memory is decisions.

## Outputs stay local

`graphify-out/` and `graph.json` are large, machine-specific, and can churn the model cache.
- Keep them **out of git**: add `graphify-out/` and `graph.json` to the repo's `.git/info/exclude` (local-only; never commit, never add to a corporate project's shared templates).
- Keep them **out of Claude's context** (don't paste them); query through the graph instead.
- **Never** sync them to Obsidian, OneDrive, or any external store.
