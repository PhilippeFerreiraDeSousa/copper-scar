#!/usr/bin/env bash
# Local tooling only. Provider choice stays explicit at the call site.
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${COPPERHEAD_KICAD_CLI:-}" ]]; then
  for candidate in "$HOME/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli" /Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli; do
    if [[ -x "$candidate" ]]; then
      export COPPERHEAD_KICAD_CLI="$candidate"
      break
    fi
  done
fi
# Avoid the user's broken global npm launcher; this package is pinned in our lock.
export COPPERHEAD_CODEX_PATH="${COPPERHEAD_CODEX_PATH:-$repo_dir/node_modules/.bin/codex}"
exec "$repo_dir/node_modules/.bin/copperhead" "$@"
