# Skill Authoring

## Anatomy

```
skills/<name>/
├── SKILL.md            # frontmatter + body
└── agents/openai.yaml  # Codex metadata + invocation policy
```

Frontmatter requirements:

- `name` — must equal the directory name.
- `description` — one or two sentences: what it does AND when to trigger it. This is the only text the model sees before deciding to load the skill, so put the trigger conditions here ("Use when…").
- `disable-model-invocation: true` — for user-only skills (side effects, network, session-compaction). Mirror it as `allow_implicit_invocation: false` in `agents/openai.yaml`.

## Writing rules

1. Self-contained: the body must work without reading `references/` (symlinked skills can't resolve relative paths reliably). Summarize the doctrine inline; references are the long-form version.
2. Open with the principle, then the procedure as a short numbered list, then the expected output.
3. Concrete over abstract: exact file paths (`.agent/CONTEXT.md`), exact formats, exact commands.
4. State the hard rules ("never X") explicitly — they are the reason the skill exists.
5. Keep it under ~40 lines of body; if it grows, the skill is doing two jobs.

## After any change

- `python3 scripts/validate_repo.py`
- `claude plugin validate . --strict` if available
- Bump the version in both plugin.json files and the marketplace (validate_repo enforces sync), and note the change in CHANGELOG.md.
- If the skill adapts upstream material, update `upstream/mattpocock/CUSTOMIZATIONS.json` and, if needed, `TRACKED.json`.
- Re-run `scripts/link_skills.sh` after adding or renaming a skill.
