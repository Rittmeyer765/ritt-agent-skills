---
name: research-and-reuse
description: Before building anything new, check whether it already exists and decide reuse vs adapt vs build. Use when a task asks for a new component, script, service, or tool, when a plan would introduce a new dependency or abstraction, or when the user asks whether something is already solved.
---

Do not reinvent the wheel. The cheapest, safest code is the code you did not write.

## Search order

1. **This repository** — existing modules, helpers, scripts, patterns. Search by behavior, not just by name.
2. **The organization** — internal libraries, shared packages, sibling repos, templates the team already trusts.
3. **The ecosystem** — well-maintained open source. Judge against primary sources (official docs, source code, release notes), not blog posts.

## Assess each candidate

- Does it actually cover the need, or only look similar?
- Maintenance: recent releases, responsive issues, security advisories handled.
- License compatible with the project (for work code, verify explicitly).
- Cost of adoption vs cost of building: integration effort, transitive dependencies, upgrade path.
- Security surface: what new attack surface or supply-chain exposure does it add?

## Decide and record

Produce a short verdict: **REUSE** (use as-is), **ADAPT** (wrap or extend, state what changes), or **BUILD** (nothing fits, state why the candidates fail). Label claims per the evidence rules: `VERIFIED` / `INFERENCE` / `HYPOTHESIS` / `UNVERIFIED`.

A new production dependency always requires explicit user approval before it is added. This skill is read-only: it does not write memory. Recommend that the orchestrator record the verdict and its one-line rationale in `.agent/CONTEXT.md` so the next session does not repeat the research — do not write it yourself.
