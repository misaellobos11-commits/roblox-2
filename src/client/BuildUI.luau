--!nonstrict
local Players = game:GetService('Players')
local UserInputService = game:GetService('UserInputService')
local UI = {}
local colors = {
    panel = Color3.fromRGB(16,27,38), border = Color3.fromRGB(56,91,108),
    text = Color3.fromRGB(230,243,249), muted = Color3.fromRGB(154,179,192),
    cyan = Color3.fromRGB(88,224,227), button = Color3.fromRGB(37,61,77),
}
local function round(parent, radius)
    local corner = Instance.new('UICorner')
    corner.CornerRadius = UDim.new(0,radius)
    corner.Parent = parent
end
local function text(parent, name, value, size, position, dimensions, color)
    local label = Instance.new('TextLabel')
    label.Name = name
    label.BackgroundTransparency = 1
    label.Position = position
    label.Size = dimensions
    label.Text = value
    label.TextSize = size
    label.Font = Enum.Font.GothamMedium
    label.TextColor3 = color or colors.text
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = parent
    return label
end
local function panel(screen, name, position, size, anchor, maxWidth)
    local frame = Instance.new('Frame')
    frame.Name = name
    frame.Position = position
    frame.Size = size
    frame.AnchorPoint = anchor
    frame.BackgroundColor3 = colors.panel
    frame.BackgroundTransparency = 0.04
    frame.BorderSizePixel = 0
    frame.Parent = screen
    round(frame,12)
    local border = Instance.new('UIStroke')
    border.Color = colors.border
    border.Thickness = 1
    border.Parent = frame
    local constraint = Instance.new('UISizeConstraint')
    constraint.MaxSize = Vector2.new(maxWidth,1000)
    constraint.Parent = frame
    return frame
end

