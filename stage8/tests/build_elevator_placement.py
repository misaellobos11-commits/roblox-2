from pathlib import Path
import sys
folder=Path(sys.argv[1]);base=Path(__file__).parent
controller=(folder/'BuildController.luau').read_text()
manual_height='    actions.height=' in controller
height_action=controller[controller.index('    actions.height='):controller.index('    actions.filter=')] if manual_height else ''
helper=''
if 'local function beltPlacement(' in controller:
    helper=controller[controller.index('local function beltPlacement('):controller.index('function Controller.start(')]
ground=controller[controller.index('    local function groundAt('):controller.index('    local function chooseAt(')]
code="local Color3={fromRGB=function(...)return {...}end}\nlocal Catalog=(function()\n"+(folder/'MachineCatalog.luau').read_text()+'\nend)()\n'
construction=(folder/'Construction.luau').read_text().replace('local Catalog = require(script.Parent.MachineCatalog)','')
code+='local Construction=(function()\n'+construction+'\nend)()\n'+helper
code+='\nlocal clockNow=0\nlocal Visual={setCargo=function()end,transferCargo=function()end}\nlocal Economy=(function()\n'+(folder/'Economy.luau').read_text()+'\nend)()\n'
sim=(folder/'FactorySimulation.luau').read_text()
sim='\n'.join(l for l in sim.splitlines() if not l.startswith(('local Catalog=require','local Visual=require','local Economy=require')))
code+='local Simulation=(function()\n'+sim.replace('os.clock()','clockNow')+'\nend)()\n'
code+='\nlocal manualHeightEnabled='+str(manual_height).lower()+'\n'+'''
local state=Construction.newState(1)
local origin={X=0,Y=0,Z=0}
local buildLevel,rotation=0,0
local mode,selectedId='place',nil
local candidate,dragStroke=nil,nil
local heightOverride,rotationOverride=false,false
local feedbackUntil=math.huge
local plot={FindFirstChild=function()return {}end}
local cameraRay
local PointerRay={fromScreen=function()return cameraRay end}
local GuiService={GetGuiInset=function()return {}end}
local workspace={CurrentCamera={}}
local ui={setHeight=function()end,setStatus=function()end}
local function kind()return 'Belt'end
local function clearPreview()candidate=nil end
local function previewAt()end
local function floorHit()
 local t=-cameraRay.Origin.Y/cameraRay.Direction.Y
 return {X=cameraRay.Origin.X+cameraRay.Direction.X*t,Y=0,Z=cameraRay.Origin.Z+cameraRay.Direction.Z*t}
end
local function ray()return {Position=floorHit()}end
local function floorCell()
 local p=floorHit();local x,z=Construction.worldToCell(p.X,p.Z,0,0)
 return {x=x,z=z}
end
local function aim(x,z,level)
 local wx,wz=(x+.5)*4,(z+.5)*4
 local y=.9+level*8
 cameraRay={Origin={X=wx-(40-y)*.3,Y=40,Z=wz-(40-y)},Direction={X=.3,Y=-1,Z=1}}
end
local pending=false
local lastSent
local dragGhost={ClearAllChildren=function()end}
local actions={}
local function placing()return mode=='place' or mode=='move'end
local function refresh()end
local function feedback()end
local function send(command)lastSent=command end
ui.containsPoint=function()return false end
'''+ground+'\n'+controller[controller.index('    local function strokeKey'):controller.index('    local function drawStroke')]+'''
local function drawStroke()end
'''+controller[controller.index('    local function addStrokeCell'):controller.index('    actions.catalog=')]+height_action+'\n'+(base/'elevator-placement.luau').read_text()
(folder/'elevator-placement.luau').write_text(code)
if '--all-transport' in sys.argv:
    code=code.replace("local function kind()return 'Belt'end", "local testKind='Belt'\nlocal function kind()return testKind end")
    code+='\n'+(base/'auto-transport-placement.luau').read_text()
    (folder/'elevator-placement.luau').write_text(code)
