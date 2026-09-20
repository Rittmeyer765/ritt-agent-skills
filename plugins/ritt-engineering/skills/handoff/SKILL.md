---
name: handoff
description: Compact the current session into a handoff so another agent or person can continue without re-discovering anything.
disable-model-invocation: true
---

Write a handoff that lets a fresh agent continue in under five minutes of reading.

## Before writing

Update project memory first (project-memory skill): log pending milestones to `.agent/history/YYYY-MM.md`, refresh the active `.agent/tasks/<TASK-ID>.md`, and refresh `.agent/CONTEXT.md`. The handoff references memory; it does not replace it.

## Structure

1. **Estado** — what is done and `VERIFIED`, what is done but `UNVERIFIED`, what is in progress.
2. **Pendiente** — remaining work in dependency order, with acceptance criteria.
3. **Riesgos y trampas** — what failed before (link HISTORY entries), fragile areas, things that look wrong but are intentional (link the "why" in CONTEXT.md).
4. **Validación** — exactly which checks passed, which were not run and why.
5. **Prompt sugerido** — a ready-to-paste prompt for the next agent: goal, constraints, first action, and which skills to invoke.

## Rules

- Do not duplicate what already lives in specs, plans, ADRs, diffs, or memory files — link or reference by path instead.
- Save the handoff to `.agent/HANDOFF.md` (overwrite the previous one; history stays in `history/YYYY-MM.md`).
- No secrets, tokens, or credentials — ever.
