# Operations

Final architecture: **Ponytail** trims output by default · **skills** load context on demand ·
**small agents** research/implement/review · **`.agent/`** holds operational memory ·
**Graphify** is manual/optional for complex cross-file relationships · **OmniRoute** is prepared but inactive.

## 1. Everyday work
1. Open the project.
2. Describe the task.
3. Let the orchestrator pick the skill.
4. Use small agents to research, implement, and review.
5. Save stable context in `.agent/`.

## 2. Graphify (occasional, manual — not linked, not on global PATH)
```bash
GRAPHIFY_QUERY_LOG_DISABLE=1 PATH="$HOME/.graphify-venv/bin:$PATH" \
  "$HOME/.claude/ritt-agent-skills/plugins/ritt-engineering/skills/graphify-map/scripts/graphify_map.sh" build .
GRAPHIFY_QUERY_LOG_DISABLE=1 PATH="$HOME/.graphify-venv/bin:$PATH" \
  "$HOME/.claude/ritt-agent-skills/plugins/ritt-engineering/skills/graphify-map/scripts/graphify_map.sh" \
  query "which components use this service?"
```
Queries are budget-capped (`--budget ${GRAPHIFY_QUERY_BUDGET:-1500}`). `install`/`hook`/`mcp`/`serve`/docs/network are refused. Outputs (`graphify-out/`, `graph.json`) stay local — keep them out of git/context.

## 3. Validate the kit
```bash
python3 scripts/test_security.py
python3 scripts/validate_repo.py
claude plugin validate . --strict
```

## 4. Upstream review (monthly job + manual)
```bash
python3 scripts/check_upstream.py --source mattpocock
python3 scripts/check_upstream.py --source agent-skills-spec
```
Monthly LaunchAgent `com.rittmeyer.upstream-check` runs the above (read-only) on day 1 ~09:17; log at
`reports/upstream/monthly-cron.log` (bounded). It only reports — never imports/accepts/installs.
- Check:   `launchctl list | grep upstream-check`
- Remove:  `launchctl unload "$HOME/Library/LaunchAgents/com.rittmeyer.upstream-check.plist" && rm "$HOME/Library/LaunchAgents/com.rittmeyer.upstream-check.plist" "$HOME/.claude/ritt-upstream-check.sh"`

## 5. Permission resilience (Auto vs Manual) — v0.5.2
`auto` mode routes actions through a background classifier; if that classifier is down it can block
even safe Bash. `default` (Manual) asks for approval when an unknown action appears, without depending
on the classifier — it is the official fallback.

- **Recovery (per session):** `claude --permission-mode default`. Never use `--permission-mode bypassPermissions`.
- **Stable config:** `~/.claude/settings.json` → `permissions.defaultMode: "default"`.
- **Minimal local allowlist** (per project, in `.claude/settings.local.json`, local & untracked):
  `Bash(gh auth status)`, `Bash(gh pr view *)`, `Bash(gh pr diff *)`, `Bash(gh pr list *)`,
  `Bash(gh pr checks *)`, `Agent(code-explorer)`. Do NOT allow `Bash(*)`, `gh *`, `Agent(*)`, or
  preauthorize `gh api`/`pr merge`/`pr edit`/`pr close`/`git push`/writes/deletes — those keep asking.
- **DEGRADED policy:** if the classifier or subagents are unavailable — retry ONCE, no loops; mark
  `DEGRADED`; continue with Read/Grep/Glob; never simulate subagent results; recommend the recovery
  command if Bash is needed; resume delegation when `Agent` returns.
- **TCC / OneDrive (independent):** an "Operation not permitted" on the vault is unrelated to the
  classifier. Options: keep using Read/Write tools; or grant Terminal/Claude Code access to
  Documents/OneDrive in System Settings → Privacy & Security → Files and Folders; Full Disk Access
  only if the specific grant fails.
