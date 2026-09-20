# Question Policy

Ask the questions that change the outcome — never the ones the repository already answers.

## Budget by risk

| Task profile | Budget |
| --- | --- |
| Trivial, reversible | 0–3 questions |
| Standard feature or fix | up to 10 |
| High-risk: migrations, security, data, infra, ambiguous goals | up to 20 |

## Rules

- Inspect the repository and project memory **before** asking anything.
- Ask in **one numbered batch**, grouped by theme (scope, constraints, acceptance, risks) — not a drip of one-at-a-time questions.
- Propose a sensible default per question so the user can reply "defaults except 3 and 7".
- Only ask questions that change the solution, the scope, or the acceptance criteria.
- Challenging the premise counts as clarification: if the approach looks wrong, say so in the batch.

## Closing states

Every clarification pass ends in exactly one:

- `READY` — proceed.
- `READY WITH ASSUMPTIONS` — list them; proceed only if accepted.
- `BLOCKED` — name what is missing and from whom.
