# Working on this repository

This repo IS the instruction kit — hold it to its own standards.

## Rules

1. `plugins/ritt-engineering/` is the canonical implementation for both Codex and Claude Code; skills must stay self-contained (see docs/SKILL_AUTHORING.md).
2. Every skill keeps valid frontmatter (`name` = directory, trigger-rich `description`) and a matching `agents/openai.yaml` invocation policy.
3. Never write upstream snapshot content into `plugins/` — porting is a manual, reviewed edit that also updates `upstream/mattpocock/CUSTOMIZATIONS.json` (see docs/UPSTREAM_POLICY.md).
4. Scripts must never delete user files; installers are copy-with-backup only.
5. After any change: `python3 scripts/validate_repo.py` must pass before claiming success. When manifests change, keep the version identical in both plugin.json files and the marketplace, and update CHANGELOG.md.
6. After adding/renaming a skill: re-run `scripts/link_skills.sh` and re-sync the skill table in README.md.
7. Do not claim results that were not verified.
