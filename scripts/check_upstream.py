#!/usr/bin/env python3
"""Check the current upstream revision and generate a report."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check upstream state")
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
    lock_path = ROOT / "upstream" / "mattpocock" / "LOCK.json"
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
    report_path = report_dir / "check-upstream.md"
    report_path.write_text(
        "# Upstream check\n\n"
        f"- Status: {status}\n"
        f"- Accepted revision: {accepted_revision or 'none'}\n"
        f"- Current head: {head or 'unavailable'}\n"
        f"- Checked at: {report['checked_at']}\n",
        encoding="utf-8",
    )

    print(f"Status: {status}")
    print(f"Report written to {report_path}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
