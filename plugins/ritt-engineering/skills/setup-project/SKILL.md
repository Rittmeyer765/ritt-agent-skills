---
name: setup-project
description: Install the agent instruction kit (AGENTS.md, CLAUDE.md, rules, and memory files) into the current project and adapt it to the project's stack.
disable-model-invocation: true
---

Bootstrap a repository so every future agent session starts with the same contract and memory.

## Procedure

1. **Inspect first.** If the project already has AGENTS.md, CLAUDE.md, or `.agent/`, summarize what exists and STOP for the user's decision — never overwrite silently.
2. **Install the kit** from this plugin's `assets/project/` (via `scripts/install_project.py <target>` when working inside ritt-agent-skills, or by copying the files). Without `--force` the installer refuses on any conflict; `--force` backs conflicting files up to `.agent-kit-backup/<timestamp>/` first.
3. **Adapt to the stack.** Detect the project's languages, frameworks, and build system (Bazel, npm, go.mod, pyproject…). Keep only the relevant `.agent/rules/stack-*.md` files and fill in the project's real commands (test, lint, build) in `.agent/rules/validation.md`.
4. **Seed the memory.** Write an initial `.agent/CONTEXT.md` (current state of the project in a few lines) and the first `.agent/history/YYYY-MM.md` entry recording the kit installation. Use the canonical schema (`CONTEXT.md`, `tasks/`, `history/`, `HANDOFF.md`); never seed legacy `HISTORY.md`/`PLANS.md`.
5. **Choose visibility (default: private).** Unless the user explicitly wants to share the kit with their team, add the kit paths (`AGENTS.md`, `CLAUDE.md`, `.agent/`, `.agent-kit-backup/`) to the repo's `.git/info/exclude` — a local-only ignore that is never committed or pushed. Never add them to `.gitignore` (that file is shared) and never commit the kit without the user's explicit choice.
6. **Verify.** List the installed files, confirm AGENTS.md is under ~100 lines, and confirm `git status` shows no kit files when private mode was chosen.

## Rules

- Never delete or move existing project files.
- Ask before installing into a repository with uncommitted changes.
- The kit is behavioral guidance; recommend the user also configure tool-level permissions/hooks for hard enforcement.
