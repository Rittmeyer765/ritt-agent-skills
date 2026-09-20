# Validation Ladder

Discover checks from the repository (manifests, Makefile, CI config, Bazel targets); never assume a tool is installed. Climb only as high as the risk demands — and no less.

1. **Inspect** — requirements, affected paths, repo-provided commands.
2. **Static** — format, lint, type check on changed files, using only tools the repo configures.
3. **Targeted tests** — the affected module or Bazel targets first; broad suites only when the change is shared or cross-cutting.
4. **Integration boundary** — exercise the seams that changed (API↔consumer, service↔DB, component↔API, build rule↔artifact).
5. **Build** — the affected artifact: package, binary, bundle, Bazel target, container image.
6. **Smoke** — real behavior in a local or safe environment when the change is user-visible or operational.
7. **Final diff review** — unrelated files, secrets, generated artifacts, `git diff --check`.

Risk floor: migrations, security, infra, and public-contract changes must reach at least step 5. QUICK-mode edits may stop at 2–3 unless something fails.

Every step reports one of: `PASSED`, `FAILED` (with output), `PARTIAL`, `NOT RUN` (with reason), `NOT APPLICABLE`. A skipped step is reported, never silently omitted.
