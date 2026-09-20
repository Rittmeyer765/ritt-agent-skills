---
name: clarify-task
description: Sharpen an ambiguous or high-stakes task with one adaptive batch of targeted questions before any work starts. Use when scope, constraints, or acceptance criteria are unclear, before planning a large or risky change, or when the user asks to refine ("afinar") what to build.
---

Ask the questions that change the outcome — nothing else. Never ask for information the repository can already answer.

## Procedure

1. **Inspect first.** Read repository guidance (AGENTS.md/CLAUDE.md), `.agent/CONTEXT.md` if present, structure, manifests, and the files the task touches. Every question you can answer yourself is a question you must not ask.
2. **Size the question budget by risk, not by habit:**
   - Trivial, reversible change: 0–3 questions, or none.
   - Standard feature or fix: up to 10 questions.
   - High-risk work (migrations, security, data, infra, cross-service, ambiguous goals): up to 20 questions.
3. **Ask in ONE numbered batch**, grouped by theme (scope, constraints, acceptance, risks). For each question, propose a sensible default so the user can answer "defaults except 3 and 7".
4. **Challenge the premise when warranted.** If inspection suggests the requested approach is wrong, unsafe, or already solved, say so in the batch — disagreeing early is part of clarifying.
5. **Close with an explicit state:**
   - `READY` — scope, constraints, and acceptance criteria are clear.
   - `READY WITH ASSUMPTIONS` — list each assumption; proceed only if the user accepts them.
   - `BLOCKED` — name exactly what is missing and from whom.

## Output

A short summary: goal, in-scope / out-of-scope, constraints, acceptance criteria, open assumptions, and the closing state. This skill is read-only: it does not write memory. If the project keeps agent memory, recommend that the orchestrator persist the agreed scope to `.agent/CONTEXT.md` — do not write it yourself.
