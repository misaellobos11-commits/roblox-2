#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
check_tmp=$(mktemp -d)
trap 'rm -rf "$check_tmp"' EXIT
python stage8/build_86.py
python stage8/tests/build_regressions.py build/Matterloom_8_6_Cintas.rbxlx "$check_tmp"
python stage8/tests/build_belt_regressions.py "$check_tmp"
python stage8/tests/build_visual_contract.py "$check_tmp"
/workspace/tools/luau-0.744/luau "$check_tmp/logic.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/belt-render.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/belt-preview.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/visual-contract.luau"
/workspace/tools/luau-0.744/luau-compile --null "$check_tmp"/*.luau
python stage8/tests/verify_place.py stage8/original-8.4.rbxlx build/Matterloom_8_6_Cintas.rbxlx --86
