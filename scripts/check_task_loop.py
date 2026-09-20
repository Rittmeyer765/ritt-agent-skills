#!/usr/bin/env python3
"""Anti-loop guard for .agent/tasks/<id>.md attempt tables.

State COUNTERS are scoped PER TABLE (they reset at every attempts-table header
`| attempt |...` or `#`/`##` section heading), so a fingerprint legitimately reused
once per table is not cross-flagged. The RESULT is whole-file: any table with a true
violation flags the entire file — a clean later table never hides an earlier real loop
(historical violations remain blocking).

## Rules (per table)
- `action_fingerprint`: an identifier of the action taken (command + key args). A fingerprint
  may repeat ONLY if `input_changed` is truthy on the repeat (you changed inputs/env/approach).
  A repeated fingerprint with `input_changed` false/empty is a loop.
- `input_changed`: truthy (`true/yes/si/sí`) means this attempt materially changed inputs,
  environment, or approach versus the earlier attempt with the same fingerprint.
- A hypothesis may back at most **2** attempts; a 3rd attempt for the same hypothesis is a loop
  (reformulate into a new, differently-named hypothesis instead).
- "No progress": more than **3 consecutive** non-`OK` results is a loop; an `OK` resets it.

## Usage
  check_task_loop.py <file>                      # validate an existing file
  check_task_loop.py <file> --candidate "<row>"  # PROSPECTIVE: evaluate file + candidate row (no write)
  check_task_loop.py <file> --candidate-stdin    # candidate row read from stdin
  check_task_loop.py <file> --candidate "<row>" --append   # if allowed, atomically append the row

Exit codes: 0 allowed / 1 ANTI-LOOP BLOCK / 2 usage or invalid file/row.
"""
from __future__ import annotations
import argparse
import os
import sys
import tempfile
from pathlib import Path


def _is_sep(cells: list[str]) -> bool:
    return all(set(c) <= {"-", ":"} and c for c in cells) if cells else False


_COLUMNS = ["attempt", "hypothesis", "action_fingerprint", "input_changed", "result", "evidence", "next"]
_VALID_INPUT_CHANGED = {"true", "false", "yes", "no", "si", "sí", "n/a", "-"}
_VALID_RESULT = {"OK", "KO", "PARTIAL", "BLOCKED", "UNVERIFIED", "NOT RUN", "N/A"}


def validate_row(row: str) -> str | None:
    """Return an error string if `row` is not a well-formed attempt row, else None."""
    if row.strip("\n").count("\n") > 0:
        return "candidate must be a single line"
    s = row.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return "row must be a full markdown table row delimited by '|'"
    cells = [c.strip() for c in s.strip("|").split("|")]
    if len(cells) != len(_COLUMNS):
        return f"row must have exactly {len(_COLUMNS)} columns ({'|'.join(_COLUMNS)}), got {len(cells)}"
    for name, val in zip(_COLUMNS, cells):
        if not val:
            return f"column '{name}' must not be empty"
    if cells[3].lower() not in _VALID_INPUT_CHANGED:
        return f"input_changed must be one of {sorted(_VALID_INPUT_CHANGED)}"
    if cells[4].upper() not in _VALID_RESULT:
        return f"result must be one of {sorted(_VALID_RESULT)}"
    return None


def find_violations(text: str) -> list[str]:
    errs: list[str] = []
    seen_fp: dict[str, bool] = {}
    hyp_count: dict[str, int] = {}
    no_progress = 0

    def reset():
        nonlocal seen_fp, hyp_count, no_progress
        seen_fp, hyp_count, no_progress = {}, {}, 0

    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("#"):
            reset()
            continue
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5 or _is_sep(cells):
            continue
        if cells[0].lower() in ("attempt", "n"):
            reset()
            continue

        hyp, fp = cells[1], cells[2]
        input_changed = cells[3].lower() in ("true", "yes", "si", "sí")
        result = cells[4].upper()

        if fp:
            if fp in seen_fp and not input_changed:
                errs.append(f"repeated fingerprint '{fp}' without input_changed")
            seen_fp[fp] = input_changed
        if hyp:
            hyp_count[hyp] = hyp_count.get(hyp, 0) + 1
            if hyp_count[hyp] > 2:
                errs.append(f"more than 2 attempts for hypothesis '{hyp}'")
        if result and result != "OK":
            no_progress += 1
            if no_progress > 3:
                errs.append("more than 3 consecutive attempts without observable progress")
        else:
            no_progress = 0
    return list(dict.fromkeys(errs))


def atomic_append(path: Path, row: str) -> None:
    """Append `row` (+newline) to `path` atomically via a temp file in the same dir."""
    current = path.read_text(encoding="utf-8")
    if current and not current.endswith("\n"):
        current += "\n"
    new = current + row.rstrip("\n") + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp_task_", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(new)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description="Anti-loop guard (prospective, atomic)")
    ap.add_argument("file")
    ap.add_argument("--candidate", help="candidate attempt row to evaluate (prospective)")
    ap.add_argument("--candidate-stdin", action="store_true", help="read candidate row from stdin")
    ap.add_argument("--append", action="store_true", help="atomically append the candidate if allowed")
    args = ap.parse_args()

    p = Path(args.file)
    if not p.exists():
        print(f"no such file: {p}")
        return 2

    candidate = args.candidate
    if args.candidate_stdin:
        candidate = sys.stdin.read().strip()
    if args.append and not candidate:
        print("--append requires --candidate/--candidate-stdin")
        return 2
    if candidate is not None:
        err = validate_row(candidate)
        if err:
            print(f"invalid candidate row: {err}")
            return 2

    text = p.read_text(encoding="utf-8")
    effective = text
    if candidate:
        if not effective.endswith("\n"):
            effective += "\n"
        effective += candidate.rstrip("\n") + "\n"

    errs = find_violations(effective)
    if errs:
        print("ANTI-LOOP BLOCK:")
        for e in errs:
            print(f"  - {e}")
        return 1

    if args.append and candidate:
        atomic_append(p, candidate)
        print("candidate allowed: appended atomically")
        return 0
    print("anti-loop OK: no violations" + (" (candidate allowed)" if candidate else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
