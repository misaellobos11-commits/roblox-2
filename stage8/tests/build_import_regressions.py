"""Run the actual asset installer with transform-aware Roblox boundary adapters.

Native mouth/arrow axes are calibration fixtures inferred from the reported
screenshots, not decoded mesh vertices. Studio playtest must confirm them.
"""
from pathlib import Path
import sys

folder=Path(sys.argv[1])
visual=(folder/'MachineVisual.luau').read_text()
catalog=(folder/'MachineCatalog.luau').read_text()
installer=visual[visual.index('local visualKeys='):visual.index('local function importedLabel')]
adapter=Path(__file__).with_name('import-adapter.luau').read_text()
tests=Path(__file__).with_name('import-orientation.luau').read_text()
code=adapter+'\nlocal Catalog=(function()\n'+catalog+'\nend)()\n'+installer+'\n'+tests
(folder/'import-orientation.luau').write_text(code)
