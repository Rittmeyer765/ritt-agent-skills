# Integration Matrix (v0.5)

One responsibility per component. **No component writes another's store.**

| Layer                 | Responsibility                                         | Must NOT                                                     |
| --------------------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Agent Skills (spec)   | SKILL.md format + progressive loading                  | —                                                            |
| `ritt-agent-skills`   | working method + orchestration                         | —                                                            |
| `.agent/`             | decisions, tasks, attempts, handoff (durable memory)   | be replaced by Graphify                                      |
| Graphify (optional)   | derived structural code map (regenerable), `file:line` | store decisions / act as memory / be treated as ground truth |
| Ponytail              | concision + YAGNI (anti over-engineering)              | —                                                            |
| OmniRoute (optional)  | transport: providers, fallback, context compression    | become the default route / duplicate Ponytail's concision    |

Flow: request → kit orchestrates → Graphify (map) + `.agent/` (memory); Ponytail shapes the output;
OmniRoute, if ever enabled, is opt-in transport underneath.

Rules:
- **Graphify is a map, not memory.** A finding becomes durable only when the orchestrator records it
  in `.agent/` via `project-memory` (the single writer). Graphify outputs stay local, out of git/context.
- **OmniRoute is never the default.** Use only via opt-in wrappers; keep its own concise output OFF —
  Ponytail owns concision.
- No loops, no duplication: Graphify does not replace `.agent/`; OmniRoute does not replace Ponytail.

> Uso operativo y política final: ver `OPERATIONS.md`. Graphify es **manual/opcional** (ver `benchmarks/graphify-smoke.md`), no ruta por defecto.
