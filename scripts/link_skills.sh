#!/usr/bin/env bash
# Symlink every plugin skill into the local harness skill directories so both
# Claude Code (~/.claude/skills) and Codex (~/.agents/skills) pick them up.
# Re-run after adding, removing, or renaming a skill. Only touches symlinks
# that point into this repository; real directories are never overwritten.
set -euo pipefail

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
skills_dir="$repo_dir/plugins/ritt-engineering/skills"
targets=("$HOME/.claude/skills" "$HOME/.agents/skills")

for target in "${targets[@]}"; do
  mkdir -p "$target"

  # Remove stale links that point into this repo but no longer exist.
  for link in "$target"/*; do
    [[ -L $link ]] || continue
    dest=$(readlink "$link")
    if [[ $dest == "$skills_dir"/* && ! -e $link ]]; then
      rm "$link"
      echo "Removed stale link: $link"
    fi
  done

  for skill in "$skills_dir"/*/; do
    name=$(basename "$skill")
    link="$target/$name"
    if [[ -L $link ]]; then
      ln -sfn "${skill%/}" "$link"
    elif [[ -e $link ]]; then
      echo "SKIP: $link exists and is not a symlink (not touching it)" >&2
      continue
    else
      ln -s "${skill%/}" "$link"
    fi
    echo "Linked $name -> $link"
  done
done
