# Validation

Discover checks from this repository — manifests, Makefile, CI config, Bazel targets. Never assume a tool is installed; a check that can't run is reported `NOT RUN` with the reason, not silently replaced.

## Ladder (climb as high as the risk demands)

1. Static: format / lint / type check on changed files (repo-configured tools only).
2. Targeted tests: the affected module or targets.
3. Integration boundary: the seams that changed.
4. Build: the affected artifact (package, binary, bundle, image, Bazel target).
5. Smoke: real behavior in a safe environment when user-visible or operational.
6. Final diff review: unrelated files, secrets, generated artifacts.

Risk floor: migrations, security, infra, and public-contract changes reach at least step 4. Infra validation stops at `fmt`/`validate`/`plan` — never `apply`.

Report every step as `PASSED` / `FAILED` (with output) / `PARTIAL` / `NOT RUN` (reason) / `NOT APPLICABLE`.

## Project commands

<!-- setup-project fills these in with the repo's real commands -->
- Test: _(e.g. `bazel test //...`, `npm test`)_
- Lint: _(…)_
- Build: _(…)_
