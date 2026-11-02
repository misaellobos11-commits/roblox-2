#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_822.py
folder=build/822-sources
python stage8/tests/build_regressions.py build/Matterloom_8_22_Maquinas_Redisenadas.rbxlx "$folder"
python stage8/tests/build_expansion.py "$folder"
python stage8/tests/build_cargo_models.py "$folder"
python stage8/tests/build_expansion_visual.py "$folder"
cat stage8/tests/polish-visual.luau >> "$folder/expansion-visual.luau"
python stage8/tests/build_catalog_ui.py "$folder" --horizontal --contextual
cat stage8/tests/expansion-ui.luau >> "$folder/catalog-ui.luau"
python stage8/tests/build_belt_animation.py "$folder"
python stage8/tests/build_functional_visual.py "$folder" --transport-only
for name in expansion-test expansion-visual expansion-cargo catalog-ui belt-animation functional-visual; do
    /workspace/tools/luau-0.744/luau "$folder/$name.luau"
done
/workspace/tools/luau-0.744/luau-compile "$folder/MachineVisual.luau" > /dev/null
/workspace/tools/luau-0.744/luau-compile "$folder/BuildUI.luau" > /dev/null
python stage8/expansion/preview_822.py
python stage8/tests/check_canyon_schema.py build/Expansion_822_Preview.rbxmx
