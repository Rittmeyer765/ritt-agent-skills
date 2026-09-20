"""Shared helpers for repository maintenance scripts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def read_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_tracked_paths(tracked_path: Path) -> list[str]:
    data = read_json(tracked_path, default={})
    if isinstance(data, dict):
        paths = data.get("paths") or data.get("tracked_paths") or []
        if isinstance(paths, list):
            return [str(item) for item in paths]
    if isinstance(data, list):
        return [str(item) for item in data]
    return []


# ---- Security helpers (path traversal / symlink hardening) ----
import re as _re

SHA1_RE = _re.compile(r"^[0-9a-f]{40}$")


def validate_revision(rev: str) -> str:
    """Accept only a full 40-char lowercase hex SHA. Blocks path traversal via --revision."""
    if not isinstance(rev, str) or not SHA1_RE.match(rev):
        raise SystemExit(f"Invalid revision {rev!r}: must match ^[0-9a-f]{{40}}$ (full commit SHA).")
    return rev


def is_within(path: Path, base: Path) -> bool:
    """True iff `path` resolves to a location inside `base` (resolved)."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except (ValueError, OSError):
        return False


def has_symlink_in_chain(path: Path, boundary: Path) -> bool:
    """True if `path` itself, or any ancestor down to (and excluding) `boundary`, is a symlink.

    `path` need not exist yet; non-existent components are simply skipped. `boundary` must be an
    ancestor of `path`. Use to refuse following a symlink into or out of a trusted directory.
    """
    boundary = boundary.resolve()
    node = path
    while True:
        try:
            if node.is_symlink():
                return True
        except OSError:
            return True
        rp = node.resolve()
        if rp == boundary:
            return False
        if node.parent == node:  # filesystem root reached without hitting boundary
            return False
        node = node.parent
