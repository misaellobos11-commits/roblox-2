#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_818.py
python stage8/tests/check_lighting_818.py build/Matterloom_8_18_Noche_Clara_y_Focos.rbxlx
python stage8/tests/build_day_night_runtime.py build/Matterloom_8_18_Noche_Clara_y_Focos.rbxlx build/day-night-818-runtime.luau --clear-night
/workspace/tools/luau-0.744/luau build/day-night-818-runtime.luau
python - <<'PY'
from pathlib import Path
s=Path('stage8/tests/day-night.luau').read_text().replace("require('../environment/DayNight')", "require('./818-scripts/MatterloomDayNight')")
Path('build/day-night-818-palette.luau').write_text(s)
PY
/workspace/tools/luau-0.744/luau build/day-night-818-palette.luau
/workspace/tools/luau-0.744/luau-compile build/818-scripts/MatterloomDayNight.luau build/818-scripts/MatterloomDayNightClient.luau build/818-scripts/MatterloomDayNightServer.luau > /dev/null
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_818.rbxmx
