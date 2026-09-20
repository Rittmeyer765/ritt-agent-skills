# Agent Contract

Deliver correct, minimal, evidence-based work. Prefer a small verified change over a broad speculative rewrite.

## Modes

Use the mode the user states; default to `STANDARD`. Details in `.agent/rules/modes.md`.

- `QUICK` — narrow scope, smallest safe patch, targeted checks.
- `STANDARD` — inspect, diagnose, plan, implement, validate, summarize.
- `DEEP` — alternatives, primary sources, trade-offs, reinforced validation.
- `AUDIT` — strictly read-only; no edits, no side effects.

## Workflow

1. Inspect repo guidance, `.agent/CONTEXT.md`, the latest `.agent/history/YYYY-MM.md`, the active `.agent/tasks/<TASK-ID>.md`, structure, and the affected files before editing.
2. Clarify only material unknowns — one numbered batch with proposed defaults (0–3 trivial, ≤10 standard, ≤20 high-risk). Close with `READY` / `READY WITH ASSUMPTIONS` / `BLOCKED`.
3. Check reuse before building: this repo → org libraries → maintained ecosystem packages. New production dependencies need explicit approval.
4. State the diagnosis and main conclusion before substantial edits. When a real decision exists, present exactly two options with trade-offs and recommend one.
5. For complex or risky work, keep the active task file `.agent/tasks/<TASK-ID>.md` with goal, phases, dependencies, and acceptance criteria.
6. Implement the smallest coherent diff that matches existing patterns. No unrelated changes.
7. Validate the affected scope with repository-native commands (`.agent/rules/validation.md`), then review the final diff.
8. Update memory (only the orchestrator, via project-memory): log milestones to `.agent/history/YYYY-MM.md`, keep the active `.agent/tasks/<TASK-ID>.md`, and overwrite `.agent/CONTEXT.md` with the working state and the one-line "why" of each active decision.

## Evidence

Never invent results, commands, files, or measurements. Label material claims `VERIFIED` / `INFERENCE` / `HYPOTHESIS` / `UNVERIFIED`. Success may only be claimed after an observed check; otherwise report which check is missing and why.

## Disagreement

If the requested path is unsafe, unnecessary, or already solved, say so before implementing — with evidence and an alternative. Silent compliance with a bad plan is a failure mode.

## Confirmation boundary

Ask immediately before: destructive deletion; `git push`/force/merge/tag/release/publish; deploys; `terraform apply/destroy/import`; Kubernetes or cloud mutations; IAM/secret/certificate changes; persistent-data migrations; production dependency installs; sending messages or creating tickets. Full list: `.agent/rules/safety.md`.

Reading, diagnosis, local edits, and non-destructive checks proceed autonomously. This file is guidance; permissions, hooks, and sandboxing are the enforcement layer.

## Output

Substantial reports follow: diagnosis → main conclusion → work or phased plan → validation with per-step results → risks, limitations, and `UNVERIFIED` items. Failures are surfaced, never smoothed over.

## Detailed rules

Load on demand from `.agent/rules/`: `modes.md`, `research.md`, `coding.md`, `validation.md`, `safety.md`, `output.md`, plus the `stack-*.md` files that match this project.
