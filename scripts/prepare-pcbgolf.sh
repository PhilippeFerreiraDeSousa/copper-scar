#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
revision=7210bdb5049c5b7fdf4900a34928e2736767292a
source_dir="$PWD/.local/pcbgolf-source"
candidate_dir="$PWD/.local/pcbgolf-candidate"
mkdir -p .local
if [[ ! -d "$source_dir" ]]; then
  git clone https://github.com/commaai/PCBGolf.git "$source_dir"
  git -C "$source_dir" checkout --detach "$revision"
fi
[[ "$(git -C "$source_dir" rev-parse HEAD)" == "$revision" ]]
[[ -z "$(git -C "$source_dir" status --porcelain)" ]]
if [[ ! -d "$candidate_dir" ]]; then
  git clone --no-hardlinks "$source_dir" "$candidate_dir"
  git -C "$candidate_dir" switch -c codex/pcbgolf-candidate
fi
printf 'Reference: %s\nCandidate: %s\n' "$source_dir" "$candidate_dir"
