@AGENTS.md

# Claude Code Additions

- Use Plan mode before editing for cross-service, architectural, migration, or security-sensitive work.
- Load skills from the ritt-engineering plugin when their description matches the task; do not preload them.
- Treat this file as behavioral context; `.claude/settings.json` permissions and `PreToolUse` hooks are the hard boundary.
- Project-specific rules belong in focused files under `.agent/rules/` or nested CLAUDE.md files, not in this file.
- Before claiming completion, review the final diff and state which checks actually passed.
