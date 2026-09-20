# Architecture

Three layers, deliberately isolated so an upstream update can never touch a customized skill:

```
plugins/ritt-engineering/    ← the canonical implementation (skills, references, project kit)
upstream/mattpocock/         ← read-only inputs: baseline lock, tracked paths, immutable snapshots
reports/upstream/            ← generated review reports (gitignored)
```

## Plugin layout

- `skills/<name>/SKILL.md` — one skill per directory; YAML frontmatter (`name`, `description`, optional `disable-model-invocation`) drives discovery in Claude Code.
- `skills/<name>/agents/openai.yaml` — Codex interface metadata and `allow_implicit_invocation` policy (mirrors the frontmatter decision).
- `references/` — shared doctrine the skills summarize inline (skills stay self-contained so they work when symlinked individually).
- `assets/project/` — the per-project instruction kit that `install_project.py` copies: `AGENTS.md`, `CLAUDE.md`, `.agent/rules/`, `.agent/{CONTEXT,HISTORY,PLANS}.md`, `docs/adr/`.

## Distribution paths

1. **Claude Code plugin** via `.claude-plugin/marketplace.json` (single-plugin marketplace).
2. **Symlinks** via `scripts/link_skills.sh` into `~/.claude/skills` and `~/.agents/skills` — works for both harnesses, and a `git pull` updates everything.

## Upstream flow

`check_upstream.py` (read-only, exit code signals state) → `import_upstream.py` (immutable snapshot per SHA with hashed manifest) → `compare_upstream.py` (diff report) → human review guided by `CUSTOMIZATIONS.json` → `accept_upstream.py` (explicit, double-confirmed baseline move). Nothing in this pipeline writes into `plugins/`.

## Invariants

- Every skill has frontmatter whose `name` matches its directory (enforced by `validate_repo.py`).
- Plugin version is identical across both plugin.json files and the marketplace (enforced).
- Scripts never delete user files; installs are copy-with-backup only.
