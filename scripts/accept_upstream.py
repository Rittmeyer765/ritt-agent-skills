#!/usr/bin/env python3
"""Accept a reviewed upstream snapshot as the new baseline."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from _common import read_json, resolve_upstream_source, validate_revision, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Accept a reviewed upstream snapshot")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--confirm", required=True)
    parser.add_argument("--source", default="mattpocock", help="Upstream source under upstream/ (default: mattpocock)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_revision(args.revision)
    validate_revision(args.confirm)
    if args.revision != args.confirm:
        raise SystemExit("--revision and --confirm must match exactly.")

    upstream_dir = resolve_upstream_source(args.source)
    # Never move the baseline to a revision whose immutable snapshot is not present.
    snapshot_manifest = upstream_dir / "snapshots" / args.revision / "MANIFEST.json"
    if not snapshot_manifest.exists():
        raise SystemExit(
            f"Refusing to accept {args.revision}: no snapshot manifest at {snapshot_manifest}. "
            "Run import_upstream.py for this revision first."
        )

    lock_path = upstream_dir / "LOCK.json"
    lock = read_json(lock_path, default={}) or {}
    lock.update(
        {
            "accepted_revision": args.revision,
            "accepted_at": datetime.now(timezone.utc).isoformat(),
            "last_checked_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_json(lock_path, lock)
    print(f"Accepted baseline {args.revision}")


if __name__ == "__main__":
    main()
