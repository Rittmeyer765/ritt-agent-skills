# Output

Substantial reports follow this order:

1. **Diagnosis** — the real state, evidence-labeled.
2. **Main conclusion** — the one thing that matters, first.
3. **Work** — what changed (files, scope) or the phased plan with acceptance criteria.
4. **Validation** — per-step results: `PASSED` / `FAILED` / `PARTIAL` / `NOT RUN` (reason) / `NOT APPLICABLE`.
5. **Risks and limits** — residual risks, `UNVERIFIED` items, what was deliberately not done.

Rules:

- Distinguish observed results from expected results; failures are reported with their output, never smoothed over.
- Concise while executing; complete in the final report.
- Two options + recommendation when a real decision exists — not one, not five.
- Plain language a teammate can skim; no invented shorthand.
