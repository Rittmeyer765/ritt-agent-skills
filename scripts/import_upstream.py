#!/usr/bin/env python3
"""Import a specific upstream revision into an immutable snapshot.

The snapshot is read-only input for review. Importing NEVER touches
plugins/ — promoting upstream ideas into a skill is always a manual edit.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from _common import (
    ROOT,
    ensure_dir,
    has_symlink_in_chain,
    is_within,
    load_tracked_paths,
    read_json,
    resolve_upstream_source,
    sha256_file,
    validate_revision,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import an upstream snapshot candidate")
    parser.add_argument("--revision", required=True, help="Full commit SHA to import")
    parser.add_argument("--source", default="mattpocock", help="Upstream source under upstream/ (default: mattpocock)")
    parser.add_argument("--source-dir", default=None, help="Optional local checkout to import from")
    return parser.parse_args()


def checkout_revision(repo_url: str, revision: str, workdir: Path) -> Path:
    subprocess.run(
        ["git", "clone", "--filter=blob:none", repo_url, str(workdir)],
        check=True, capture_output=True, text=True,
    )
    subprocess.run(
        ["git", "-C", str(workdir), "checkout", "--detach", revision],
        check=True, capture_output=True, text=True,
    )
    return workdir


def resolved_head(checkout: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
        ).strip()
    except Exception:
        return None


def assert_safe_snapshots_root(snapshots_root: Path, upstream_dir: Path) -> None:
    """Refuse if snapshots/ is a symlink, sits under a symlink, or resolves outside upstream/."""
    if has_symlink_in_chain(snapshots_root, upstream_dir) or not is_within(snapshots_root, upstream_dir):
        raise SystemExit(
            "Refusing: snapshots/ is a symlink or resolves outside upstream/mattpocock/."
        )


def snapshot_files(source_dir: Path, tracked_paths: list[str]) -> list[Path]:
    """Expand tracked paths into concrete files, refusing symlinks and out-of-checkout escapes."""
    files: list[Path] = []
    src_root = source_dir.resolve()
    for rel_path in tracked_paths:
        source_path = source_dir / rel_path
        if has_symlink_in_chain(source_path, source_dir):
            raise SystemExit(f"Refusing symlinked tracked path (possible exfiltration): {rel_path}")
        if source_path.is_dir():
            for p in sorted(source_path.rglob("*")):
                if p.is_symlink():
                    raise SystemExit(f"Refusing symlink inside tracked dir: {p.relative_to(source_dir)}")
                if p.is_file() and is_within(p, src_root):
                    files.append(p)
        elif source_path.is_file() and is_within(source_path, src_root):
            files.append(source_path)
    return files


def main() -> None:
    args = parse_args()
    validate_revision(args.revision)  # blocks path traversal via --revision
    upstream_dir = resolve_upstream_source(args.source)
    lock = read_json(upstream_dir / "LOCK.json", default={}) or {}
    tracked_paths = load_tracked_paths(upstream_dir / "TRACKED.json")
    if not tracked_paths:
        raise SystemExit("TRACKED.json lists no paths; nothing to import.")

    snapshots_root = upstream_dir / "snapshots"
    assert_safe_snapshots_root(snapshots_root, upstream_dir)
    snapshot_dir = snapshots_root / args.revision
    if not is_within(snapshot_dir, snapshots_root):
        raise SystemExit("Refusing snapshot path outside snapshots/.")
    manifest_path = snapshot_dir / "MANIFEST.json"
    if manifest_path.exists():
        print(f"Snapshot already exists at {snapshot_dir}")
        return

    with tempfile.TemporaryDirectory(prefix="upstream-import-") as temp_dir:
        if args.source_dir:
            source_dir = Path(args.source_dir).resolve()
        else:
            repo_url = lock.get("remote")
            if not repo_url:
                raise SystemExit("No upstream remote in LOCK.json. Provide --source-dir.")
            source_dir = checkout_revision(repo_url, args.revision, Path(temp_dir) / "repo")

        actual = resolved_head(source_dir)
        if actual and actual != args.revision:
            raise SystemExit(
                f"Checkout is at {actual}, not the requested {args.revision}. "
                "Pass the full SHA, or check out the right revision in --source-dir."
            )

        ensure_dir(snapshot_dir)
        entries: list[dict[str, str | None]] = []
        missing: list[str] = []
        for source_path in snapshot_files(source_dir, tracked_paths):
            rel = source_path.relative_to(source_dir).as_posix()
            target_path = snapshot_dir / rel
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            entries.append({"path": rel, "sha256": sha256_file(target_path)})
        for rel_path in tracked_paths:
            if not (source_dir / rel_path).exists():
                missing.append(rel_path)

    manifest = {
        "revision": args.revision,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tracked_paths": tracked_paths,
        "missing_tracked_paths": missing,
        "files": entries,
    }
    write_json(manifest_path, manifest)
    print(f"Imported {len(entries)} file(s) into {snapshot_dir}")
    if missing:
        print("Tracked paths missing upstream (review TRACKED.json):")
        for rel_path in missing:
            print(f"  {rel_path}")


if __name__ == "__main__":
    main()
