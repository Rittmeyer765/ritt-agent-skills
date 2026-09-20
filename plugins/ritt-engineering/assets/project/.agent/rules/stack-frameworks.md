# Stack: Frameworks

- Detect the stack from manifests and lockfiles; advice must match the **locked version**, not the latest docs.
- Follow the framework's current official documentation and the repo's existing idioms; when they conflict, surface the conflict.
- Framework upgrades are their own task with their own plan — never a side effect.
- Config files (`next.config.*`, `tsconfig.json`, `pyproject.toml`, CI) change only with an explicit reason stated.

<!-- setup-project: replace this generic file with per-stack rules the project actually uses (e.g. stack-python.md, stack-typescript.md) -->
