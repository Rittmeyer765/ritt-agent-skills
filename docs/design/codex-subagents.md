# Codex subagents — design notes (NOT active in this environment)

Reference for when/if Codex custom subagents are enabled. Kept out of the always-loaded
global so a future Codex update can't leave an obsolete explanation loaded every session.

## Verified for codex-cli 0.144.1 (empirical)
- A flat `[agents] enabled=… max_concurrent_threads_per_session=…` block is INVALID and breaks
  config load: `invalid type: boolean true, expected struct AgentRoleToml in 'agents'`.
- Multi-agent concurrency/tuning lives under the EXPERIMENTAL feature flag:
  `features.multi_agent_v2.*` (e.g. `max_concurrent_threads_per_session`).
- Custom roles are a map: `[agents.<name>]` = `AgentRoleToml` (a 3-field struct).
- `gpt-5.6-luna` is an accepted model (models_cache.json).

## Still UNVERIFIED by safe means
- Exact fields of `AgentRoleToml` and the home of `default_subagent_model`/`interrupt_message`.
  Validate with `codex exec --strict-config` in an isolated `CODEX_HOME` before applying anything.

## Gate before applying
Backup config → validate in a temp `CODEX_HOME` with `--strict-config`/`codex doctor` →
minimal change → confirm startup → restore on failure. Draft (not applied) lives in
`~/.claude/agents-migration-staging/codex/`.
