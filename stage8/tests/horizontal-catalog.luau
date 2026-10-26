assert(ui.actions.height==nil and ui.actions.bulk==nil,'obsolete height or multi-select toggle remains')
assert(ui.actions.remove==nil,'single/group deletion should share one action')
local items=ui.catalog:FindFirstChild('Componentes')
local grid=items:FindFirstChildOfClass('UIGridLayout')
assert(items.AutomaticCanvasSize==Enum.AutomaticSize.X and items.ScrollingDirection==Enum.ScrollingDirection.X,'catalog must scroll right, not down')
assert(grid.FillDirection==Enum.FillDirection.Vertical and grid.FillDirectionMaxCells==2,'cards must fill two rows then extend right')
for _,dims in ipairs({{1366,768},{900,640},{800,480},{640,360},{390,844}})do
 ui.screen.AbsoluteSize=Vector2.new(dims[1],dims[2]-36)
 ui:setCatalogOpen(true)
 assert(grid.CellSize.X.Scale==0 and grid.CellSize.Y.Offset<=88,'miniatures must remain compact')
 local usableWidth=ui.catalog.Size.X.Offset-24
 if dims[1]>=900 then
  assert(grid.CellSize.X.Offset*6+5*8<=usableWidth,'11 production objects need six visible columns on desktop')
 end
 assert(grid.CellSize.Y.Offset*2+8+5<=ui.catalog.Size.Y.Offset-96,'second row or scrollbar clips')
end
ui:setMode('select',7,false,'FusionChamber',1,false)
assert(ui.actions.move.Interactable and ui.actions.recipe.Interactable and ui.actions.bulkRemove.Interactable,'single selection lost its actions')
ui:setMode('select',nil,false,'Receiver',2,false)
assert(not ui.actions.move.Interactable and not ui.actions.recipe.Interactable,'group exposes single-object action')
assert(ui.actions.bulkRemove.Interactable,'group cannot be removed')
for _,key in ipairs({'demo','productionDemo','megaDemo'})do assert(ui.actions[key].Interactable,'demo removed or disabled by default selection')end
ui:setMode('select',nil,true,'Receiver',2,true)
for _,b in pairs(ui.actions)do assert(not b.Interactable,'pending order leaves action active')end
ui:setHeight(1)
print('PASS compact two-row horizontal catalog, all production cards on desktop, automatic-height HUD and default selection actions')
