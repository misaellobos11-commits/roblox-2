from pathlib import Path
import sys
folder=Path(sys.argv[1]);tests=Path(__file__).parent
code=(tests/'render-engine-adapter.luau').read_text()
code+='\nlocal Catalog=(function()\n'+(folder/'MachineCatalog.luau').read_text()+'\nend)()\nlocal Construction={CELL_SIZE=4}\n'
source=(folder/'MachineVisual.luau').read_text()
source='\n'.join(l for l in source.splitlines() if not l.startswith(('local Construction=require','local Catalog=require')))
code+='local Visual=(function()\n'+source+'\nend)()\n'+(tests/'expansion-visual.luau').read_text()
(folder/'expansion-visual.luau').write_text(code)
# Reuse every existing cargo motion/clearance assertion for the expanded catalog.
code=(folder/'cargo-models.luau').read_text().replace("count==14", "count==54").replace('all 14 resource','all 54 resource')
(folder/'expansion-cargo.luau').write_text(code)
