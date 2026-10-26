"""Exercise the real loader, plot builder, ownership presentation and spawn facing."""
from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET
folder=Path(sys.argv[1]);base=Path(__file__).parent
root=ET.parse(sys.argv[2]).getroot()
world=next(i for i in root.iter('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomWorld')
code=(base/'render-engine-adapter.luau').read_text()+'\nlocal Vector2={new=function(x,y)return {X=x,Y=y}end}\nlocal workspace=Instance.new("Folder")\n'
lines=[]
def fixture(item,parent):
    n='o'+str(len(lines));lines.append('')
    name=item.findtext("Properties/string[@name='Name']")
    lines[-1]=f'local {n}=Instance.new({json.dumps(item.get("class"))});{n}.Name={json.dumps(name)};{n}.Parent={parent}'
    position=item.find("Properties/CoordinateFrame[@name='CFrame']")
    if position is not None:
        values=','.join(position.findtext(a) for a in 'XYZ')
        lines[-1]+=f';{n}.Position=Vector3.new({values})'
    for child in item.findall('Item'):fixture(child,n)
fixture(world,'workspace')
# Separate lexical scopes avoid Luau's 200-local limit for the imported scene fixture.
code+='do\n'+ '\n'.join(line.replace('local o','o',1) for line in lines)+'\nend\n'
code+='local MapConfig=(function()\n'+(folder/'MapConfig.luau').read_text()+'\nend)()\n'
code+='local MapGenerator=(function()\n'+(folder/'MapGenerator.luau').read_text()+'\nend)()\n'
code+='local Construction={GRID_SIZE=48,CELL_SIZE=4}\n'
server=(folder/'BuildServer.luau').read_text()
code+=server[server.index('local CYAN ='):server.index('local function redrawBelts')]
code+=server[server.index('local function setPlotOwner'):server.index('function BuildServer.start')]
code+='local sessions={}\n'+server[server.index('    local function moveCharacter'):server.index('    getPlots.OnServerInvoke')]
code+='''
local world=workspace:FindFirstChild('MatterloomWorld')
assert(world:FindFirstChild('PreviewPlots'))
local count=#world:GetDescendants()
local spawn=MapGenerator.build()
assert(spawn.Name=='MatterloomLobbySpawn' and spawn:IsA('SpawnLocation'))
assert(not world:FindFirstChild('PreviewPlots'),'preview floors were not removed')
local remaining=#world:GetDescendants()
assert(remaining<count and MapGenerator.build()==spawn and #world:GetDescendants()==remaining,'loader duplicated world/spawn')
local plots=Instance.new('Folder');plots.Parent=workspace
for slot=1,8 do
 local info=createVacantPlot(plots,slot)
 local center=MapConfig.plotCenter(slot)
 local direction=MapConfig.entryDirection(slot)
 assert((info.origin+Vector3.new(96,0,96)-center).Magnitude<1e-6)
 assert((info.spawn.Position-MapConfig.entryPoint(slot)-Vector3.new(0,.5,0)).Magnitude<1e-6)
 local floor=info.model:FindFirstChild('BuildFloor')
 assert(floor.Size.X==192 and floor.Size.Z==192 and floor.Position.Y==-.5)
 local entry=info.model:FindFirstChild('Entrada')
 assert((direction.X==0 and entry.Size.X==28 and entry.Size.Z==24)
     or (direction.Z==0 and entry.Size.X==24 and entry.Size.Z==28),'side entrance was not rotated')
 local character={WaitForChild=function()return {}end,PivotTo=function(self,cf)self.frame=cf end}
 local player={UserId=slot+100,DisplayName='Tester '..slot,Character=character}
 setPlotOwner(info,player)
 assert(info.model.Name=='Plot_'..player.UserId and floor:GetAttribute('OwnerUserId')==player.UserId)
 local session={slot=slot,spawn=info.spawn};sessions[player]=session
 moveCharacter(player,character,session)
 assert((character.frame.Position-info.spawn.Position-Vector3.new(0,4,0)).Magnitude<1e-6)
 assert((character.frame:VectorToWorldSpace(Vector3.new(0,0,-1))+direction).Magnitude<1e-6,'spawn faces away from plot')
 setPlotOwner(info,nil)
 assert(info.model.Name=='PlotSlot_'..slot and floor:GetAttribute('OwnerUserId')==0)
 assert(string.find(info.sign.Text,'LIBRE'))
end
assert(#plots:GetChildren()==8)
print('PASS actual canyon loader and eight plots: preview cleanup, origins, entry widths, ownership reset and respawn facing')
'''
(folder/'canyon-runtime.luau').write_text(code)
if '--quiet-plots' in sys.argv:
    code+='''
for _,model in plots:GetChildren()do
 assert(#model:FindFirstChild('Grid'):GetChildren()==0,'server should not replicate grid lines')
 local board=model:FindFirstChild('PlacaParcela')
 assert(board and board.Size.X==14 and board.Size.Y==4,'physical entrance sign missing')
 local sign=board:FindFirstChild('CartelParcela')
 assert(sign:IsA('SurfaceGui') and not sign.AlwaysOnTop and sign.MaxDistance<=72,'sign still overlays the world from afar')
 assert(sign:FindFirstChild('Estado').TextScaled)
end
print('PASS quiet plots: no replicated grid and eight bounded physical entrance signs')
'''
    (folder/'canyon-runtime.luau').write_text(code)
