#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
check_tmp=$(mktemp -d)
trap 'rm -rf "$check_tmp"' EXIT
python stage8/build_811.py
python stage8/tests/build_regressions.py build/Matterloom_8_11_Conexiones_Ascensores.rbxlx "$check_tmp"
python stage8/tests/build_belt_regressions.py "$check_tmp"
python stage8/tests/build_directional_regressions.py "$check_tmp"
python stage8/tests/build_functional_visual.py "$check_tmp" --transport-only
python stage8/tests/build_visual_contract.py "$check_tmp" --machines
python stage8/tests/build_catalog_ui.py "$check_tmp" --height-control
python stage8/tests/build_belt_animation.py "$check_tmp"
python stage8/tests/build_three_model_regressions.py "$check_tmp"
python stage8/tests/build_elevator_placement.py "$check_tmp"
/workspace/tools/luau-0.744/luau "$check_tmp/elevator-placement.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/three-model-orientation.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/logic.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/functional-visual.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/visual-contract.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/belt-render.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/belt-preview.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/belt-animation.luau"
/workspace/tools/luau-0.744/luau "$check_tmp/catalog-ui.luau"
/workspace/tools/luau-0.744/luau-compile --null "$check_tmp"/*.luau
python stage8/tests/verify_place.py build/Matterloom_8_10_Tres_Modelos.rbxlx build/Matterloom_8_11_Conexiones_Ascensores.rbxlx --811-delta
