#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_816.py
python stage8/tests/check_side_districts.py build/Matterloom_8_16_Sectores_Laterales.rbxlx
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_816.rbxmx
