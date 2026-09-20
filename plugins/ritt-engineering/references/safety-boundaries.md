# Safety Boundaries

Reading, diagnosis, local edits, and non-destructive checks proceed autonomously. Everything below requires **explicit confirmation immediately before** the action — approval in one context does not carry to the next:

- Destructive deletion: `rm -rf` outside known generated dirs, dropping data, `git reset --hard`, force-checkout over uncommitted work.
- Git publication: `push`, force operations, merges to protected branches, tags, releases, package publishing.
- Deployments and infrastructure: deploys to any shared environment, `terraform apply/destroy/import`, Kubernetes mutations, cloud resource changes.
- Identity and secrets: IAM changes, secret/key/certificate creation, rotation, or deletion.
- Persistent data: migrations or scripts that mutate stored data.
- Dependencies: installing or upgrading production dependencies, lockfile changes.
- External communication: sending messages or email, creating tickets, calling external APIs with side effects.

Additional hard rules:

- Never weaken tests, suppress failing checks, or bypass safeguards to reach green.
- Never write secrets into code, config, logs, memory files, or handoffs.
- For infra validation, stop at `fmt` / `validate` / `plan` — `apply` is never a validation step.

Markdown is guidance, not enforcement. Configure the hard boundary in the tool: Claude Code permissions and `PreToolUse` hooks, Codex execpolicy rules, and sandboxing.
