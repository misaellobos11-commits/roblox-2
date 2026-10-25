from pathlib import Path
import sys

folder=Path(sys.argv[1]);base=Path(__file__).parent
visual=(folder/'MachineVisual.luau').read_text()
installer=visual[visual.index('local visualKeys='):visual.index('local function importedLabel')]
code=(base/'import-adapter.luau').read_text()
code+='\nlocal Catalog=(function()\n'+(folder/'MachineCatalog.luau').read_text()+'\nend)()\n'
code+=installer+'\n'+(base/'three-model-orientation.luau').read_text()
(folder/'three-model-orientation.luau').write_text(code)
