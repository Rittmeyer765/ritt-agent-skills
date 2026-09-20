---
name: research-plan-implement
description: Run a large or brownfield change as three context-isolated phases — Research, Plan, Implement — keeping a single active task file as the source of truth and the context lean so bad research can't leak into thousands of bad lines. Use when starting a big multi-file change in a large codebase, or when asked for RPI, spec-driven development, or an agentic workflow that resists context rot.
disable-model-invocation: true
---

The only lever on output quality is the quality of the context. Split the work into three phases, each in a FRESH context, so bad research can't leak into thousands of bad lines and the plan stays small enough to review.

This skill is a **light router**: it sequences existing skills; it does not re-implement them, and it never runs the same skill twice in one pass or spawns recursive cascades. The single active task file is `.agent/tasks/<TASK-ID>.md` (canonical schema) — it does NOT create `RESEARCH.md` or `PLANS.md`.

## Procedure

1. **Research — fresh context.** Run `clarify-task`, then `research-and-reuse` (both read-only). Delegate wide searches to read-only sub-agents and keep only distilled findings. The orchestrator records the findings and REUSE/ADAPT/BUILD verdict into the task file's *Verified facts* / *Decisions* sections via `project-memory`. If the research is wrong, redo it now — cheap here, ruinous later.
2. **Plan — fresh context.** Run `plan-change` (read-only): two options + recommendation, phased by dependency, with acceptance criteria. The orchestrator persists it into the *Plan / current step* section of the task file via `project-memory` — this task file, not the code, is the source of truth. Review it visually with plannotator when available.
3. **Implement — fresh context.** Start from the task file alone. Run `implement-change` phase by phase (single writer, no subagents); after each phase the orchestrator runs `validate-change` and compacts status back into the task file (tick the phase). Checkpoint with a commit only if the project's workflow already uses commits — never push. Read and own every diff.

## Rules

- Keep context utilization ~40–60%. When it climbs, compact to the task file and reset.
- One phase = one goal = one context.
- The task file is a contract: if reality contradicts it mid-implementation, stop and revise it — don't improvise silently.
- Only the orchestrator writes memory (`project-memory`), exactly once per closing step — secondary agents never write memory.
- Close with `review-change` (read-only, independent of the author), then a single memory update.

## Output

The active `.agent/tasks/<TASK-ID>.md` (spec of record) plus a verified diff — with green validation and one memory update.
