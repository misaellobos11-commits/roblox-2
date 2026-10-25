from pathlib import Path
import sys
folder=Path(sys.argv[1])
base=Path(__file__).parent
visual=(folder/'MachineVisual.luau').read_text()
visual='\n'.join(line for line in visual.splitlines() if not line.startswith(('local Construction=require','local Catalog=require')))
code=(base/'render-engine-adapter.luau').read_text()
code+='\nlocal Catalog=(function()\n'+(folder/'MachineCatalog.luau').read_text()+'\nend)()\n'
code+='local Construction={CELL_SIZE=4}\nlocal Visual=(function()\n'+visual+'\nend)()\n'
code+=(base/'transfer-visual.luau').read_text()
code+=(base/'functional-visual.luau').read_text()
(folder/'functional-visual.luau').write_text(code)
