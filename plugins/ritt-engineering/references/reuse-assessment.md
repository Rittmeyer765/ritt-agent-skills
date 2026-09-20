# Reuse Assessment

Before building, exhaust these in order: this repository → organization libraries and sibling repos → well-maintained ecosystem packages.

Score each candidate:

1. **Fit** — covers the actual need, or merely looks similar? Missing 20% can cost more than building.
2. **Maintenance** — recent releases, responsive maintainers, handled security advisories, bus factor.
3. **License** — compatible with the project; verify explicitly for work code.
4. **Adoption cost** — integration effort, transitive dependencies, upgrade path, team familiarity.
5. **Security surface** — new attack surface, supply-chain exposure, data it touches.

Verdicts: **REUSE** (as-is) / **ADAPT** (wrap or extend — state what changes) / **BUILD** (state why each candidate fails).

Record the verdict and one-line rationale in `.agent/CONTEXT.md`. New production dependencies always need explicit user approval before adoption.
