from pathlib import Path
import sys
folder=Path(sys.argv[1])
p=folder/'logic.luau'
s=p.read_text()
s=s.replace('local Visual={setCargo=function() end}',
    'local transfers={}\nlocal Visual={setCargo=function() end,transferCargo=function(model,item,route) table.insert(transfers,{item=item,route=route}) end}')
test=Path(__file__).with_name('directional-routing.luau').read_text()
s=s.replace("assert(failures==0,tostring(failures)..' regressions failed')",test+"\nassert(failures==0,tostring(failures)..' regressions failed')")
p.write_text(s)
