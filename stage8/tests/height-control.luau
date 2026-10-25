local changes=0
local heightUI=UI.new({height=function()changes+=1 end})
assert(heightUI.actions.height,'height control is missing from HUD')
heightUI:setMode('place',nil,false,'Belt')
heightUI:setHeight(1)
assert(heightUI.actions.height.Interactable and string.find(heightUI.actions.height.Text,'elevada'),'height button must show elevated mode')
heightUI.actions.height.Activated:Fire()
assert(changes==1,'height button does not invoke controller')
heightUI:setHeight(0)
assert(string.find(heightUI.actions.height.Text,'suelo'),'height button must show ground mode')
for _,typ in ipairs({'Receiver','ElevatorUp','ElevatorDown'})do
 heightUI:setMode('place',nil,false,typ)
 assert(not heightUI.actions.height.Interactable,'fixed-height machine should not change level')
end
heightUI:setMode('place',nil,true,'Belt')
assert(not heightUI.actions.height.Interactable,'pending placement must block height changes')
print('PASS visible height control, callback, labels and fixed-height restrictions')
