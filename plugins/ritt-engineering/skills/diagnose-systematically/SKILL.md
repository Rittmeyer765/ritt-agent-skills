---
name: diagnose-systematically
description: Find the root cause of a bug or failure through evidence, separating cause from symptoms before touching any code. Use when something fails, behaves unexpectedly, or a fix attempt did not work — before proposing or applying a fix.
---

No fix before diagnosis. A patch aimed at a symptom creates two bugs: the original one and the illusion that it is gone.

## Procedure

1. **Reproduce or precisely characterize** the failure: exact command, input, environment, full error output. If it cannot be reproduced, say so — that changes everything downstream.
2. **Check the memory first.** The latest `.agent/history/YYYY-MM.md` and the active `.agent/tasks/<TASK-ID>.md` may show this was attempted before and how it failed; `.agent/CONTEXT.md` may explain why the current design is the way it is.
3. **Collect evidence before opinions:** logs, stack traces, recent diffs (`git log`/`git diff`), config, versions. Every claim gets a label:
   - `VERIFIED` — directly observed (output, code, primary docs).
   - `INFERENCE` — follows from evidence, not directly seen.
   - `HYPOTHESIS` — plausible, needs a test.
   - `UNVERIFIED` — could not check.
4. **Separate the root cause from symptoms and secondary issues.** List them explicitly; fix only the root cause in this pass, file the rest as follow-ups.
5. **Test hypotheses cheapest-first, one variable at a time.** Predict what you expect to observe before running each probe; a probe that cannot fail teaches nothing.
6. **Stop when the cause is `VERIFIED`** — or present the top 2 hypotheses with the discriminating test for each and let the user choose where to invest.

## Output

Diagnosis (root cause with its evidence label), symptoms explained by it, secondary findings, and the minimal fix proposal. This skill is read-only: it does not write memory. Recommend that the orchestrator record failed attempts in `.agent/history/YYYY-MM.md` (or the active task file) so nobody repeats them — do not write them yourself.
