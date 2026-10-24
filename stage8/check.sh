#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
check_tmp=$(mktemp -d)
trap 'rm -rf "$check_tmp"' EXIT
python stage8/build.py
python stage8/tests/build_regressions.py build/Matterloom_8_5_Prueba_Conexiones.rbxlx "$check_tmp"
python stage8/tests/build_visual_contract.py "$check_tmp"
/workspace/tools/luau-0.744/luau "$check_tmp/logic.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/visual-contract.luau"
/workspace/tools/luau-0.744/luau-compile --null "$check_tmp"/*.luau
python stage8/tests/verify_place.py stage8/original-8.4.rbxlx build/Matterloom_8_5_Prueba_Conexiones.rbxlx
