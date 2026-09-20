---
name: review-change
description: Review a diff for correctness, security, and maintainability, reporting findings by severity. Use before committing or handing off a change, when the user asks for a review, or after implement-change on anything touching auth, data, infra, or public contracts.
---

Review the diff as a skeptical colleague who will be paged when it breaks. Findings, not compliments.

## Scope

Review the actual diff (`git diff`, staged or branch), not the description of it. Read enough surrounding code to judge each change in context.

## Checklist

**Correctness**
- Does the change do what the plan says — and nothing else? Flag every unrelated edit.
- Edge cases: empty inputs, errors, concurrency, timezone/encoding, boundary values.
- Are the tests real? A test that cannot fail is a finding.

**Security (always, not only "security tasks")**
- Secrets or credentials in code, config, logs, or test fixtures.
- Unvalidated external input; injection (SQL, shell, path, template).
- AuthN/AuthZ changes: privilege escalation, missing checks, IAM widening.
- New dependencies: supply-chain risk, license, known advisories.
- Unsafe defaults, weakened TLS/crypto, data exposure in errors or logs.

**Maintainability**
- Follows existing patterns and naming; no parallel abstraction for something that exists.
- Public contract changes are intentional, versioned, and documented.
- Dead code, debug leftovers, commented-out blocks, generated artifacts in the diff.

## Report

Order findings by severity: **BLOCKER** (must fix), **MAJOR** (should fix now), **MINOR** (follow-up), **NOTE**. For each: file/line, the issue, why it matters, and a concrete fix. State explicitly what you did NOT review. If the change is sound, say so plainly — do not pad findings to justify the review.

This skill is read-only and independent of the author: it does not edit code or write memory, and it must not run in the same pass as the change's implementer. It returns findings to the orchestrator.
