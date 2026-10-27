#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_820.py
python stage8/tests/build_cargo_models.py build/820-sources
python stage8/tests/build_belt_animation.py build/820-sources
python stage8/tests/build_functional_visual.py build/820-sources --transport-only
/workspace/tools/luau-0.744/luau build/820-sources/cargo-models.luau
/workspace/tools/luau-0.744/luau build/820-sources/belt-animation.luau
/workspace/tools/luau-0.744/luau build/820-sources/functional-visual.luau
/workspace/tools/luau-0.744/luau-compile build/820-sources/MachineVisual.luau > /dev/null
python stage8/visuals/preview_cargo.py
python stage8/tests/check_canyon_schema.py build/Cargo_820_Preview.rbxmx
