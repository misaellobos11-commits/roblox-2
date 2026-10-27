#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_817.py
python stage8/tests/check_side_districts.py build/Matterloom_8_17_Perimetro_Dia_Noche.rbxlx
python stage8/tests/check_perimeter_817.py build/Matterloom_8_17_Perimetro_Dia_Noche.rbxlx
/workspace/tools/luau-0.744/luau stage8/tests/day-night.luau
python stage8/tests/build_day_night_runtime.py build/Matterloom_8_17_Perimetro_Dia_Noche.rbxlx build/day-night-runtime.luau
/workspace/tools/luau-0.744/luau build/day-night-runtime.luau
/workspace/tools/luau-0.744/luau-compile stage8/environment/DayNight.luau stage8/environment/DayNight.server.luau stage8/environment/DayNight.client.luau > /dev/null
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_817.rbxmx
