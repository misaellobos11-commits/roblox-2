-- UI behavior under an Instance adapter: real creation and event handlers run.
local chosen=nil
local ui=UI.new({choose=function(kind)chosen=kind end})
local screen=ui.screen
local detail=screen:FindFirstChild('DetalleMaquina')
assert(detail,'right-hand description panel was removed')
for _,name in ipairs({'DetalleNombre','Descripcion','Insumos','Productos','Notas'})do
 local text=detail:FindFirstChild(name)
 assert(text.TextWrapped and text.AutomaticSize==Enum.AutomaticSize.Y,'right-hand text must grow without clipping: '..name)
end
assert(detail.AutomaticCanvasSize==Enum.AutomaticSize.Y,'expanded details need scrollable content height')
assert(ui.catalog:FindFirstChild('Categories'):IsA('ScrollingFrame'),'narrow category tabs must scroll rather than crush their labels')
ui:setCatalogOpen(true)
local cards=0
for typ,b in pairs(ui.machineButtons)do
 local view=b:FindFirstChild('Miniatura')
 assert(view and view:IsA('ViewportFrame'),'catalog card needs a real object thumbnail: '..typ)
 assert(view.CurrentCamera and view:FindFirstChildOfClass('WorldModel'),'thumbnail needs camera and model')
 assert(b.Text=='','object name still covers the thumbnail')
 assert(b:FindFirstChild('Precio'),'price must remain visible')
 b.MouseEnter:Fire()
 assert(detail:FindFirstChild('DetalleNombre').Text==Catalog.types[typ].name:upper(),'hover does not update right-hand name')
 assert(detail:FindFirstChild('Descripcion').Text==Catalog.types[typ].description,'right-hand description changed')
 b.MouseLeave:Fire()
 b.Activated:Fire()
 assert(chosen==typ,'thumbnail selection does not choose the object')
 cards+=1
end
ui:setFactory({cash=100000,lifetimeRevenue=1000000,techTier=5},nil,0,'select')
ui:setMode('place',nil,false,'Receiver')
for _,b in pairs(ui.machineButtons)do assert(b.Text=='','economy refresh overwrote thumbnail with name')end
ui:setMode('place',nil,true,'Receiver')
for _,b in pairs(ui.machineButtons)do assert(not b.Interactable,'pending action should disable purchases')end
ui:setFactory({cash=100000,lifetimeRevenue=1000000,techTier=5},nil,0,'place')
for _,b in pairs(ui.machineButtons)do assert(not b.Interactable,'economy refresh re-enabled a pending purchase')end
ui:setMode('select',nil,false,nil)
ui:setFactory({cash=0,lifetimeRevenue=0,techTier=1},nil,0,'select')
assert(not ui.machineButtons.Receiver.Interactable,'unaffordable card must not buy')
assert(string.find(ui.machineButtons.Smelter:FindFirstChild('Precio').Text,'NIVEL'),'locked price badge must explain level requirement')
print('PASS catalog thumbnails, details, selection and purchase state: '..cards..' cards')
for _,size in ipairs({{1280,800},{900,640},{800,480},{640,360},{390,844}})do
 workspace.CurrentCamera.ViewportSize=Vector2.new(size[1],size[2])
 -- ScreenGui's usable coordinates exclude Roblox's 36px top bar.
 ui.screen.AbsoluteSize=Vector2.new(size[1],size[2]-36)
 ui:setCatalogOpen(true)
 local function rect(frame)
  local w,h=frame.Size.X.Offset,frame.Size.Y.Offset
  local x=frame.Position.X.Scale*size[1]+frame.Position.X.Offset-frame.AnchorPoint.X*w
  local y=frame.Position.Y.Scale*(size[2]-36)+frame.Position.Y.Offset-frame.AnchorPoint.Y*h
  return x,y,w,h
 end
 local x,y,w,h=rect(ui.catalog)
 local dx,dy,dw,dh=rect(detail)
 assert(x>=0 and y>=0 and x+w<=size[1] and y+h<=size[2]-36,'catalog clipped outside viewport')
 assert(dx>=x+w and dy>=0 and dx+dw<=size[1] and dy+dh<=size[2]-36,'description overlaps catalog or leaves usable viewport')
 assert(math.abs(y-dy)<1e-4,'catalog and description ignore different GUI insets')
 assert(detail.Visible,'description must stay on the right')
end
print('PASS catalog and right detail bounds in desktop, tablet, landscape and narrow layouts')
