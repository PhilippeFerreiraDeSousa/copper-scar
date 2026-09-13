#!/usr/bin/env bash
# Offline recording rehearsal. Every run gets a fresh, retained artifact directory.
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"
python_bin="${COPPER_SCAR_PYTHON:-$repo_dir/.venv/bin/python}"
if [[ ! -x "$python_bin" ]]; then
  echo 'Create .venv and install pydantic first; see demos/pass_timeline.md.' >&2
  exit 1
fi
mkdir -p demos/out
run_dir="$(mktemp -d "$repo_dir/demos/out/rehearsal.XXXXXX")"
"$python_bin" -m copper_scar.cli demo --no-weave --passes 3 \
  --scars-dir "$run_dir/scars" --out-dir "$run_dir" > "$run_dir/demo.log"
"$python_bin" -m copper_scar.cli eval --no-weave > "$run_dir/eval.txt"
# Keep the on-camera terminal focused. Full spans are retained in demo.log.
sed '/^--- spans ---/,$d' "$run_dir/pass_timeline.txt"
"$python_bin" - "$run_dir/scars/scar_001.json" <<'PY'
import json, sys
scar = json.load(open(sys.argv[1]))
print('Persisted rule:', json.dumps(scar['rule'], sort_keys=True))
PY
cat "$run_dir/eval.txt"
printf '\nArtifacts: %s\n' "$run_dir"
