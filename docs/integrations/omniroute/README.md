<!-- STATUS: DRAFT · NOT ACTIVE · verify-then-install · opt-in only -->

# OmniRoute integration (INACTIVE, opt-in)

Design + templates only. **Nothing here is installed or activated.** OmniRoute
(https://github.com/diegosouzapw/OmniRoute, MIT) is a **local** gateway that puts one
OpenAI-compatible endpoint (`http://127.0.0.1:20128/v1`) in front of many providers, with
fallback and optional context compression. It **intercepts all model traffic and handles your
credentials**, so it is opt-in and isolated by default.

## Rules
- Do not install/run until a separate, explicit gate. Verify the repo/release/image first.
- **Never the default route.** Keep normal `claude`/`codex` pointing directly at their providers.
  Use the opt-in wrappers (`claude-omni`, `codex-omni`) only when you deliberately want the gateway.
- **Never on corporate repositories** without authorization.
- Do **not** enable OmniRoute's own concise/"ponytail-style" output — we already use the local
  Ponytail plugin; two would fight/duplicate.
- The vendor's 15–95% context-reduction figure is a **claim to measure**, not a guarantee.

## Files
- `SECURITY_CHECKLIST.md` — must-pass list before ever starting it.
- `env.example` — required secrets + hardening flags (placeholders; reconcile names with the pinned release's `.env.selfhost.example`).
- `docker-compose.example.yml` — loopback-only, pinned, no extra services.
- `claude-wrapper.example.sh` / `codex-wrapper.example.sh` — opt-in wrappers; normal commands stay direct.

## Rollback (if ever piloted)
`docker compose down`; remove the `.env`; delete the wrappers. Direct `claude`/`codex` are unaffected
because they were never modified.

## Future A/B (do NOT run now)
Same 3 tasks, direct vs `*-omni`, on a PUBLIC/personal repo with a test provider. Compare tokens,
latency, cost, correctness. Verify it logs no prompts and never binds beyond loopback. Only then
decide if it earns routine use.
