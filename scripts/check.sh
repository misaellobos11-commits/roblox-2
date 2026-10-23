#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
tool_root="${MATTERLOOM_TOOLS:-/workspace/tools}"
luau_dir="$tool_root/luau-0.744"
"$luau_dir/luau" tests/construction.spec.luau
"$luau_dir/luau" tests/pointer.spec.luau
"$luau_dir/luau-analyze" src/shared/Construction.luau src/client/PointerRay.luau
mapfile -t luau_sources < <(rg --files src tests -g '*.luau')
"$luau_dir/luau-compile" --null "${luau_sources[@]}"
mkdir -p build
"$tool_root/bin/rojo" build default.project.json -o build/Matterloom.rbxlx
"$tool_root/bin/rojo" sourcemap default.project.json -o build/sourcemap.json
python scripts/check-place.py build/Matterloom.rbxlx
