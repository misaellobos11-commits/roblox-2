local filtered=nil
local extraUI=UI.new({chooseFilter=function(item)filtered=item end})
extraUI:setCatalogOpen(true)
local visited={}
for _,tab in ipairs(extraUI.catalog:FindFirstChild('Categories'):GetChildren())do
 if tab:IsA('TextButton')then
  tab.Activated:Fire()
  for typ,card in pairs(extraUI.machineButtons)do if card.Visible then visited[typ]=true end end
 end
end
for _,typ in ipairs(Catalog.expansionOrder)do assert(visited[typ],'new machine absent from every tab: '..typ)end
extraUI:setMode('select',3,false,'FilterLeft',1,false)
extraUI:setDetails('FilterLeft',nil,'Carbon')
extraUI:toggleFilterPicker()
local picker=assert(extraUI.screen:FindFirstChild('SelectorMaterial'))
assert(picker.Visible)
local search=picker:FindFirstChild('Buscar')
search.Text='núcleo'
local results=picker:FindFirstChild('Materiales');local n=0
for _,b in ipairs(results:GetChildren())do if b:IsA('TextButton') and b.Visible then n+=1 end end
assert(n==2,'filter search must find both advanced cores')
results:FindFirstChild('QuantumCore').Activated:Fire()
assert(filtered=='QuantumCore' and not picker.Visible,'filter choice not sent/closed')
extraUI:toggleFilterPicker();extraUI:setMode('select',4,false,'FilterRight',1,false)
assert(not picker.Visible,'picker remains open for a different selected machine')
extraUI:toggleFilterPicker();extraUI:setMode('select',nil,false,nil,0,false)
assert(not picker.Visible,'picker remains open without a selected filter')
extraUI:setMode('select',nil,false,nil,0,false)
assert(extraUI.actions.expansionDemo.Interactable,'expansion test unavailable')
extraUI:setMode('place',nil,false,'Receiver',0,false)
assert(not extraUI.actions.expansionDemo.Interactable,'demo allowed while placing')
print('PASS all 44 cards discoverable by family, searchable filter picker and expansion demo action')
