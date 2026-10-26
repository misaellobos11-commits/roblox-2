ui.screen.AbsoluteSize=Vector2.new(1280,764)
ui:setCatalogOpen(false);ui:setDetails(nil)
ui:setMode('select',nil,false,nil,0,false)
local dock=ui.screen:FindFirstChild('ConstructionActions')
local demos=ui.screen:FindFirstChild('Pruebas')
assert(not dock.Visible,'idle HUD still covers the lower world')
assert(not demos.Visible and ui.screen:FindFirstChild('IdleHint').Visible)
assert(ui.screen:FindFirstChild('Header').Size.Y.Offset==64)
for _,b in dock:FindFirstChild('Actions'):GetChildren()do
 if b:IsA('TextButton')then assert(not b.Visible,'idle actions should disappear')end
end
ui:setMode('place',nil,false,'Belt',0,false)
assert(dock.Visible and dock.Size.Y.Offset<=110 and dock.Size.X.Offset<=620)
assert(ui.actions.rotate.Visible and ui.actions.confirm.Visible and ui.actions.cancel.Visible)
assert(not ui.actions.move.Visible and not ui.actions.bulkRemove.Visible and not ui.actions.recipe.Visible)
ui:setMode('select',1,false,'Receiver',1,false)
assert(ui.actions.move.Visible and ui.actions.bulkRemove.Visible and not ui.actions.recipe.Visible and not ui.actions.filter.Visible)
ui:setMode('select',1,false,'FusionChamber',1,false)
assert(ui.actions.recipe.Visible and ui.actions.recipe.Interactable)
ui:setMode('select',1,false,'FilterLeft',1,false)
assert(ui.actions.filter.Visible and ui.actions.filter.Interactable and not ui.actions.recipe.Visible)
ui:setMode('select',nil,false,nil,3,false)
assert(ui.actions.cancel.Visible and ui.actions.bulkRemove.Visible and not ui.actions.move.Visible)
ui.screen:FindFirstChild('AbrirPruebas').Activated:Fire()
assert(demos.Visible and not dock.Visible,'demos did not move into a separate menu')
for _,key in ipairs({'demo','productionDemo','megaDemo'})do
 assert(ui.actions[key].Parent==demos:FindFirstChild('Demos') and ui.actions[key].Interactable)
end
demos:FindFirstChild('CerrarPruebas').Activated:Fire()
assert(not demos.Visible and dock.Visible)
ui:setCatalogOpen(true);assert(not dock.Visible and not demos.Visible)
ui:setCatalogOpen(false)
for _,dims in ipairs({{1280,764},{900,604},{640,324},{390,808}})do
 ui.screen.AbsoluteSize=Vector2.new(dims[1],dims[2])
 ui:setMode('select',1,false,'FusionChamber',1,false)
 local w,h=dock.Size.X.Offset,dock.Size.Y.Offset
 local left=dock.Position.X.Offset
 local top=dims[2]+dock.Position.Y.Offset-h
 local detail=ui.screen:FindFirstChild('DetalleMaquina')
 assert(top>=0 and left>=0 and left+w<=detail.Position.X.Offset,'context dock overlaps right details or leaves screen')
end
print('PASS contextual HUD: clear idle view, compact actions, relevant recipe/filter, separate retained demos and responsive bounds')