function UI.new(callbacks)
    local screen = Instance.new('ScreenGui')
    screen.Name = 'MatterloomBuildUI'
    screen.ResetOnSpawn = false
    screen.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
    screen.Parent = Players.LocalPlayer:WaitForChild('PlayerGui')
    local header = panel(screen,'Header',UDim2.new(0.5,0,0,10),UDim2.new(0.94,0,0,90),Vector2.new(0.5,0),510)
    local title = text(header,'Title','MATTERLOOM',22,UDim2.fromOffset(16,10),UDim2.new(1,-32,0,28),colors.cyan)
    title.Font = Enum.Font.GothamBold
    text(header,'Stage','01 / TERRENO Y CONSTRUCCIÓN',12,UDim2.fromOffset(16,40),UDim2.new(1,-32,0,20),colors.muted)
    local counter = text(header,'Count','48 × 48 casillas · 0 / 64 máquinas',12,UDim2.fromOffset(16,63),UDim2.new(1,-32,0,18))
    local dock = panel(screen,'BuildDock',UDim2.new(0.5,0,1,-12),UDim2.new(0.94,0,0,214),Vector2.new(0.5,1),540)
    local modeLabel = text(dock,'Mode','Elige «Nueva» para empezar',14,UDim2.fromOffset(14,10),UDim2.new(1,-28,0,22),colors.cyan)
    local status = text(dock,'Status','Construcción de prueba · sin guardado todavía.',12,UDim2.fromOffset(14,36),UDim2.new(1,-28,0,34),colors.muted)
    status.TextWrapped = true
    status.TextYAlignment = Enum.TextYAlignment.Top
    local buttonsFrame = Instance.new('Frame')
    buttonsFrame.Name = 'Actions'
    buttonsFrame.BackgroundTransparency = 1
    buttonsFrame.Position = UDim2.fromOffset(12,76)
    buttonsFrame.Size = UDim2.new(1,-24,0,96)
    buttonsFrame.Parent = dock
    local layout = Instance.new('UIGridLayout')
    layout.CellSize = UDim2.new(1/3,-6,0,44)
    layout.CellPadding = UDim2.fromOffset(8,8)
    layout.SortOrder = Enum.SortOrder.LayoutOrder
    layout.Parent = buttonsFrame
    local buttons = {}
    for index, action in {
        {'new','Nueva'}, {'rotate','Girar · R'}, {'confirm','Colocar'},
        {'move','Mover'}, {'remove','Retirar'}, {'cancel','Cancelar'},
    } do
        local button = Instance.new('TextButton')
        button.Name = action[1]
        button.LayoutOrder = index
        button.BackgroundColor3 = colors.button
        button.BorderSizePixel = 0
        button.Text = action[2]
        button.TextColor3 = colors.text
        button.TextSize = 14
        button.Font = Enum.Font.GothamBold
        button.Parent = buttonsFrame
        round(button,8)
        button.Activated:Connect(function()
            local callback = callbacks[action[1]]
            if callback then callback() end
        end)
        buttons[action[1]] = button
    end
    local hint = text(dock,'Hint','R: girar · Esc: cancelar · toca una máquina para seleccionarla',11,UDim2.fromOffset(14,180),UDim2.new(1,-28,0,28),colors.muted)
    hint.TextWrapped = true
    local self = {screen=screen,buttons=buttons}

    function self:setMode(mode, selected, busy)
        local building = mode == 'place' or mode == 'move'
        modeLabel.Text = if mode == 'move' then 'MOVER · confirma la nueva posición'
            elseif mode == 'place' then 'DESCOMPONEDOR · 2 × 2 casillas'
            elseif selected then 'DESCOMPONEDOR #' .. selected .. ' seleccionado'
            else 'Elige «Nueva» para empezar'
        local enabled = {
            new = not busy,
            rotate = building and not busy,
            confirm = building and not busy,
            move = selected ~= nil and not building and not busy,
            remove = selected ~= nil and not building and not busy,
            cancel = not busy and (building or selected ~= nil),
        }
        for name, button in buttons do
            button.Active = enabled[name]
            button.Interactable = enabled[name]
            button.AutoButtonColor = enabled[name]
            button.TextTransparency = if enabled[name] then 0 else 0.6
            button.BackgroundColor3 = if name == 'confirm' and enabled[name]
                then Color3.fromRGB(26,109,113) else colors.button
        end
        buttons.confirm.Text = if busy then 'Esperando…' elseif mode == 'move' then 'Confirmar' else 'Colocar'
    end

    function self:setStatus(message, valid)
        if status.Text ~= message then status.Text = message end
        status.TextColor3 = if valid == false then Color3.fromRGB(255,156,164)
            elseif valid == true then Color3.fromRGB(139,233,187) else colors.muted
    end

    function self:setCount(count)
        counter.Text = string.format('48 × 48 casillas · %d / 64 máquinas',count)
    end

    function self:containsPoint(position)
        local playerGui = Players.LocalPlayer:FindFirstChild('PlayerGui')
        if not playerGui then return false end
        for _, object in playerGui:GetGuiObjectsAtPosition(position.X,position.Y) do
            if object:IsDescendantOf(screen) then return true end
        end
        return false
    end

    -- Keep the standard mobile movement/jump controls clear at the bottom.
    local viewportConnection
    local function adaptLayout()
        local camera = workspace.CurrentCamera
        if not camera then return end
        local touch = UserInputService.PreferredInput == Enum.PreferredInput.Touch
        local compact = camera.ViewportSize.Y < 520
        header.Visible = not compact
        dock.AnchorPoint = if touch then Vector2.new(1,0) else Vector2.new(0.5,1)
        dock.Position = if touch then UDim2.new(1,-12,0,if compact then 10 else 110)
            else UDim2.new(0.5,0,1,-12)
        dock:FindFirstChildOfClass('UISizeConstraint').MaxSize = Vector2.new(if touch then 360 else 540,1000)
    end
    local function bindCamera()
        if viewportConnection then viewportConnection:Disconnect() end
        local camera = workspace.CurrentCamera
        if camera then viewportConnection = camera:GetPropertyChangedSignal('ViewportSize'):Connect(adaptLayout) end
        adaptLayout()
    end
    workspace:GetPropertyChangedSignal('CurrentCamera'):Connect(bindCamera)
    UserInputService:GetPropertyChangedSignal('PreferredInput'):Connect(adaptLayout)
    bindCamera()
    self:setMode('select',nil,false)
    return self
end

return UI
