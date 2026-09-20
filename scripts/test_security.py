#!/usr/bin/env python3
"""Regression tests reproducing the confirmed filesystem/logic attacks. Exit 0 = all blocked."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _common  # noqa: E402
import import_upstream  # noqa: E402


def _run(*args: str, cwd: str | None = None):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=cwd)


def test_revision_traversal() -> bool:
    for bad in ["../../../escape", "..%2f..", "abc", "e9fcdf95" * 5 + "z", "/etc/passwd"]:
        try:
            _common.validate_revision(bad)
            return False  # should have raised
        except SystemExit:
            pass
    return True


def test_import_symlink_source() -> bool:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "external.txt").write_text("SECRET-EXTERNAL")
        src = d / "src"; src.mkdir()
        os.symlink(d / "external.txt", src / "evil.md")
        try:
            import_upstream.snapshot_files(src, ["evil.md"])
            return False
        except SystemExit:
            return True


def test_install_symlink_dest() -> bool:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "outside.txt").write_text("EXTERNAL-UNTOUCHABLE")
        target = d / "target"; target.mkdir()
        os.symlink(d / "outside.txt", target / "AGENTS.md")  # symlinked destination
        r = _run(str(SCRIPTS / "install_project.py"), str(target), "--force")
        blocked = r.returncode != 0
        intact = (d / "outside.txt").read_text() == "EXTERNAL-UNTOUCHABLE"
        return blocked and intact


def test_install_backup_symlink() -> bool:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        external = d / "external"; external.mkdir()
        target = d / "target"; target.mkdir()
        (target / "AGENTS.md").write_text("ORIGINAL")  # non-memory conflict -> triggers backup
        os.symlink(external, target / ".agent-kit-backup")  # backup dir is a symlink outside target
        r = _run(str(SCRIPTS / "install_project.py"), str(target), "--force")
        blocked = r.returncode != 0
        external_empty = not any(external.iterdir())
        intact = (target / "AGENTS.md").read_text() == "ORIGINAL"
        return blocked and external_empty and intact


def test_import_snapshots_symlink() -> bool:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        upstream = d / "upstream"; upstream.mkdir()
        external = d / "external"; external.mkdir()
        os.symlink(external, upstream / "snapshots")  # snapshots is a symlink outside upstream
        try:
            import_upstream.assert_safe_snapshots_root(upstream / "snapshots", upstream)
            return False
        except SystemExit:
            return not any(external.iterdir())  # nothing written outside the repo


def test_check_task_loop_malformed() -> bool:
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "task.md"
        f.write_text("## Attempts\n| attempt | hypothesis | action_fingerprint | input_changed | result | evidence | next |\n| 1 | h | fp | true | OK | e | n |\n")
        before = f.read_bytes()
        r = _run(str(SCRIPTS / "check_task_loop.py"), str(f), "--candidate", "| malformed |", "--append")
        return r.returncode == 2 and f.read_bytes() == before


TESTS = {
    "revision path-traversal blocked": test_revision_traversal,
    "import_upstream symlink source blocked": test_import_symlink_source,
    "install_project symlink dest blocked": test_install_symlink_dest,
    "install_project .agent-kit-backup symlink blocked": test_install_backup_symlink,
    "import_upstream snapshots/ symlink blocked": test_import_snapshots_symlink,
    "check_task_loop malformed candidate blocked": test_check_task_loop_malformed,
}


def main() -> int:
    failed = 0
    for name, fn in TESTS.items():
        ok = False
        try:
            ok = fn()
        except Exception as exc:  # pragma: no cover
            print(f"  ERROR {name}: {exc}")
        print(f"  {'PASS' if ok else 'FAIL'}: {name}")
        failed += 0 if ok else 1
    print(f"security regression: {len(TESTS) - failed}/{len(TESTS)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
