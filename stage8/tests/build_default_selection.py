"""Run the complete controller and its actual input/remote callbacks with service adapters."""
from pathlib import Path
import sys
folder=Path(sys.argv[1]);base=Path(__file__).parent
code=(base/'render-engine-adapter.luau').read_text()
code+='\nlocal Catalog=(function()\n'+(folder/'MachineCatalog.luau').read_text()+'\nend)()\n'
construction=(folder/'Construction.luau').read_text().replace('local Catalog = require(script.Parent.MachineCatalog)','')
code+='local Construction=(function()\n'+construction+'\nend)()\n'
code+='''
function Methods:ClearAllChildren()for _,c in self:GetChildren()do c:Destroy()end end
function Methods:FindFirstAncestorOfClass(class)
 local p=self.Parent;while p do if p:IsA(class)then return p end;p=p.Parent end
end
local Vector2={new=function(x,y)return Vector3.new(x,y,0)end,zero=Vector3.zero}
local RaycastParams={new=function()return {}end}
local workspace=Instance.new('Workspace');workspace.CurrentCamera=Instance.new('Camera')
local player=Instance.new('Player');player.UserId=1;player.CharacterAdded=signal()
local Players={LocalPlayer=player}
local plotFolder=Instance.new('Folder');plotFolder.Name='MatterloomPlots';plotFolder.Parent=workspace
local plot=Instance.new('Model');plot.Name='Plot_1';plot.Parent=plotFolder
local floor=Instance.new('Part');floor.Name='BuildFloor';floor.Parent=plot
local machines=Instance.new('Folder');machines.Name='Machines';machines.Parent=plot
local serverState=Construction.newState(1)
for _,rec in ipairs({{machineType='Receiver',x=2,z=2},{machineType='FusionChamber',x=8,z=8}})do
 rec.kind='place';rec.rotation=0;rec.level=0
 local ok,_,id=Construction.apply(serverState,1,rec);assert(ok)
 local model=Instance.new('Model');model.Name=rec.machineType..'_'..id;model.Parent=machines
 model:SetAttribute('OwnerUserId',1);model:SetAttribute('BuildingId',id)
 local part=Instance.new('Part');part.Name='Base';part.Parent=model
end
local hitId=nil
local mouse=Vector2.new(10,10)
function workspace:Raycast(rayOrigin,rayDirection,params)
 if params.FilterDescendantsInstances[1]==floor then return {Instance=floor,Position=Vector3.new(mouse.X,0,mouse.Y)}end
 if hitId then
  for _,model in machines:GetChildren()do
   if model:GetAttribute('BuildingId')==hitId then return {Instance=model:FindFirstChild('Base')}end
  end
 end
 return nil
end
local PointerRay={fromScreen=function()return {Origin=Vector3.new(mouse.X,40,mouse.Y),Direction=Vector3.new(0,-1,0)}end}
local UserInputService={InputBegan=signal(),InputEnded=signal(),TouchTapInWorld=signal(),PreferredInput='KeyboardAndMouse',
 GetFocusedTextBox=function()return nil end,GetMouseLocation=function()return mouse end}
local RunService={RenderStepped=signal()}
local GuiService={MenuOpened=signal(),GetGuiInset=function()return Vector2.zero end}
local ReplicatedStorage=Instance.new('Folder')
local remotes=Instance.new('Folder');remotes.Name='Matterloom';remotes.Parent=ReplicatedStorage
local lastSent,sends=nil,0
local commandEvent
for _,n in ipairs({'Command','FactoryState','GetState'})do
 local remote=Instance.new('RemoteEvent');remote.Name=n;remote.Parent=remotes;remote.OnClientEvent=signal()
 remote.FireServer=function(_,order)lastSent=order;sends+=1 end
 if n=='Command'then commandEvent=remote end
end
local actions,uiState,overUI
uiState={}
local UI={new=function(callbacks)
 actions=callbacks
 return {
  setMode=function(_,mode,id,pending,chosen,count,confirmation)
   uiState.mode=mode;uiState.id=id;uiState.pending=pending;uiState.count=count;uiState.confirmation=confirmation
  end,
  setStatus=function(_,message)uiState.message=message end,
  setDetails=function(_,typ)uiState.detail=typ end,
  setCount=function()end,setFactory=function()end,setHeight=function()end,setCatalogOpen=function()end,
  containsPoint=function()return overUI==true end,
 }
end}
local Visual={create=function()return Instance.new('Model')end,pivot=function()end,setPreview=function()end,setBeltIncoming=function()end}
'''
controller=(folder/'BuildController.luau').read_text()
code+='local Controller=(function()\n'+controller[controller.index('local Controller={}'):]+ '\nend)()\n'
code+='''
Controller.start({state=Construction.snapshot(serverState),origin=Vector3.zero,factory={cash=700}})
local function click(id)
 hitId=id
 UserInputService.InputBegan:Fire({UserInputType='MouseButton1'},false)
 UserInputService.InputEnded:Fire({UserInputType='MouseButton1'})
end
local function reply(code,id)
 commandEvent.OnClientEvent:Fire({ok=true,code=code,id=id,state=Construction.snapshot(serverState)})
end
click(1)
assert(uiState.id==1 and uiState.count==1 and uiState.detail=='Receiver','first click should retain single-machine details')
click(2)
assert(uiState.id==nil and uiState.count==2,'multiple selection is not the default')
actions.move();assert(uiState.mode=='select','group must not move as a single machine')
actions.recipe();assert(sends==0,'group must not configure one machine')
click(2);assert(uiState.id==1 and uiState.count==1,'second click should unmark')
actions.move();assert(uiState.mode=='move','single selected machine cannot move')
actions.cancel();assert(uiState.mode=='select' and uiState.count==0,'cancel did not restore default selection')
-- Rectangle gestures work immediately after cancel, without a V mode toggle.
hitId=nil;mouse=Vector2.new(0,0)
UserInputService.InputBegan:Fire({UserInputType='MouseButton1'},false)
mouse=Vector2.new(40,40)
RunService.RenderStepped:Fire(.1)
UserInputService.InputEnded:Fire({UserInputType='MouseButton1'})
assert(uiState.count==2 and uiState.id==nil,'area drag did not select both machines')
actions.bulkRemove();assert(sends==0 and uiState.confirmation,'first delete must require confirmation')
actions.bulkRemove();assert(lastSent.kind=='remove_many' and #lastSent.ids==2 and sends==1,'second delete must send both IDs')
actions.bulkRemove();assert(sends==1,'pending delete was submitted twice')
reply('removed_many')
assert(uiState.count==0 and uiState.mode=='select','server acknowledgement disabled default selection')
click(1);assert(uiState.count==1)
overUI=true;click(2);assert(uiState.count==1,'clicking UI changed selection');overUI=false
click(nil);assert(uiState.count==0,'clicking empty floor should clear selection')
-- T and V no longer change height or disable multi-selection.
assert(actions.height==nil and actions.bulk==nil,'obsolete callbacks remain')
UserInputService.InputBegan:Fire({KeyCode='T'},false)
UserInputService.InputBegan:Fire({KeyCode='V'},false)
click(1);click(2);assert(uiState.count==2)
for _,case in ipairs({{'demo','demo'},{'productionDemo','demo_production'},{'megaDemo','demo_mega'}})do
 actions[case[1]]();assert(lastSent.kind==case[2],'demo action lost in default selection')
 reply(case[2]);assert(uiState.mode=='select' and uiState.count==0)
end
-- Existing server feedback may select the newly placed/configured machine.
reply('placed',1);assert(uiState.id==1 and uiState.count==1)
actions.cancel();hitId=1
UserInputService.TouchTapInWorld:Fire(mouse,false)
hitId=2;UserInputService.TouchTapInWorld:Fire(mouse,false)
assert(uiState.count==2,'touch cannot add multiple machines')
player.CharacterAdded:Fire();assert(uiState.count==0 and uiState.mode=='select')
print('PASS full controller: default click/rectangle/touch selection, single actions, confirmed group deletion, acknowledgements, demos and removed T/V toggles')
local ok,_,elevatorId=Construction.apply(serverState,1,{kind='place',machineType='ElevatorUp',x=10,z=10,rotation=0,level=0})
assert(ok);reply('placed',elevatorId)
local elevator=serverState.buildings[elevatorId]
for _,case in ipairs({{'SplitterLeft','output'},{'FilterLeft','input'}})do
 local port=Catalog.port(elevator,case[2])
 mouse=Vector2.new((port.x+port.dx*.5)*4,(port.z+port.dz*.5)*4)
 actions.choose(case[1])
 RunService.RenderStepped:Fire(.1)
 lastSent=nil;actions.confirm()
 assert(lastSent and lastSent.machineType==case[1] and lastSent.level==port.level,'transport confirmation sent the wrong height/type')
 local device={id=100,machineType=lastSent.machineType,x=lastSent.x,z=lastSent.z,rotation=lastSent.rotation,level=lastSent.level}
 assert(if case[2]=='output' then Catalog.connected(elevator,device) else Catalog.connected(device,elevator))
 reply('placed')
end
print('PASS full controller confirms splitter above and filter below without manual height')
'''
(folder/'default-selection.luau').write_text(code)
if '--local-grid' in sys.argv:
    code+='''
actions.cancel()
local function gridLines()return plot:FindFirstChild('Grid'):GetChildren()end
for _,line in gridLines()do assert(line.Transparency==1,'grid remains visible while idle')end
actions.choose('Belt')
assert(#gridLines()==98,'owner construction grid missing')
for _,line in gridLines()do
 assert(line.Transparency>=.66 and line.Transparency<1 and not line.CanQuery and not line.CanCollide and not line.CastShadow)
end
local port=Catalog.port(elevator,'output')
mouse=Vector2.new((port.x+port.dx*.5)*4,(port.z+port.dz*.5)*4)
RunService.RenderStepped:Fire(.1)
for _,line in gridLines()do assert(math.abs(line.Position.Y-8.035)<1e-6,'grid did not follow automatically elevated preview')end
actions.catalog()
for _,line in gridLines()do assert(line.Transparency==1,'catalog opening leaves grid visible')end
actions.catalog()
for _,line in gridLines()do assert(line.Transparency<1)end
actions.cancel()
for _,line in gridLines()do assert(line.Transparency==1)end
print('PASS local grid: shown only for construction, follows automatic height, hides on catalog/cancel')
'''
    (folder/'default-selection.luau').write_text(code)
