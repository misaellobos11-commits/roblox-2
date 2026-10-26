from pathlib import Path
import sys
folder=Path(sys.argv[1]);base=Path(__file__).parent
code=(base/'render-engine-adapter.luau').read_text()
for name,var in [('MachineCatalog','Catalog'),('Economy','Economy'),('MachineVisual','Visual')]:
    src=(folder/(name+'.luau')).read_text()
    src='\n'.join(l for l in src.splitlines() if not l.startswith(('local Construction=require','local Catalog=require')))
    if name=='MachineVisual':code+='\nlocal Construction={CELL_SIZE=4}\n'
    code+='\nlocal '+var+'=(function()\n'+src+'\nend)()\n'
code+='''
local Vector2={new=function(x,y)return {X=x,Y=y}end,zero={X=0,Y=0}}
local workspace=Instance.new('Workspace')
workspace.CurrentCamera=Instance.new('Camera')
workspace.CurrentCamera.ViewportSize=Vector2.new(1280,800)
local input=Instance.new('UserInputService')
input.PreferredInput=Enum.PreferredInput.KeyboardAndMouse
local player=Instance.new('Player')
local playerGui=Instance.new('PlayerGui');playerGui.Name='PlayerGui';playerGui.Parent=player
local oldGetService=game.GetService
local baseNew=Instance.new
Instance.new=function(class)
 local instance=baseNew(class)
 if class=='ScreenGui'then instance.AbsoluteSize=Vector2.new(1280,764)end
 return instance
end
game.GetService=function(self,name)
 if name=='Players'then return {LocalPlayer=player}end
 if name=='UserInputService'then return input end
 return oldGetService(self,name)
end
'''
ui=(folder/'BuildUI.luau').read_text()
ui='\n'.join(l for l in ui.splitlines() if not l.startswith(('local Catalog=require','local Economy=require','local Visual=require')))
code+='local UI=(function()\n'+ui+'\nend)()\n'+(base/'catalog-ui.luau').read_text()
if '--height-control' in sys.argv:
    code+=(base/'height-control.luau').read_text()
if '--horizontal' in sys.argv:
    code+=(base/'horizontal-catalog.luau').read_text()
(folder/'catalog-ui.luau').write_text(code)
