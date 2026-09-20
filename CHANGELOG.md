# Changelog

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
