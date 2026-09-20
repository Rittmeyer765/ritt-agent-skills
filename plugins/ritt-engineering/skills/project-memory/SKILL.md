---
name: project-memory
description: Maintain the project's agent memory under .agent/ - a monthly history/ log, per-task task files, an overwritten CONTEXT.md, and HANDOFF.md. Use after a significant milestone or failure, before ending a session, or when the user asks to save or recall project context.
disable-model-invocation: true
---

> **Single writer, manual-only.** This is the ONLY skill that writes `.agent/` memory, and it runs only when the orchestrator (or the user) invokes it explicitly — never implicitly from an analysis, review, or AUDIT pass.

Canonical schema (see references/project-memory-schema.md). Never recommend new writes to legacy `HISTORY.md`, `PLANS.md` or `RESEARCH.md`.

## `.agent/CONTEXT.md` — overwritten snapshot
Current working state only. Sections: Estado actual · Decisiones activas (+ one-line why) · Hechos verificados (source/date) · punteros a `tasks/<id>.md` y `docs/adr/`. Keep under ~60 lines / 8 KiB. Replace superseded entries; if a "why" stops being true, rewrite it. No attempts, no logs, no secrets.

## `.agent/tasks/<TASK-ID>.md` — one per task (≤100 lines / 16 KiB)
Goal & acceptance, verified facts, decisions, plan/current step, attempts, validation, next action or blocker. Each attempt:
`attempt | hypothesis | action_fingerprint | input_changed | result | evidence | next`
Anti-loop semantics (per table): a `action_fingerprint` may repeat ONLY when `input_changed` is truthy on the repeat (you changed inputs/env/approach); a hypothesis backs at most 2 attempts (a 3rd is a loop — reformulate under a new name); more than 3 consecutive non-`OK` results is a loop. An OK without observed evidence is recorded `UNVERIFIED`.

**Enforcement (prospective + atomic).** Never write the row first and revert. Append through the guard so it evaluates *file + candidate* BEFORE writing:

```
GUARD=${RITT_KIT:-$HOME/.claude/ritt-agent-skills}/scripts/check_task_loop.py   # or resolve from the kit that provides this skill
python3 "$GUARD" .agent/tasks/<id>.md --candidate '| n | hyp | fp | input_changed | result | evidence | next |' --append
```

Exit 0 = allowed and appended atomically; exit 1 = `ANTI-LOOP BLOCK` (nothing written — change hypothesis/input or close `BLOCKED`); exit 2 = fatal usage/invalid file (nothing written — report). This runs only here (memory written at a milestone), not on every session.

## `.agent/history/YYYY-MM.md` — append-only, monthly
One line per milestone (not per command): `- YYYY-MM-DD | intent: … | cmd: … | result: OK|KO — …`. Never rewrite old entries; `KO` are the most valuable. Not loaded by default.

## `.agent/HANDOFF.md`
Overwritten snapshot linking CONTEXT + the active task; does not duplicate them.

## Discipline
- Write at milestones or failures worth keeping, at handoff, or on explicit request — not one giant end-of-session dump.
- Heavy architectural decisions graduate to `docs/adr/` (link from CONTEXT).
- Shared with humans: plain language, no agent jargon, secrets never.
