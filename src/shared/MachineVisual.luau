--!nonstrict
-- Rendering only; gameplay state lives in Construction and on the server.
local Construction = require(script.Parent.Construction)
local Visual = {}

local function part(parent, name, size, position, color, material)
    local object = Instance.new('Part')
    object.Name = name
    object.Size = size
    object.CFrame = CFrame.new(position)
    object.Anchored = true
    object.Color = color
    object.Material = material or Enum.Material.Metal
    object.TopSurface = Enum.SurfaceType.Smooth
    object.BottomSurface = Enum.SurfaceType.Smooth
    object.Parent = parent
    return object
end

local function label(parent, text, offset, color, size)
    local billboard = Instance.new('BillboardGui')
    billboard.Name = 'Label'
    billboard.Size = UDim2.fromOffset(size or 120, 26)
    billboard.StudsOffsetWorldSpace = offset
    billboard.AlwaysOnTop = true
    billboard.MaxDistance = 100
    billboard.Parent = parent
    local textLabel = Instance.new('TextLabel')
    textLabel.Size = UDim2.fromScale(1,1)
    textLabel.BackgroundColor3 = Color3.fromRGB(12,20,29)
    textLabel.BackgroundTransparency = 0.15
    textLabel.Text = text
    textLabel.TextColor3 = color
    textLabel.Font = Enum.Font.GothamBold
    textLabel.TextSize = 12
    textLabel.Parent = billboard
    local corner = Instance.new('UICorner')
    corner.CornerRadius = UDim.new(0,5)
    corner.Parent = textLabel
end

function Visual.pivot(model, record, origin)
    local center = origin + Vector3.new((record.x + 1)*Construction.CELL_SIZE, 0, (record.z + 1)*Construction.CELL_SIZE)
    model:PivotTo(CFrame.new(center) * CFrame.Angles(0,-record.rotation*math.pi/2,0))
    model:SetAttribute('GridX',record.x)
    model:SetAttribute('GridZ',record.z)
    model:SetAttribute('Rotation',record.rotation)
end

function Visual.create(parent, record, origin, preview)
    local model = Instance.new('Model')
    model.Name = if preview then 'BuildPreview' else 'Decomposer_' .. record.id
    model:SetAttribute('BuildingId',record.id)
    model:SetAttribute('MachineType','Decomposer')
    local anchor = part(model,'Anchor',Vector3.new(0.1,0.1,0.1),Vector3.zero,Color3.new())
    anchor.Transparency = 1
    anchor.CanCollide = false
    anchor.CanQuery = false
    anchor.CanTouch = false
    model.PrimaryPart = anchor
    part(model,'Footprint',Vector3.new(7.85,0.4,7.85),Vector3.new(0,0.2,0),Color3.fromRGB(39,54,66))
    part(model,'Housing',Vector3.new(6,3.5,5),Vector3.new(0,2.15,0),Color3.fromRGB(63,82,98))
    part(model,'Top',Vector3.new(6.3,0.35,5.3),Vector3.new(0,4.05,0),Color3.fromRGB(28,41,53))
    part(model,'Core',Vector3.new(1.6,0.3,3.5),Vector3.new(0,4.4,0),Color3.fromRGB(58,218,224),Enum.Material.Neon)
    for _, x in {-2.5,2.5} do
        part(model,'Frame',Vector3.new(0.35,4.2,0.45),Vector3.new(x,2.5,-2.2),Color3.fromRGB(112,137,151))
    end
    local input = part(model,'InputMark',Vector3.new(2.5,0.2,0.7),Vector3.new(0,0.55,-3.45),Color3.fromRGB(255,188,86),Enum.Material.Neon)
    local output = part(model,'OutputMark',Vector3.new(2.5,0.2,0.7),Vector3.new(0,0.55,3.45),Color3.fromRGB(68,225,227),Enum.Material.Neon)
    label(input,'IN · entrada',Vector3.new(0,0.7,0),Color3.fromRGB(255,208,133),100)
    label(output,'OUT · salida',Vector3.new(0,0.7,0),Color3.fromRGB(142,245,245),100)
    label(anchor,'DESCOMPONEDOR',Vector3.new(0,5.7,0),Color3.fromRGB(230,244,250),150)
    for name, z in {Input=-4,Output=4} do
        local attachment = Instance.new('Attachment')
        attachment.Name = name
        attachment.Position = Vector3.new(0,0.5,z)
        attachment.Parent = anchor
    end
    if preview then
        for _, item in model:GetDescendants() do
            if item:IsA('BasePart') then
                item.CanCollide = false
                item.CanQuery = false
                item.CanTouch = false
            end
        end
    end
    Visual.pivot(model,record,origin)
    model.Parent = parent
    return model
end

function Visual.setPreview(model, valid)
    local color = if valid then Color3.fromRGB(75,231,170) else Color3.fromRGB(255,99,111)
    for _, item in model:GetDescendants() do
        if item:IsA('BasePart') and item.Name ~= 'Anchor' then
            item.Color = color
            item.Transparency = 0.5
        end
    end
end

return Visual
