# Third-Party Evidence (Phase 0) — v0.5 integrations

Read-only verification of canonical sources. No third-party code was copied into this repo
during Phase 0. Repos confirmed via the GitHub API on 2026-09-20.

## Agent Skills (specification)
- Canonical spec: https://agentskills.io/specification
- Spec repo: https://github.com/agentskills/agentskills — **code Apache-2.0, documentation CC-BY-4.0** (per-content licensing; see repo `#license`). GitHub API reports the primary license as Apache-2.0.
- Official validator: `skills-ref validate ./skill` (from that repo). Not installed here; its rules are mirrored in `scripts/validate_repo.py`.
- Frontmatter (verified): `name` (req, 1–64, `^[a-z0-9]+(?:-[a-z0-9]+)*$`, must match dir, no leading/trailing/consecutive hyphens), `description` (req, 1–1024, non-empty), `license` (opt, string), `compatibility` (opt, 1–500), `metadata` (opt, map string→string), `allowed-tools` (opt, space-separated string, experimental). SKILL.md < 500 lines recommended; references one level deep.
- **No `anthropic`/`claude` name prohibition exists in the spec.** (Earlier assumption was wrong.)
- Examples repo: https://github.com/anthropics/skills — **per-directory licensing** (NOT simply "no license"): many skills are Apache-2.0, while the document skills are **source-available** only (see the repo README "About this repository"). The GitHub API reports no single top-level license. Treat as examples only; **do not copy** and **do not use as the conformance source**.

## Graphify (optional, code-map)
- Repo: https://github.com/Graphify-Labs/graphify — **Apache-2.0 with MIT components/`NOTICE`** where applicable (ships `LICENSE` + `LICENSE-MIT` + `NOTICE`), default branch `v8`.
- Package name: **`graphifyy`** (pyproject `name = "graphifyy"`); CLI command is **`graphify`**. Install (NOT run here): `uv tool install graphifyy==<pinned>`.
- Ships its OWN `AGENTS.md`, `ARCHITECTURE.md`, `.pre-commit-config.yaml`, and an installer. `graphify install` can write `AGENTS.md`/`CLAUDE.md`/hooks → **collision risk with this kit**. Our adapter never runs `graphify install`.
- Local vs network: AST/tree-sitter **code** analysis is local and does not execute source. The skill also exposes MCP/`serve` and optional doc/PDF/image/URL/semantic features that may use network/model. → **pilot is `--code-only`**; other modes require explicit confirmation. `INFERRED` edges are hypotheses.
- Security: https://github.com/Graphify-Labs/graphify/blob/v8/SECURITY.md

## OmniRoute (optional, transport)
- Repo: https://github.com/diegosouzapw/OmniRoute — license **MIT**, default branch `release/v3.8.51`.
- Local gateway (npm/docker) at `http://localhost:20128/v1`; ships `.env.selfhost.example` + `docker-compose.prod.yml` + `SECURITY.md`.
- It **intercepts all model traffic and handles credentials**. If `STORAGE_ENCRYPTION_KEY` is unset it can fall back to plaintext credential storage → must be set. Surfaces to disable by default: MCP, A2A, webhooks, cloud sync, MITM, secondary services, non-loopback binding, prompt logging.
- Security model: https://github.com/diegosouzapw/OmniRoute/blob/main/SECURITY.md
- Vendor-claimed 15–95% context reduction is a **claim to measure**, not a guaranteed result.

## Decisions carried into implementation
- Track `agentskills/agentskills` as the spec upstream (Apache-2.0); do NOT import snapshots yet; do NOT auto-import `anthropics/skills`.
- Graphify: manual-only adapter skill, no install, `--code-only`, outputs kept local.
- OmniRoute: docs + templates only; not installed, not activated; opt-in wrappers.
