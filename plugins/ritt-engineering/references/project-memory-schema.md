# Project Memory Schema (canonical v0.4)

Per-project agent memory lives in `.agent/`. Only the orchestrator writes it (skill `project-memory`), at milestones or handoff, never during AUDIT.

```
.agent/
├── CONTEXT.md            # current state, overwritten (≤60 lines / 8 KiB)
├── tasks/<TASK-ID>.md    # one file per task: goal, facts, decisions, plan, attempts, validation
├── history/YYYY-MM.md    # one line per milestone, monthly rotation
├── HANDOFF.md            # overwritten relay snapshot; links, does not duplicate
└── README.md            # the schema, source of truth in-project
```

## `.agent/CONTEXT.md` — overwritten snapshot
Only the current working state; superseded approaches are replaced. Sections: Estado actual, Decisiones activas (+ one-line why), Hechos verificados, punteros a tareas/ADR. No attempts, no logs.

## `.agent/tasks/<TASK-ID>.md` — one file per task (≤100 lines / 16 KiB)
Folds what used to be split across RESEARCH/PLANS: goal & acceptance, verified facts, decisions, plan/current step, attempts, validation, next action or blocker. Each attempt logs:
`attempt | hypothesis | action_fingerprint | input_changed | result | evidence | next`
Anti-loop: no repeated fingerprint without changing hypothesis/input/env; ≤2 attempts/hypothesis; ≤3 without observable progress; then a discriminating test, a question, or `BLOCKED`.

## `.agent/history/YYYY-MM.md` — append-only, monthly
One line per milestone (not per command): `- YYYY-MM-DD | intent: … | cmd: … | result: OK|KO — …`. `KO` entries are the most valuable. Not loaded by default; queried by task_id/error/fingerprint.

## `.agent/HANDOFF.md`
Overwritten snapshot that links CONTEXT + the active task; never duplicates them. Generated only on explicit request.

## Legacy (migration only)
`HISTORY.md`, `PLANS.md`, `RESEARCH.md` are the old format. Recognize them to migrate, but **no new writes** create them — use `history/YYYY-MM.md` and `tasks/<id>.md`. Promote heavy decisions to `docs/adr/`.
