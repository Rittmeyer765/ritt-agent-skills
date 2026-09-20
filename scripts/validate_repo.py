#!/usr/bin/env python3
"""Validate repo structure, manifests, skill frontmatter, invocation/effect coherence
(disable-model-invocation <-> allow_implicit_invocation), canonical memory schema,
absence of legacy runtime references, links, and version."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import ROOT

PLUGIN = ROOT / "plugins" / "ritt-engineering"

EXPECTED_SKILLS = 12          # count test: bump when adding/removing a skill
EXPECTED_VERSION = "0.4.0"    # release under validation

_POLICY_RE = re.compile(r"allow_implicit_invocation\s*:\s*(true|false)")
_LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#)([^)]+)\)")
# Case-sensitive legacy filenames (won't match the rules file research.md)
_LEGACY_RE = re.compile(r"HISTORY\.md|PLANS\.md|RESEARCH\.md")
_LEGACY_OK = re.compile(r"legacy|migra|does NOT create|no new writes|ninguna escritura|solo migraci", re.I)


def check_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required path: {path}")


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{skill_file}: missing YAML frontmatter (must start with ---)")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"')
    raise ValueError(f"{skill_file}: unterminated frontmatter block")


def parse_openai_policy(yaml_file: Path) -> bool:
    match = _POLICY_RE.search(yaml_file.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{yaml_file}: missing policy.allow_implicit_invocation (true|false)")
    return match.group(1) == "true"


def validate_skills() -> int:
    skill_dir = PLUGIN / "skills"
    skill_paths = sorted(path for path in skill_dir.iterdir() if path.is_dir())
    for skill_path in skill_paths:
        skill_file = skill_path / "SKILL.md"
        check_path(skill_file)
        fields = parse_frontmatter(skill_file)
        if fields.get("name") != skill_path.name:
            raise ValueError(
                f"{skill_file}: frontmatter name {fields.get('name')!r} "
                f"does not match directory {skill_path.name!r}"
            )
        if len(fields.get("description", "")) < 20:
            raise ValueError(f"{skill_file}: description missing or too short to trigger reliably")

        yaml_file = skill_path / "agents" / "openai.yaml"
        check_path(yaml_file)
        allow_implicit = parse_openai_policy(yaml_file)
        disable = fields.get("disable-model-invocation", "").lower() == "true"
        if allow_implicit == disable:
            raise ValueError(
                f"{skill_path.name}: invocation policy incoherent — "
                f"disable-model-invocation={disable} but allow_implicit_invocation={allow_implicit}."
            )

    if len(skill_paths) != EXPECTED_SKILLS:
        raise ValueError(f"Skill count {len(skill_paths)} != EXPECTED_SKILLS {EXPECTED_SKILLS}.")
    return len(skill_paths)


def validate_versions() -> str:
    claude_plugin = read_json(PLUGIN / ".claude-plugin" / "plugin.json") or {}
    codex_plugin = read_json(PLUGIN / ".codex-plugin" / "plugin.json") or {}
    marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json") or {}
    versions = {
        "claude-plugin": claude_plugin.get("version"),
        "codex-plugin": codex_plugin.get("version"),
        "marketplace": (marketplace.get("plugins") or [{}])[0].get("version"),
    }
    if len(set(versions.values())) != 1 or None in versions.values():
        raise ValueError(f"Version mismatch across manifests: {versions}")
    version = str(claude_plugin["version"])
    if version != EXPECTED_VERSION:
        raise ValueError(f"Version {version} != EXPECTED_VERSION {EXPECTED_VERSION}")
    return version


def validate_links() -> int:
    checked = 0
    md_files = [ROOT / "README.md", *sorted((PLUGIN / "skills").glob("*/SKILL.md"))]
    for md_file in md_files:
        for target in _LINK_RE.findall(md_file.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0].strip()
            if not target:
                continue
            if not (md_file.parent / target).resolve().exists():
                raise ValueError(f"{md_file}: broken repo link -> {target}")
            checked += 1
    return checked


def validate_no_legacy_runtime_refs() -> int:
    """No doc may reference legacy memory files except on a line clearly about migration."""
    offenders = []
    scan_dirs = [PLUGIN / "skills", PLUGIN / "references", PLUGIN / "assets", ROOT]
    seen: set[Path] = set()
    for base in scan_dirs:
        for md in ([base] if base.is_file() else base.rglob("*.md")):
            if md in seen or "/.git/" in str(md) or "/docs/design/" in str(md) or md.name == "CHANGELOG.md":
                continue
            seen.add(md)
            for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                if _LEGACY_RE.search(line) and not _LEGACY_OK.search(line):
                    offenders.append(f"{md.relative_to(ROOT)}:{i}")
    # README top-level allowed to mention within migration context already filtered by _LEGACY_OK
    if offenders:
        raise ValueError("Legacy memory references outside migration context:\n  " + "\n  ".join(offenders))
    return len(seen)


def validate_canonical_template() -> None:
    agent = PLUGIN / "assets" / "project" / ".agent"
    for rel in ["CONTEXT.md", "README.md", "HANDOFF.md", "tasks/_TEMPLATE.md", "history"]:
        check_path(agent / rel)
    for legacy in ["HISTORY.md", "PLANS.md", "RESEARCH.md"]:
        if (agent / legacy).exists():
            raise ValueError(f"Template still ships legacy memory file: .agent/{legacy}")


def validate_upstream_baseline() -> None:
    lock = read_json(ROOT / "upstream" / "mattpocock" / "LOCK.json", default={}) or {}
    revision = lock.get("accepted_revision")
    if revision:
        if not SHA1_RE.match(str(revision)):
            raise ValueError(f"LOCK accepted_revision {revision!r} is not a 40-char hex SHA")
        manifest = ROOT / "upstream" / "mattpocock" / "snapshots" / revision / "MANIFEST.json"
        if not manifest.exists():
            raise ValueError(f"LOCK accepted_revision {revision} has no snapshot manifest")


def validate_security_regression() -> None:
    """Run the filesystem/logic security regression suite; fail validation if any attack succeeds."""
    import subprocess

    test = ROOT / "scripts" / "test_security.py"
    check_path(test)
    result = subprocess.run([sys.executable, str(test)], capture_output=True, text=True)
    if result.returncode != 0:
        raise ValueError("security regression tests FAILED:\n" + (result.stdout or result.stderr))


def validate_anti_loop_guard() -> None:
    """Self-test: the anti-loop guard exists, passes a valid table, and blocks a looping one."""
    import os
    import subprocess
    import tempfile

    guard = ROOT / "scripts" / "check_task_loop.py"
    check_path(guard)
    header = "## Attempts\n| attempt | hypothesis | action_fingerprint | input_changed | result | evidence | next |\n"
    good = header + "| 1 | h1 | fp1 | false | KO | e | retry |\n| 2 | h2 | fp2 | true | OK | e | done |\n"
    bad = header + "| 1 | h | fp | false | KO | e | r |\n| 2 | h | fp | false | KO | e | r |\n| 3 | h | fp | false | KO | e | r |\n"
    # Multi-table legit: same fingerprint reused once per table must NOT false-positive.
    multi = ("## Iter 1\n" + header + "| 1 | h1 | shared_fp | false | KO | e | r |\n| 2 | h2 | fpb | true | OK | e | done |\n"
             + "## Iter 2\n" + header + "| 1 | h3 | shared_fp | false | KO | e | r |\n| 2 | h4 | fpc | true | OK | e | done |\n")
    valid_file = header + "| 1 | h | fpA | false | KO | e | r |\n| 2 | h | fpB | true | KO | e | r |\n"
    loop_row = "| 3 | h | fpB | false | KO | e | r |"   # repeats fpB + 3rd time hypothesis h
    ok_row = "| 3 | h3 | fpC | true | OK | e | done |"

    def run(*a: str) -> int:
        return subprocess.run([sys.executable, str(guard), *a], capture_output=True).returncode

    with tempfile.TemporaryDirectory() as d:
        gp, bp, mp = os.path.join(d, "good.md"), os.path.join(d, "bad.md"), os.path.join(d, "multi.md")
        Path(gp).write_text(good, encoding="utf-8")
        Path(bp).write_text(bad, encoding="utf-8")
        Path(mp).write_text(multi, encoding="utf-8")
        if run(gp) != 0:
            raise ValueError("anti-loop guard rejected a valid task file")
        if run(bp) != 1:
            raise ValueError("anti-loop guard failed to block a looping task file")
        if run(mp) != 0:
            raise ValueError("anti-loop guard false-positives on a legit multi-table file")

        # Prospective + atomic write contract (the real integration path used by project-memory).
        # 1) prospective block: candidate that creates a loop must not write.
        pb = os.path.join(d, "prosp_block.md"); Path(pb).write_text(valid_file, encoding="utf-8")
        before = Path(pb).read_bytes()
        if run(pb, "--candidate", loop_row, "--append") != 1:
            raise ValueError("prospective guard failed to block a looping candidate")
        if Path(pb).read_bytes() != before:
            raise ValueError("guard modified the file despite blocking the candidate")
        # 2) prospective allow + atomic append: valid candidate appends exactly one row.
        pa = os.path.join(d, "prosp_allow.md"); Path(pa).write_text(valid_file, encoding="utf-8")
        n0 = len(Path(pa).read_text(encoding="utf-8").splitlines())
        if run(pa, "--candidate", ok_row, "--append") != 0:
            raise ValueError("prospective guard rejected a valid candidate")
        if len(Path(pa).read_text(encoding="utf-8").splitlines()) != n0 + 1:
            raise ValueError("atomic append did not add exactly one row")
        # 3) usage error (row without pipes) must not write.
        pe = os.path.join(d, "prosp_err.md"); Path(pe).write_text(valid_file, encoding="utf-8")
        before = Path(pe).read_bytes()
        if run(pe, "--candidate", "3 h fpB false KO", "--append") != 2:
            raise ValueError("guard did not return usage error for a malformed candidate")
        if Path(pe).read_bytes() != before:
            raise ValueError("guard modified the file on usage error")


def main() -> None:
    for path in [
        ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "CHANGELOG.md", PLUGIN,
        ROOT / "upstream" / "mattpocock" / "LOCK.json",
        ROOT / "upstream" / "mattpocock" / "TRACKED.json",
        ROOT / "upstream" / "mattpocock" / "CUSTOMIZATIONS.json",
    ]:
        check_path(path)

    for manifest_path in [
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
    ]:
        if not isinstance(read_json(manifest_path), dict):
            raise ValueError(f"Invalid JSON manifest: {manifest_path}")

    skill_count = validate_skills()
    version = validate_versions()
    links = validate_links()
    docs_scanned = validate_no_legacy_runtime_refs()
    validate_canonical_template()
    validate_anti_loop_guard()
    validate_security_regression()
    validate_upstream_baseline()

    references = sorted((PLUGIN / "references").glob("*.md"))
    project_assets = PLUGIN / "assets" / "project"
    for path in [project_assets / "AGENTS.md", project_assets / "CLAUDE.md"]:
        check_path(path)

    print(
        f"Validation passed: version {version}, {skill_count} skills with coherent invocation policy, "
        f"{len(references)} references, {links} repo links OK, {docs_scanned} md files free of legacy "
        "runtime refs, canonical .agent template, anti-loop guard self-tested, security regression "
        "passed, manifests valid, upstream baseline consistent."
    )


from _common import SHA1_RE, read_json  # noqa: E402  (kept after functions for readability)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Validation failed: {exc}")
        sys.exit(1)
