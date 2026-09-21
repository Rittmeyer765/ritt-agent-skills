#!/usr/bin/env bash
# OPT-IN wrapper `codex-omni`: route Codex through a LOCAL OmniRoute you started yourself.
# Your normal `codex` stays DIRECT and unmodified. Never use on corporate repos without authorization.
set -euo pipefail
# Point Codex at the local OpenAI-compatible endpoint via inline config overrides.
# Verify the exact model_provider keys for your codex version before relying on this.
exec codex -c 'model_provider="omniroute"' \
           -c 'model_providers.omniroute.base_url="http://127.0.0.1:20128/v1"' \
           "$@"
