# Framework Discovery

Identify the stack before proposing anything, and let each framework's own conventions win over generic habits.

## Detect

- Manifests and lockfiles: `package.json`, `pyproject.toml`, `go.mod`, `requirements*.txt`, `Cargo.toml`.
- Build system: `MODULE.bazel` / `WORKSPACE` / `BUILD` files (Bazel), `Makefile`, `Dockerfile`, CI config.
- Framework markers: `next.config.*`, `vite.config.*`, `tsconfig.json`, `manage.py`, `main.go` layout, k8s manifests, `terraform/`.
- Versions matter: read the lockfile, not just the manifest — advice for v3 can be wrong for v4.

## Apply

- Follow the framework's **current official documentation** for the detected version; prefer primary sources over blog posts.
- Match the repo's existing idioms even when the docs allow alternatives — local consistency beats global fashion.
- When the repo and the framework's best practice conflict, surface the conflict instead of silently picking one.
- For stack-specific depth, load the matching `.agent/rules/stack-*.md` in the project (Bazel guidance lives in bazel-guidance.md).
