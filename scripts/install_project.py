#!/usr/bin/env python3
"""Install the project instruction kit into a target repository.

Safety model:
- The target directory is NEVER deleted or replaced.
- Real project memory is NEVER overwritten, even with --force (create-if-absent only).
- `--dry-run` previews every action and writes nothing.
- Without --force, the script refuses if any non-memory destination file exists.
- With --force, conflicting non-memory files are backed up under
  <target>/.agent-kit-backup/<timestamp>/ before being overwritten.
- Legacy memory files are detected and a migration is PROPOSED, never imposed.
- The script never edits .gitignore or .git/info/exclude; it only prints a suggestion.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, has_symlink_in_chain, is_within

SOURCE = ROOT / "plugins" / "ritt-engineering" / "assets" / "project"

# Files that hold real, project-specific memory: create if absent, NEVER overwrite.
MEMORY_PROTECTED = {".agent/CONTEXT.md", ".agent/HANDOFF.md"}
# Any existing file under these dirs (except shipped scaffolding) is real memory too.
MEMORY_DIRS = (".agent/tasks/", ".agent/history/")
SCAFFOLDING = {".agent/tasks/_TEMPLATE.md", ".agent/history/README.md", ".agent/history/.gitkeep"}
# Legacy memory filenames (migration only).
LEGACY = [".agent/HISTORY.md", ".agent/PLANS.md", ".agent/RESEARCH.md"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install project instruction templates")
    parser.add_argument("target", help="Target project directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions; write nothing")
    parser.add_argument("--force", action="store_true", help="Back up and overwrite conflicting NON-memory files")
    return parser.parse_args()


def kit_files() -> list[Path]:
    return sorted(p for p in SOURCE.rglob("*") if p.is_file())


def is_memory(rel: str) -> bool:
    if rel in SCAFFOLDING:
        return False
    if rel in MEMORY_PROTECTED:
        return True
    return any(rel.startswith(d) for d in MEMORY_DIRS)


def main() -> None:
    args = parse_args()
    target = Path(args.target).resolve()
    if not target.is_dir():
        raise SystemExit(f"Target directory does not exist: {target}")

    creates: list[str] = []
    overwrites: list[str] = []        # non-memory conflicts (backed up under --force)
    memory_skips: list[str] = []      # existing memory: never touched

    for source_path in kit_files():
        rel = source_path.relative_to(SOURCE).as_posix()
        exists = (target / rel).exists()
        if not exists:
            creates.append(rel)
        elif is_memory(rel):
            memory_skips.append(rel)
        else:
            overwrites.append(rel)

    legacy_found = [rel for rel in LEGACY if (target / rel).exists()]

    # ---- Symlink safety: never write to, back up, or follow a symlinked destination ----
    # (a symlinked file or parent dir could redirect writes/backups outside the target).
    touched = [rel for rel in (creates + overwrites) if rel not in memory_skips]
    unsafe = sorted(
        rel for rel in touched
        if has_symlink_in_chain(target / rel, target) or not is_within(target / rel, target)
    )

    # ---- Report the plan ----
    print(f"Target: {target}")
    print(f"  create ({len(creates)}): " + (", ".join(creates) if creates else "-"))
    print(f"  overwrite non-memory ({len(overwrites)}): " + (", ".join(overwrites) if overwrites else "-"))
    print(f"  keep existing memory, untouched ({len(memory_skips)}): " + (", ".join(memory_skips) if memory_skips else "-"))
    if legacy_found:
        print("  LEGACY memory detected (not modified) — migrate manually to canonical schema:")
        for rel in legacy_found:
            hint = "history/YYYY-MM.md" if rel.endswith("HISTORY.md") else "tasks/<TASK-ID>.md"
            print(f"    {rel}  ->  .agent/{hint}")
    if unsafe:
        print("  REFUSING (symlinked destination or parent — write/backup could escape target):")
        for rel in unsafe:
            print(f"    {rel}")

    if args.dry_run:
        print("\nDry run: nothing was written.")
        return

    if unsafe:
        raise SystemExit(
            "Refusing to install: one or more destinations are symlinks (or under a symlinked "
            "directory). Remove the symlink(s) first; this script never writes through symlinks."
        )

    if overwrites and not args.force:
        raise SystemExit(
            "\nRefusing to overwrite existing non-memory files. "
            "Re-run with --force to back them up and overwrite, or --dry-run to preview."
        )

    backup_dir: Path | None = None
    if overwrites:  # only non-memory files are ever overwritten
        backup_root = target / ".agent-kit-backup"
        if has_symlink_in_chain(backup_root, target) or not is_within(backup_root, target):
            raise SystemExit(
                "Refusing: .agent-kit-backup is a symlink or resolves outside the target; "
                "backups must never be written through a symlink."
            )
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        backup_dir = target / ".agent-kit-backup" / timestamp
        for rel in overwrites:
            bp = backup_dir / rel
            bp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target / rel, bp)
        print(f"\nBacked up {len(overwrites)} file(s) to {backup_dir}")

    written = 0
    for source_path in kit_files():
        rel = source_path.relative_to(SOURCE).as_posix()
        if rel in memory_skips:
            continue  # never touch existing real memory
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        written += 1

    # ---- Post-install validation ----
    required = ["AGENTS.md", ".agent/README.md", ".agent/CONTEXT.md"]
    missing = [r for r in required if not (target / r).exists()]
    if missing:
        raise SystemExit(f"Post-install check FAILED, missing: {missing}")

    print(f"Installed/updated {written} file(s); {len(memory_skips)} memory file(s) left intact.")
    print("Post-install check PASSED (AGENTS.md, .agent/README.md, .agent/CONTEXT.md present).")
    print("Next steps:")
    print("  1. Review AGENTS.md and .agent/rules/.")
    print("  2. Adjust .agent/CONTEXT.md with the project's current state.")
    print("  3. Privacy (default): add AGENTS.md, CLAUDE.md, .agent/ and .agent-kit-backup/")
    print("     to the repo's .git/info/exclude yourself — this script never edits ignore files.")


if __name__ == "__main__":
    main()
