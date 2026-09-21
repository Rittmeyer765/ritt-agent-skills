# Changelog

## [0.5.2] - 2026-09-21

### Added

- docs/OPERATIONS.md "Permission resilience": Manual (`default`) as the stable mode when the Auto-Mode classifier is down, the `claude --permission-mode default` recovery command, a minimal read-only local allowlist, the max-one-retry DEGRADED policy, and the independent TCC/OneDrive procedure. `bypassPermissions` is prohibited.

### Changed

- Version 0.5.1 -> 0.5.2 (docs/config patch; no behavior change to skills).


## [0.5.1] - 2026-09-21

### Changed

- `graphify-map`: query logging disabled by default (`GRAPHIFY_QUERY_LOG_DISABLE=1`) and answers budget-capped (`graphify query … --budget ${GRAPHIFY_QUERY_BUDGET:-1500}`, validated 100..100000). Still refuses install/hook/mcp/serve/network/docs; `build` stays `extract <path> --code-only`. Self-test now asserts the exact argv (incl. `--budget`) and rejects a non-numeric budget.

### Added

- `docs/benchmarks/graphify-smoke.md` — A/B smoke result (OPTIONAL, not default; limitations recorded).
- `docs/OPERATIONS.md` — daily flow, occasional Graphify usage, validations, upstream review, and monthly-job manage/remove.


## [0.5.0] - 2026-09-20

### Added

- Agent Skills spec conformance in `validate_repo.py` (agentskills.io): `name` pattern/length matching the directory, `description` length, optional `compatibility`/`allowed-tools`, and a >500-line SKILL.md warning.
- Multi-source upstream: `check_upstream.py`/`import_upstream.py`/`accept_upstream.py` take `--source` (default `mattpocock`); `upstream/agent-skills-spec/` tracks the Agent Skills spec repo (Apache-2.0), review-first, nothing imported. `resolve_upstream_source` guards traversal/symlink/unknown sources.
- `graphify-map` skill (#13): manual, code-only adapter for Graphify; never installs it, never runs `graphify install`, never edits AGENTS.md/CLAUDE.md/hooks; outputs kept local.
- `docs/integrations/omniroute/`: inactive, opt-in gateway templates (loopback-only, hardened, no real secrets). `docs/INTEGRATION_MATRIX.md` and `docs/integrations/THIRD_PARTY_EVIDENCE.md`.
- Security regression now 7/7 (adds upstream-source guard); graphify adapter self-test in `validate_repo.py`.

### Changed

- Version 0.4.0 -> 0.5.0 across manifests. `EXPECTED_SKILLS` 12 -> 13.


## [0.4.0] - 2026-09-20

### Changed

- Analysis skills (`clarify-task`, `diagnose-systematically`, `research-and-reuse`, `validate-change`, `plan-change`, `review-change`) are now strictly read-only: they no longer write `.agent/` memory implicitly — they recommend the orchestrator persist.
- `project-memory` is the single writer of `.agent/` and manual-only (`disable-model-invocation` + `allow_implicit_invocation:false`).
- `implement-change` runs only when editing is authorized and no longer cascades validate/review/memory automatically.
- `research-plan-implement` no longer forces a commit per phase.
- README: `project-memory` moved to manual skills; `references/` marked as human doctrine (not runtime-loaded).

### Added

- `validate_repo.py`: per-skill `agents/openai.yaml` presence, invocation-policy coherence (Claude frontmatter ↔ Codex policy), explicit skill count test, repo-relative link checking, and upstream baseline/snapshot consistency.
- `accept_upstream.py`: refuses to accept a revision whose immutable snapshot manifest is absent.


## [0.3.0] - 2026-08-26

### Added

- `research-plan-implement` skill: RPI/SDD orchestration in three context-isolated phases (Research → Plan → Implement), with `.agent/PLANS.md` as the source of truth, intentional context compaction (~40–60%), research sub-agents, and visual plan review via plannotator.

## [0.2.1] - 2026-07-16

### Changed

- Per-project kit is now private-by-default: setup-project and install_project.py recommend `.git/info/exclude` (local-only ignore) instead of committing the kit; sharing with a team is an explicit opt-in.
- README rewritten in Spanish.

## [0.2.0] - 2026-07-16

### Added

- YAML frontmatter (`name`, `description`, invocation policy) on every skill — required for discovery in Claude Code and Codex.
- `agents/openai.yaml` per skill with explicit `allow_implicit_invocation` policy.
- Full skill bodies: adaptive question budgets, two-option planning, reuse-first research, validation ladder, security review checklist, project memory schema (append-only HISTORY / overwritten CONTEXT).
- `scripts/link_skills.sh` to symlink skills into `~/.claude/skills` and `~/.agents/skills`.
- Seeded upstream tracking: remote, tracked paths, customization map, and accepted baseline snapshot `e9fcdf9`.
- Frontmatter and version-sync checks in `validate_repo.py`.

### Fixed

- `install_project.py` no longer deletes the target directory with `--force`; it now copies file-by-file and backs up only conflicting files.
- `import_upstream.py` now verifies the checkout matches the requested revision and supports directory tracked paths.

### Changed

- Project kit memory consolidated under `.agent/` (`CONTEXT.md`, `HISTORY.md`, `PLANS.md`, `rules/`).
- Project AGENTS.md template rewritten as a compact contract with QUICK/STANDARD/DEEP/AUDIT modes.

## [0.1.0] - 2026-07-15

### Added

- Initial cross-compatible Codex and Claude Code plugin.
- Review-first upstream tracking.
- Adaptive clarification and validation workflows.
