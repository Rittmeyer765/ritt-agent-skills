# Upstream Policy

Upstream is [mattpocock/skills](https://github.com/mattpocock/skills). It is an idea source, not a dependency.

## Rules

1. **Never auto-apply.** No script, hook, or agent may write upstream content into `plugins/`. Ever.
2. **Check = report.** `check_upstream.py` only compares SHAs and writes a report. Exit codes: 0 up-to-date, 1 update available, 2 no baseline, 3 unverifiable.
3. **Snapshots are immutable.** One directory per SHA under `upstream/mattpocock/snapshots/`, with a hashed manifest. Re-importing an existing SHA is a no-op.
4. **Review before accept.** An update is reviewed via `compare_upstream.py` + the `CUSTOMIZATIONS.json` map (which local skill adapts which upstream file). Only after human review does `accept_upstream.py` move the baseline — and it requires the SHA typed twice.
5. **Porting is normal work.** Bringing an upstream improvement into a local skill goes through plan-change → implement-change → validate_repo, and updates `CUSTOMIZATIONS.json`.
6. **Track deliberately.** `TRACKED.json` lists only paths we actually adapted or watch; tracking everything would make every upstream commit noise.

## Cadence

Run `/check-upstream` (or `python3 scripts/check_upstream.py`) when convenient — monthly is plenty. There is no automation that pulls; that is the point.
