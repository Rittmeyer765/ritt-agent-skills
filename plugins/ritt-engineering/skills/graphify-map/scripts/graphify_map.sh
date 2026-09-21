#!/usr/bin/env bash
# Guard-only adapter for Graphify. Explicit ops; never installs; never touches configs/hooks/network.
# Query logging is disabled by default; queries are budget-capped.
# Exit codes: 2 usage/invalid · 3 graphify not installed · 4 refused (unsupported/dangerous op).
set -euo pipefail
export GRAPHIFY_QUERY_LOG_DISABLE="${GRAPHIFY_QUERY_LOG_DISABLE:-1}"

ensure_present() {
  if ! command -v graphify >/dev/null 2>&1; then
    echo "graphify not found on PATH."
    echo "Official package: graphifyy  (install manually, pinned: 'uv tool install graphifyy==<version>')."
    echo "This adapter NEVER installs it and NEVER runs 'graphify install'."
    exit 3
  fi
}
valid_budget() {  # numeric and within a safe range
  local b="$1"
  case "$b" in ''|*[!0-9]*) return 1;; esac
  [ "$b" -ge 100 ] && [ "$b" -le 100000 ]
}
usage() {
  echo "usage: graphify_map.sh {build [path] | query \"<question>\" | path <args...> | explain <args...>}" >&2
  echo "  build -> graphify extract <path> --code-only   (default path: .)" >&2
  echo "  query -> graphify query \"<question>\" --budget \${GRAPHIFY_QUERY_BUDGET:-1500}" >&2
}

op="${1:-}"; shift || true
case "$op" in
  install|hook|hooks|mcp|serve|extract-docs|docs|media)
    echo "refused: '$op' is not allowed by this adapter (no install/hooks/mcp/serve/doc-media)."; exit 4;;
  build)
    ensure_present
    path="${1:-.}"
    exec graphify extract "$path" --code-only;;
  query)
    [ "$#" -ge 1 ] || { echo "query needs a \"<question>\"" >&2; exit 2; }
    budget="${GRAPHIFY_QUERY_BUDGET:-1500}"
    valid_budget "$budget" || { echo "invalid GRAPHIFY_QUERY_BUDGET='$budget' (integer 100..100000)" >&2; exit 2; }
    ensure_present
    exec graphify query "$@" --budget "$budget";;
  path|explain)
    ensure_present
    exec graphify "$op" "$@";;
  ""|-h|--help)
    usage; exit 2;;
  *)
    echo "refused: unknown/unsupported operation '$op'."; usage; exit 4;;
esac
