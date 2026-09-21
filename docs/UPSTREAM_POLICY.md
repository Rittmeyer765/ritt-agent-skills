# Upstream Policy

Upstream is [mattpocock/skills](https://github.com/mattpocock/skills). It is an idea source, not a dependency.

## Rules

1. **Never auto-apply.** No script, hook, or agent may write upstream content into `plugins/`. Ever.
2. **Check = report.** `check_upstream.py` only compares SHAs and writes a report. Exit codes: 0 up-to-date, 1 update available, 2 no baseline, 3 unverifiable.
3. **Snapshots are immutable.** One directory per SHA under `upstream/mattpocock/snapshots/`, with a hashed manifest. Re-importing an existing SHA is a no-op.
4. **Review before accept.** An update is reviewed via `compare_upstream.py` + the `CUSTOMIZATIONS.json` map (which local skill adapts which upstream file). Only after human review does `accept_upstream.py` move the baseline — and it requires the SHA typed twice.
5. **Porting is normal work.** Bringing an upstream improvement into a local skill goes through plan-change → implement-change → validate_repo, and updates `CUSTOMIZATIONS.json`.
6. **Track deliberately.** `TRACKED.json` lists only paths we actually adapted or watch; tracking everything would make every upstream commit noise.

## Cadence

Run `/check-upstream` (or `python3 scripts/check_upstream.py`) when convenient — monthly is plenty. There is no automation that pulls; that is the point.

## Multiple sources (v0.5+)

The upstream tooling is source-parameterized: `check_upstream.py` / `import_upstream.py` /
`accept_upstream.py` take `--source <name>` (default `mattpocock`). Each source is a directory
under `upstream/<name>/` with its own `LOCK.json` / `TRACKED.json` / `CUSTOMIZATIONS.json`. Source
names are validated (`^[a-z0-9][a-z0-9-]*$`, must resolve inside `upstream/`, no symlinks, must exist).

Tracked sources:
- `mattpocock` — idea source for the engineering skills (MIT); baseline snapshot accepted.
- `agent-skills-spec` — the canonical Agent Skills spec ([agentskills.io](https://agentskills.io/specification), Apache-2.0). Tracked for spec drift; `validate_repo.py` mirrors its SKILL.md frontmatter rules. No baseline accepted, nothing imported. `anthropics/skills` is examples-only and **unlicensed** — do NOT copy.

## Agent Skills conformance & per-tool extensions

`validate_repo.py` enforces **Agent Skills core conformance**: `name` 1-64
`^[a-z0-9]+(?:-[a-z0-9]+)*$` matching its directory, `description` 1-1024, and the optional
`compatibility`/`allowed-tools` fields when present, plus a >500-line SKILL.md warning. This is a
lightweight hand-parser check — it does **not** fully validate nested `metadata` maps or deep YAML.
For full, authoritative validation, run the official validator (optional, not bundled/installed):
`skills-ref validate ./skill` from [agentskills/agentskills](https://github.com/agentskills/agentskills).
Note: `claude plugin validate . --strict` validates the Claude Code **plugin/marketplace manifest**,
not the Agent Skills spec — they are complementary, not equivalent.

`disable-model-invocation` (Claude Code) and `agents/openai.yaml` (Codex) are per-tool extensions
layered on top of the spec, not part of it.
