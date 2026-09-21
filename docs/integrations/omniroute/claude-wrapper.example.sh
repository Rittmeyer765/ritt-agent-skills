#!/usr/bin/env bash
# OPT-IN wrapper `claude-omni`: route Claude Code through a LOCAL OmniRoute you started yourself.
# Your normal `claude` stays DIRECT and unmodified. Never use on corporate repos without authorization.
set -euo pipefail
# Verify the exact base-URL env var for your Claude Code version before relying on this.
export ANTHROPIC_BASE_URL="http://127.0.0.1:20128/v1"
exec claude "$@"
