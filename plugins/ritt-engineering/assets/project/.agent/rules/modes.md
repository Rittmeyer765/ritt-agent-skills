# Modes

State the mode at the start of a task (`MODE: DEEP`). Default is `STANDARD`.

## QUICK
Small, reversible change. 0–3 clarifying questions. Smallest safe patch. Validation: static checks plus the nearest targeted test. No refactors.

## STANDARD
Default. Inspect → diagnose → plan (two options when a real decision exists) → implement → validate affected scope → report. Up to 10 clarifying questions.

## DEEP
Broad investigation before acting: primary sources, alternatives with trade-offs, architecture impact. Up to 20 clarifying questions. Validation climbs to build/smoke. Plan maintained in the active `.agent/tasks/<TASK-ID>.md`.

## AUDIT
Strictly read-only. No file edits, no state mutations, no external side effects. Output is a findings report with evidence labels and severity.

Escalate, don't drift: if a QUICK task reveals structural problems, stop and propose switching modes instead of silently expanding scope.
