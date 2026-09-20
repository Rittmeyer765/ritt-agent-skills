---
name: validate-change
description: Prove a change works by climbing an adaptive validation ladder, with an explicit result per step. Use after implementing any change, before claiming success, before a handoff, or when the user asks whether something really works.
---

A change without an observed check is a hypothesis, not a result. Never claim success that was not observed.

## Discover, don't assume

Use the repository's own commands: manifests, `Makefile`, `package.json` scripts, CI config, Bazel targets. Do not assume a tool is installed; if a needed check cannot run, report it as `NOT RUN` with the reason — do not substitute a weaker check silently.

## The ladder (climb as high as the risk demands)

1. **Static** — format, lint, type check on the affected files (only tools the repo already configures).
2. **Targeted tests** — the module or Bazel targets the change touches (`bazel test //affected/...`).
3. **Integration boundary** — exercise the seams that changed: API↔consumer, service↔DB, component↔API, rule↔artifact.
4. **Build** — the affected artifact: package, binary, bundle, Bazel target, Docker image.
5. **Smoke** — run the real behavior in a safe environment when the change is user-visible or operational.
6. **Broad suite** — only for shared contracts or cross-cutting changes; say why it was or wasn't run.

QUICK mode stops at 1–2 unless something fails; migrations, security, infra, and shared contracts must reach 4–6. For infrastructure: `fmt`/`validate`/`plan` only — never `apply` as validation.

## Report

One line per step: `PASSED` / `FAILED` (with output) / `PARTIAL` / `NOT RUN` (with reason) / `NOT APPLICABLE`. Distinguish observed results from expected ones. A `FAILED` step is a finding to report, never something to hide or bypass. This skill is read-only: it does not write memory. Report the outcome to the orchestrator, which records it in `.agent/history/YYYY-MM.md`.
