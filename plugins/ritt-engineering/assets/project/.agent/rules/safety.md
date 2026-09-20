# Safety

Reading, diagnosis, local edits, and non-destructive checks proceed autonomously. Explicit confirmation is required immediately before:

- Destructive deletion: `rm -rf` outside known generated dirs, data drops, `git reset --hard`, checkout over uncommitted work.
- Git publication: push, force operations, merges to protected branches, tags, releases, package publishing.
- Deployments; `terraform apply/destroy/import`; Kubernetes or cloud resource mutations.
- IAM, secrets, keys, certificates: any creation, rotation, or deletion.
- Migrations or scripts that mutate persistent data.
- Installing or upgrading production dependencies / lockfile changes.
- External side effects: messages, email, tickets, external API mutations.

Hard rules:

- Never weaken tests, suppress failing checks, or bypass safeguards to reach green.
- Never write secrets into code, config, logs, memory files, or handoffs.
- Approval for one action does not extend to the next similar action.

This file is guidance. Enforce the boundary with tool-level config: Claude Code permissions + `PreToolUse` hooks, Codex execpolicy rules, and sandboxing.
