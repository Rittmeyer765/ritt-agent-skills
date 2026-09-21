<!-- STATUS: DRAFT · NOT ACTIVE -->

# OmniRoute security checklist (all must hold before starting)

- [ ] Repo/release verified: `diegosouzapw/OmniRoute`, pinned tag (e.g. `v3.8.51`) + image `@sha256:` digest. No `latest`.
- [ ] Bind **127.0.0.1 only** (never `0.0.0.0`, never a published LAN port).
- [ ] `JWT_SECRET`, `API_KEY_SECRET`, `STORAGE_ENCRYPTION_KEY` all set to fresh random values.
      (If `STORAGE_ENCRYPTION_KEY` is unset, OmniRoute can store credentials in **plaintext**.)
- [ ] No real secrets committed anywhere; `.env` is git-ignored and local.
- [ ] Disabled by default: MCP, A2A, webhooks, cloud sync, MITM, secondary services, remote access.
- [ ] Prompt logging off (or minimal retention).
- [ ] Provider **allowlist** only — no wildcard providers.
- [ ] Direct `claude`/`codex` config preserved; gateway used only via opt-in wrappers.
- [ ] Not used with corporate repositories without explicit authorization.
- [ ] Reconciled variable names/flags against the pinned release's own `.env.selfhost.example` + `SECURITY.md`.
