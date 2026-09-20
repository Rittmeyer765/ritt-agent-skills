---
name: plan-change
description: Produce a phased, dependency-ordered implementation plan with acceptance criteria, and present exactly two viable options with a recommendation. Use before implementing any non-trivial change, after clarify-task, or when the user asks for a plan, roadmap, or approach comparison.
---

A plan is a contract: it states what will be true when the work is done and how that will be proven.

## Procedure

1. **Start from evidence.** Base the plan on the real state of the repository (and `.agent/CONTEXT.md` if present), not on the request's description of it. State the main diagnosis first.
2. **Present exactly two realistic options** when a genuine decision exists — not one, not five. For each: approach, cost, risks, and what it forecloses. Recommend one and say why. If no real alternative exists, say so instead of inventing a strawman.
3. **Phase the work by dependency.** Prerequisites first (data/contracts before UI, schema before queries). Each phase gets:
   - concrete steps,
   - acceptance criteria (observable, testable),
   - the validation that proves the phase, per the validation ladder.
4. **Protect what works.** Call out explicitly what must NOT change: public contracts, passing tests, unrelated modules.
5. **Name the risks** and the rollback path for anything hard to reverse.

## Output

Return the plan in this shape. Persisting is a separate, explicit step: only when the user or the orchestrator asks, write it into the active `.agent/tasks/<TASK-ID>.md` (or the project's planning convention) so it survives the session. Do not persist implicitly during a read-only planning pass.

- Diagnosis and main conclusion
- Option A / Option B with trade-offs, and the recommendation
- Phases with steps, acceptance criteria, and validation
- Out of scope / must not change
- Risks and rollback

Keep it short enough to execute; if a phase needs a page of prose, split it. Do not start implementing until the user picks an option (or the recommendation is accepted under `READY WITH ASSUMPTIONS`).
