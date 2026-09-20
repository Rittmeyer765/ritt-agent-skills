# Coding

- Smallest coherent diff. Precise edits over rewrites; no drive-by refactors, renames, or unrelated cleanup.
- Match the codebase: naming, style, error handling, comment density, existing abstractions. Local consistency beats personal preference.
- Secure by default: validate external input, parameterized queries, least privilege, safe defaults, no secrets in code/config/logs/fixtures.
- Public contracts (APIs, schemas, CLI flags, exported symbols) change only when the task requires it, and then explicitly and documented.
- New dependencies only after a reuse assessment and explicit approval; pin and lock per the repo's convention.
- Keep the tree buildable between steps. Never suppress errors, weaken tests, or bypass safeguards to get to green.
- Comments state constraints the code can't express — not narration of the change.
