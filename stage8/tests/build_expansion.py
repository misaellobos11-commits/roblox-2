"""Execute real extracted catalog/construction/simulation with only service adapters."""
from pathlib import Path
import sys
folder=Path(sys.argv[1]);base=Path(__file__).parent
code="local Color3={fromRGB=function(...) return {...} end}\n"
for name,var in [('MachineCatalog','Catalog'),('Economy','Economy'),('Construction','Construction')]:
    source=(folder/(name+'.luau')).read_text()
    source='\n'.join(l for l in source.splitlines() if 'require(' not in l)
    code+='local '+var+'=(function()\n'+source+'\nend)()\n'
code+='local clockNow=0\nlocal Visual={setCargo=function()end,transferCargo=function()end}\n'
source=(folder/'FactorySimulation.luau').read_text()
source='\n'.join(l for l in source.splitlines() if not l.startswith(('local Catalog=require','local Visual=require','local Economy=require')))
code+='local Simulation=(function()\n'+source.replace('os.clock()','clockNow')+'\nend)()\n'
code+=(base/'expansion.luau').read_text()
if (folder/'ExpansionDemo.luau').exists():
    demo=(folder/'ExpansionDemo.luau').read_text()
    demo='\n'.join(l for l in demo.splitlines() if 'require(' not in l)
    code+='\nlocal ExpansionDemo=(function()\n'+demo+'\nend)()\n'+(base/'expansion-demo.luau').read_text()
(folder/'expansion-test.luau').write_text(code)
