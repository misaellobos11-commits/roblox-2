#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_821.py
folder=build/821-sources
python stage8/tests/build_regressions.py build/Matterloom_8_21_Expansion_Industrial.rbxlx "$folder"
python stage8/tests/build_expansion.py "$folder"
python stage8/tests/build_cargo_models.py "$folder"
python stage8/tests/build_expansion_visual.py "$folder"
python stage8/tests/build_catalog_ui.py "$folder" --horizontal --contextual
cat stage8/tests/expansion-ui.luau >> "$folder/catalog-ui.luau"
python stage8/tests/build_belt_animation.py "$folder"
python stage8/tests/build_functional_visual.py "$folder" --transport-only
python stage8/tests/build_belt_regressions.py "$folder"
python stage8/tests/build_directional_regressions.py "$folder"
python stage8/tests/build_elevator_placement.py "$folder" --all-transport
for name in expansion-test expansion-visual expansion-cargo catalog-ui belt-animation functional-visual logic belt-render belt-preview elevator-placement; do
    /workspace/tools/luau-0.744/luau "$folder/$name.luau"
done
for name in MachineCatalog Economy MachineVisual BuildUI BuildController BuildServer ExpansionDemo; do
    /workspace/tools/luau-0.744/luau-compile "$folder/$name.luau" > /dev/null
done
python stage8/expansion/preview.py
python stage8/tests/check_canyon_schema.py build/Expansion_821_Preview.rbxmx
