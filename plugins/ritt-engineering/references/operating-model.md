# Operating Model

The review-first engineering loop every skill in this plugin plugs into:

1. **Inspect** the repository and `.agent/CONTEXT.md` — establish the real state before acting.
2. **Clarify** only material unknowns (`clarify-task`): adaptive question budget, one batch, explicit READY state.
3. **Reuse before building** (`research-and-reuse`): repo → org → ecosystem.
4. **Diagnose before fixing** (`diagnose-systematically`): root cause vs symptoms, labeled evidence.
5. **Plan** with phases, acceptance criteria, and exactly two options plus a recommendation (`plan-change`).
6. **Implement** the smallest coherent diff that matches repo patterns (`implement-change`).
7. **Validate** up the ladder as far as the risk demands (`validate-change`).
8. **Review** the diff for correctness, security, maintainability (`review-change`).
9. **Remember**: append to HISTORY, overwrite CONTEXT (`project-memory`); hand off cleanly (`handoff`).

Cross-cutting rules:

- **Disagree early.** If the requested path is unsafe, unnecessary, or already solved, say so before doing it — with evidence.
- **Evidence over confidence.** Claims carry certainty labels (see certainty-labels.md). No unverified success reports.
- **Confirm before impact.** Destructive or externally visible actions require explicit approval (see safety-boundaries.md).
- **Guidance is not enforcement.** These files shape behavior; permissions, hooks, and sandboxing are the hard boundary.
