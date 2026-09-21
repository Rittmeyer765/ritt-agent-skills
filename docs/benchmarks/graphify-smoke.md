# Graphify smoke A/B (2026-09-21)

Small, honest smoke test — NOT a benchmark. Target: a copy of this kit (~18 files, own MIT code).
6 independent read-only subagents (same type/model), each task run once per arm, agents never saw
each other. Graphify used only via `graphify-map` with `GRAPHIFY_QUERY_LOG_DISABLE=1`.

- **Initial cost (one-time):** graph build ~4.26 s.
- **Recurring cost:** per query (measured below).

## Results (runtime telemetry; output tokens only)

| Task | Arm | Correct | Output tokens | Tool calls | Duration |
| --- | --- | --- | --- | --- | --- |
| T1 read_json call-sites (GT 12) | baseline (grep) | yes (12/12) | n/a¹ | 9 | n/a¹ |
| T1 | graphify | yes (12/12, but graph alone gave 8 — needed grep for 4) | 20966 | 10 | 32.9 s |
| T2 call-path main→validate_anti_loop_guard | baseline | yes | 14586 | 1 | 10.4 s |
| T2 | graphify | yes | 11593 | 2 | 14.6 s |
| T3 resolve_upstream_source def+importers | baseline | **no (3/4, missed one importer)** | 8940 | 3 | 8.4 s |
| T3 | graphify | yes (4/4 + extra use) | 21684 | 8 | 22.8 s |

¹ T1-baseline telemetry not surfaced separately (proxy: 9 tool calls).

## Reading
- Graphify **did not reduce tokens or time** here — mostly higher (query dumps a large subgraph and
  the agent still reads to confirm). On simple lookups grep is cheaper/faster.
- Its value was **recall/precision**: T3 baseline (grep) under-counted importers; Graphify found them all.
- The graph is **not always complete** (T1 needed grep fallback).

## Decision
**OPTIONAL, not default.** No ≥15% token/time win → not adopted as the default route. Kept as a manual
tool for hard cross-file dependency/usage questions where grep under-counts.

## Limitations
n=3; T1-baseline tokens missing; **output tokens only** (not input+output); do not extrapolate to large
monorepos.

## To re-evaluate later
Use a real case where grep fell short; measure **input+output** tokens; cap with `graphify query … --budget 1500`;
include graph **update** cost, not just first build.
