#!/usr/bin/env python3
"""Check the current upstream revision and generate a report."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, read_json, resolve_upstream_source, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check upstream state")
    parser.add_argument("--source", default="mattpocock", help="Upstream source under upstream/ (default: mattpocock)")
    parser.add_argument("--head", default=None, help="Override the upstream head revision")
    return parser.parse_args()


def infer_head(lock: dict) -> str | None:
    remote = lock.get("remote")
    if not remote:
        return None
    try:
        result = subprocess.check_output(["git", "ls-remote", remote, "HEAD"], text=True, stderr=subprocess.STDOUT)
        return result.split()[0]
    except Exception:
        return None


def main() -> None:
    args = parse_args()
    upstream_dir = resolve_upstream_source(args.source)
    lock_path = upstream_dir / "LOCK.json"
    lock = read_json(lock_path, default={}) or {}
    report_dir = ROOT / "reports" / "upstream"
    report_dir.mkdir(parents=True, exist_ok=True)

    accepted_revision = lock.get("accepted_revision")
    head = args.head or infer_head(lock)

    if accepted_revision is None:
        status = "NO_BASELINE"
        exit_code = 2
    elif not head:
        status = "UNVERIFIED"
        exit_code = 3
    elif head == accepted_revision:
        status = "UP_TO_DATE"
        exit_code = 0
    else:
        status = "UPDATE_AVAILABLE"
        exit_code = 1

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "accepted_revision": accepted_revision,
        "head": head,
        "status": status,
    }
    content = (
        f"# Upstream check ({args.source})\n\n"
        f"- Source: {args.source}\n"
        f"- Status: {status}\n"
        f"- Accepted revision: {accepted_revision or 'none'}\n"
        f"- Current head: {head or 'unavailable'}\n"
        f"- Checked at: {report['checked_at']}\n"
    )
    report_path = report_dir / f"check-upstream-{args.source}.md"
    report_path.write_text(content, encoding="utf-8")
    # Back-compat: keep the legacy filename for the default source's existing consumers.
    if args.source == "mattpocock":
        (report_dir / "check-upstream.md").write_text(content, encoding="utf-8")

    print(f"Status: {status}")
    print(f"Report written to {report_path}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
