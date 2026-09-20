<!-- STATUS: DRAFT · NOT ACTIVE · BLOCKED: missing nine Obsidian notes -->

```python
#!/usr/bin/env python3
"""DRAFT — sync Obsidian Prompts/ -> kit snapshot. NO aplicar sin auditar las notas."""
import argparse, hashlib, json, os, sys
from pathlib import Path

VAULT_ROOT = Path(os.environ["OBSIDIAN_VAULT"])  # e.g. OBSIDIAN_VAULT=/path/to/your/vault
VAULT_PROMPTS = VAULT_ROOT / "Prompts"
SNAP = Path(__file__).resolve().parent.parent / "plugins/ritt-engineering/prompts"
MANIFEST = SNAP / "manifest.json"

def sha256(p: Path) -> str:
    h = hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}

def cmd_check() -> int:
    if not VAULT_PROMPTS.exists():
        print("BLOCKED: vault inaccesible (TCC). Concede Full Disk Access o pasa el ZIP."); return 2
    man = load_manifest(); stale = []
    for src in sorted(VAULT_PROMPTS.glob("*.md")):
        pid = src.stem
        if man.get(pid, {}).get("sha256") != sha256(src): stale.append(pid)
    print("OK: al día" if not stale else f"DESACTUALIZADOS: {stale}"); return 0

def cmd_pull() -> int:
    if not VAULT_PROMPTS.exists():
        print("BLOCKED: vault inaccesible (TCC)."); return 2
    SNAP.mkdir(parents=True, exist_ok=True); man = {}
    for src in sorted(VAULT_PROMPTS.glob("*.md")):
        dst = SNAP / f"{src.stem}.md"; dst.write_bytes(src.read_bytes())
        man[src.stem] = {"prompt_id": src.stem, "sha256": sha256(src)}  # no absolute paths in the manifest
    MANIFEST.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    print(f"pulled {len(man)} prompts"); return 0

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["--check", "--pull"])
    args = ap.parse_args()
    return cmd_check() if args.mode == "--check" else cmd_pull()

if __name__ == "__main__":
    sys.exit(main())
```
