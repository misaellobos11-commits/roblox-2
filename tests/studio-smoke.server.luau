-- Run as a temporary Script in ServerScriptService in a Studio test copy.
-- Deliberately excluded from the shipped place. This needs the Roblox engine.
local Shared = game:GetService('ReplicatedStorage'):WaitForChild('Shared')
local Construction = require(Shared.Construction)
local Visual = require(Shared.MachineVisual)
local folder = Instance.new('Folder')
folder.Name = 'ConstructionSmokeTest'
folder.Parent = workspace
local origin = Vector3.new(224, 0, 224)
local state = Construction.newState(123)
assert(Construction.apply(state, 123, {kind='place',machineType='Decomposer',x=10,z=20,rotation=0}))
local model = Visual.create(folder, state.buildings[1], origin, false)
model:SetAttribute('OwnerUserId',123)
for rotation = 0, 3 do
    assert(Construction.apply(state,123,{kind='move',id=1,x=10,z=20,rotation=rotation}))
    Visual.pivot(model,state.buildings[1],origin)
    local expected = Construction.ports(10,20,rotation)
    for _, pair in {{'Input',expected.input},{'Output',expected.output}} do
        local attachment = model.PrimaryPart:FindFirstChild(pair[1])
        local worldPosition = origin + Vector3.new(pair[2].x*4,0.5,pair[2].z*4)
        assert((attachment.WorldPosition-worldPosition).Magnitude < 0.001,'Port rotation disagrees with grid')
    end
end
assert(model:GetAttribute('BuildingId') == 1)
assert(model:GetAttribute('Rotation') == 3)
assert(model:GetAttribute('OwnerUserId') == 123)
local preview = Visual.create(folder,state.buildings[1],origin,true)
Visual.setPreview(preview,false)
for _, part in preview:GetDescendants() do
    if part:IsA('BasePart') then
        assert(not part.CanCollide and not part.CanQuery and not part.CanTouch)
    end
end
assert(Construction.apply(state,123,{kind='remove',id=1}))
model:Destroy()
assert(model.Parent == nil and state.buildings[1] == nil)
folder:Destroy()
print('Matterloom Studio model smoke: PASS')
