#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_819.py
python stage8/tests/check_horizon_819.py build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx
python stage8/tests/check_lighting_818.py build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx
python stage8/tests/build_day_night_runtime.py build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx build/day-night-819-runtime.luau --clear-night --sky
/workspace/tools/luau-0.744/luau build/day-night-819-runtime.luau
python - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
r=ET.parse('build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx').getroot()
i=next(i for i in r.iter('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomDayNightClient')
Path('build/day-night-819-client.luau').write_text(i.findtext("Properties/ProtectedString[@name='Source']"))
PY
/workspace/tools/luau-0.744/luau-compile build/day-night-819-client.luau > /dev/null
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_819.rbxmx
python stage8/tests/check_sky_schema.py build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx
