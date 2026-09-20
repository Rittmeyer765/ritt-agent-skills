---
name: implement-change
description: Apply an agreed change as the smallest coherent, verifiable diff that follows the repository's existing patterns. Use when moving from an approved plan to code, or for any edit beyond a trivial one-liner.
---

Implement the plan — nothing more. Every line outside the agreed scope is a defect, not a bonus.

**Only run when the request authorizes editing.** If the task is analysis, diagnosis, review, or audit, stop and defer to the orchestrator — do not edit on your own initiative. You are the single writer of your scope; do not spawn subagents.

## Rules

1. **Follow the accepted plan.** If reality contradicts it mid-flight, stop, say what changed, and adjust the plan before continuing — do not silently improvise.
2. **Smallest coherent diff.** Precise edits over rewrites. No drive-by refactors, renames, or cleanup of unrelated code.
3. **Match the codebase.** Existing naming, style, error handling, comment density, and abstractions win over personal preference. Reuse before creating (see research-and-reuse).
4. **Secure by default.** No secrets in code or logs, validate external input, parameterized queries, least privilege, safe defaults. If the change touches auth, secrets, or data boundaries, flag it for review-change explicitly.
5. **No new production dependency** without a reuse assessment and explicit user approval.
6. **Work incrementally.** Keep the tree buildable between steps; validate each phase before starting the next (validate-change).
7. **Never bypass safeguards** — do not weaken tests, suppress failing checks, or hide errors to get to green.

## After the change

- Review your own diff before reporting: unrelated files, leftover debug code, secrets, generated artifacts.
- Do not run validate-change, review-change and project-memory as an automatic cascade. Report what changed and hand back to the orchestrator, which decides — exactly once — when to validate, review, and persist memory.
- Report honestly: what changed, what was validated and how, what remains `UNVERIFIED`.
