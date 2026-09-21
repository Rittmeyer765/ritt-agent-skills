#!/usr/bin/env python3
"""Compare a candidate upstream snapshot with the accepted baseline."""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import ROOT, read_json, resolve_upstream_source, validate_revision


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare upstream snapshot candidates")
    parser.add_argument("--source", default="mattpocock", help="Upstream source under upstream/ (default: mattpocock)")
    parser.add_argument("--candidate", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_revision(args.candidate)  # candidate feeds a path; must be a full SHA (no traversal)
    upstream_dir = resolve_upstream_source(args.source)
    lock = read_json(upstream_dir / "LOCK.json", default={}) or {}
    accepted_revision = lock.get("accepted_revision")
    if not accepted_revision:
        raise SystemExit("No accepted baseline exists yet.")

    candidate_dir = upstream_dir / "snapshots" / args.candidate
    accepted_dir = upstream_dir / "snapshots" / accepted_revision
    if not candidate_dir.exists() or not accepted_dir.exists():
        raise SystemExit("Candidate or accepted snapshot does not exist.")

    candidate_manifest = read_json(candidate_dir / "MANIFEST.json", default={}) or {}
    accepted_manifest = read_json(accepted_dir / "MANIFEST.json", default={}) or {}

    candidate_files = {item["path"]: item.get("sha256") for item in candidate_manifest.get("files", [])}
    accepted_files = {item["path"]: item.get("sha256") for item in accepted_manifest.get("files", [])}

    added = sorted(set(candidate_files) - set(accepted_files))
    removed = sorted(set(accepted_files) - set(candidate_files))
    modified = sorted([path for path in set(candidate_files) & set(accepted_files) if candidate_files[path] != accepted_files[path]])

    report = [
        "# Upstream comparison",
        "",
        f"- Candidate: {args.candidate}",
        f"- Accepted baseline: {accepted_revision}",
        "",
        "## Added",
        *([f"- {path}" for path in added] or ["- None"]),
        "",
        "## Removed",
        *([f"- {path}" for path in removed] or ["- None"]),
        "",
        "## Modified",
        *([f"- {path}" for path in modified] or ["- None"]),
        "",
    ]
    report_path = ROOT / "reports" / "upstream" / f"compare-{args.source}-{args.candidate}.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Comparison report written to {report_path}")


if __name__ == "__main__":
    main()
