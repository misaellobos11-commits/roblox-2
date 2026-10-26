#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python stage8/build_815.py
python stage8/tests/check_canyon_schema.py build/Matterloom_Canyon_World_815.rbxmx
