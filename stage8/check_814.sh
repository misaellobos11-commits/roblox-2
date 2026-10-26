#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
check_tmp=$(mktemp -d)
trap 'rm -rf "$check_tmp"' EXIT
python stage8/build_814.py
python stage8/tests/build_regressions.py build/Matterloom_8_14_Entorno_y_HUD.rbxlx "$check_tmp"
python stage8/tests/build_belt_regressions.py "$check_tmp"
python stage8/tests/build_directional_regressions.py "$check_tmp"
python stage8/tests/build_functional_visual.py "$check_tmp" --transport-only
python stage8/tests/build_visual_contract.py "$check_tmp" --machines
python stage8/tests/build_catalog_ui.py "$check_tmp" --horizontal --contextual
python stage8/tests/build_belt_animation.py "$check_tmp"
python stage8/tests/build_three_model_regressions.py "$check_tmp"
python stage8/tests/build_elevator_placement.py "$check_tmp" --all-transport
python stage8/tests/build_default_selection.py "$check_tmp" --local-grid
/workspace/tools/luau-0.744/luau "$check_tmp/default-selection.luau"
python stage8/tests/build_canyon_runtime.py "$check_tmp" build/Matterloom_8_14_Entorno_y_HUD.rbxlx --quiet-plots
/workspace/tools/luau-0.744/luau "$check_tmp/canyon-runtime.luau"
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
python stage8/tests/test_canyon.py build/Matterloom_8_13_Catalogo_Horizontal.rbxlx build/Matterloom_8_14_Entorno_y_HUD.rbxlx --814
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_814.rbxmx
