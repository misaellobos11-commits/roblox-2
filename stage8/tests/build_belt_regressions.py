"""Execute shipped planner and geometry builders; rendering is recorded, not run in Studio."""
from pathlib import Path
import sys

folder=Path(sys.argv[1])
logic=folder/'logic.luau'
source=logic.read_text()
source=source.replace("assert(failures==0,tostring(failures)..' regressions failed')",Path(__file__).with_name('belt-flow.luau').read_text()+"\nassert(failures==0,tostring(failures)..' regressions failed')")
logic.write_text(source)
visual=(folder/'MachineVisual.luau').read_text()
start=visual.find('local function createBeltStraight(')
if start<0:start=visual.index('local function createBeltBend(')
body=visual[start:visual.index('-- ETAPA 5:')]
prelude=Path(__file__).with_name('belt-render-adapter.luau').read_text()
tests=Path(__file__).with_name('belt-render.luau').read_text()
(folder/'belt-render.luau').write_text(prelude+'\n'+body+'\n'+tests)
controller=(folder/'BuildController.luau').read_text()
planner=controller[controller.index('    local function flowRotation'):controller.index('    local function clearStroke')]
draw=controller[controller.index('    local function drawStroke'):controller.index('    local function addStrokeCell')]
catalog=(folder/'MachineCatalog.luau').read_text()
preview=prelude+'\nlocal Catalog=(function()\n'+catalog+'\nend)()\n'
preview+='''
local Construction={CELL_SIZE=4}
local rotation,buildLevel=0,0
local origin=Vector3.new(100,7,200)
local dragGhost=object('Ghosts')
function dragGhost:ClearAllChildren() self.children={} end
local dragStroke=nil
local ui={setStatus=function()end}
CFrame.lookAt=function(position,target)return {position=position,target=target}end
Enum.Material.SmoothPlastic=0
local newInstance=Instance.new
Instance.new=function(class)
 local instance=newInstance(class)
 function instance:Clone()
  local clone=Instance.new(class)
  for k,v in pairs(self) do if k~='Parent' and k~='children' then clone[k]=v end end
  return clone
 end
 return instance
end
'''+planner+draw+Path(__file__).with_name('belt-preview.luau').read_text()
(folder/'belt-preview.luau').write_text(preview)
