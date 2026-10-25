from pathlib import Path
import sys
folder=Path(sys.argv[1]);base=Path(__file__).parent
code=(base/'render-engine-adapter.luau').read_text()
code+='\nlocal Catalog=(function()\n'+(folder/'MachineCatalog.luau').read_text()+'\nend)()\n'
visual=(folder/'MachineVisual.luau').read_text()
visual='\n'.join(l for l in visual.splitlines() if not l.startswith(('local Construction=require','local Catalog=require')))
code+='local Construction={CELL_SIZE=4}\nlocal Visual=(function()\n'+visual+'\nend)()\n'
code+=(base/'belt-animation.luau').read_text()
(folder/'belt-animation.luau').write_text(code)
