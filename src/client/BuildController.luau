--!nonstrict
local Players = game:GetService('Players')
local ReplicatedStorage = game:GetService('ReplicatedStorage')
local UserInputService = game:GetService('UserInputService')
local RunService = game:GetService('RunService')
local GuiService = game:GetService('GuiService')
local Construction = require(ReplicatedStorage:WaitForChild('Shared'):WaitForChild('Construction'))
local Visual = require(ReplicatedStorage.Shared:WaitForChild('MachineVisual'))
local UI = require(script.Parent.BuildUI)
local PointerRay = require(script.Parent.PointerRay)
local Controller = {}

function Controller.start()
    local player = Players.LocalPlayer
    local remotes = ReplicatedStorage:WaitForChild('Matterloom')
    local getState = remotes:WaitForChild('GetState')
    local commandEvent = remotes:WaitForChild('Command')
    local state, origin, plot
    local mode, selectedId, rotation = 'select', nil, 0
    local candidate, preview, pending = nil, nil, false
    local feedbackUntil = 0
    local actions = {}
    local ui = UI.new(actions)
    local highlight = Instance.new('Highlight')
    highlight.Name = 'SelectedMachine'
    highlight.FillTransparency = 0.85
    highlight.FillColor = Color3.fromRGB(79,218,225)
    highlight.OutlineColor = Color3.fromRGB(152,249,248)
    highlight.DepthMode = Enum.HighlightDepthMode.Occluded
    highlight.Parent = workspace

    local function isBuilding()
        return mode == 'place' or mode == 'move'
    end
    local function refresh()
        ui:setMode(mode,selectedId,pending)
        if state then ui:setCount(Construction.count(state)) end
        local machines = plot and plot:FindFirstChild('Machines')
        highlight.Adornee = if selectedId and machines then machines:FindFirstChild('Decomposer_' .. selectedId) else nil
    end
    local function feedback(message, valid)
        feedbackUntil = os.clock()+2.5
        ui:setStatus(message,valid)
    end
    local function clearPreview()
        if preview then preview:Destroy(); preview = nil end
        candidate = nil
    end
    local function renderPreview()
        if not candidate or not isBuilding() then return end
        local valid, code = Construction.canPlace(state,candidate.x,candidate.z,rotation,if mode == 'move' then selectedId else nil)
        local record = {id=0,x=candidate.x,z=candidate.z,rotation=rotation}
        if not preview then preview = Visual.create(workspace,record,origin,true) end
        Visual.pivot(preview,record,origin)
        Visual.setPreview(preview,valid)
        if os.clock() >= feedbackUntil then
            ui:setStatus(Construction.messages[code],valid)
        end
    end
    local function ray(position, targets)
        local camera = workspace.CurrentCamera
        if not camera then return nil end
        local inset = GuiService:GetGuiInset()
        local screenRay = PointerRay.fromScreen(camera,position,inset)
        local params = RaycastParams.new()
        params.FilterType = Enum.RaycastFilterType.Include
        params.FilterDescendantsInstances = targets
        return workspace:Raycast(screenRay.Origin,screenRay.Direction*4096,params)
    end
    local function targetGround(position)
        if not plot then return end
        local floor = plot:FindFirstChild('BuildFloor')
        local hit = if floor then ray(position,{floor}) else nil
        if hit then
            local x, z = Construction.worldToCell(hit.Position.X,hit.Position.Z,origin.X,origin.Z)
            candidate = {x=x,z=z}
            renderPreview()
        else
            clearPreview()
            if os.clock() >= feedbackUntil then
                ui:setStatus('Apunta dentro de tu terreno.',false)
            end
        end
    end
    local function selectAt(position)
        local machines = plot and plot:FindFirstChild('Machines')
        local hit = if machines then ray(position,{machines}) else nil
        local model = hit and hit.Instance:FindFirstAncestorOfClass('Model')
        selectedId = nil
        if model and model:GetAttribute('OwnerUserId') == player.UserId then
            local id = model:GetAttribute('BuildingId')
            if state.buildings[id] then selectedId = id end
        end
        refresh()
        feedback(if selectedId then 'Máquina de prueba · usa Mover o Retirar.' else 'Selecciona una máquina o pulsa «Nueva».',nil)
    end
    local function send(command)
        if pending or not state then return end
        pending = true
        refresh()
        feedback('Validando construcción…',nil)
        commandEvent:FireServer(command)
    end

    actions.new = function()
        if pending or not state then return end
        clearPreview()
        selectedId = nil
        mode = 'place'
        rotation = 0
        feedbackUntil = 0
        refresh()
        ui:setStatus('Apunta o toca el terreno y pulsa Colocar.',nil)
    end
    actions.rotate = function()
        if pending or not isBuilding() then return end
        rotation = Construction.rotate(rotation)
        feedbackUntil = 0
        renderPreview()
    end
    actions.confirm = function()
        if pending or not isBuilding() or not state then return end
        if not candidate then feedback('Elige primero una posición dentro del terreno.',false); return end
        local valid, code = Construction.canPlace(state,candidate.x,candidate.z,rotation,if mode == 'move' then selectedId else nil)
        if not valid then feedback(Construction.messages[code],false); return end
        send({kind=if mode=='move' then 'move' else 'place',machineType='Decomposer',
            id=selectedId,x=candidate.x,z=candidate.z,rotation=rotation})
    end
    actions.move = function()
        if pending or not selectedId or isBuilding() then return end
        local record = state.buildings[selectedId]
        if not record then return end
        clearPreview()
        mode = 'move'
        rotation = record.rotation
        candidate = {x=record.x,z=record.z}
        feedbackUntil = 0
        refresh()
        renderPreview()
    end
    actions.remove = function()
        if pending or not selectedId or isBuilding() then return end
        send({kind='remove',id=selectedId})
    end
    actions.cancel = function()
        if pending then return end
        clearPreview()
        mode = 'select'
        selectedId = nil
        refresh()
        feedback('Acción cancelada. La fábrica no cambió.',nil)
    end

    commandEvent.OnClientEvent:Connect(function(response)
        pending = false
        if response.state then state = Construction.fromSnapshot(response.state) end
        if response.ok then
            clearPreview()
            mode = 'select'
            selectedId = if response.code == 'removed' then nil else response.id
        end
        refresh()
        feedback(Construction.messages[response.code] or 'No se pudo completar la acción.',response.ok)
    end)

    local ok, initial = pcall(function() return getState:InvokeServer() end)
    if not ok or not initial or initial.error then
        ui:setMode('select',nil,true)
        ui:setStatus(if ok and initial then initial.error else 'No se pudo cargar la parcela. Vuelve a entrar.',false)
        return
    end
    state, origin = Construction.fromSnapshot(initial.state), initial.origin
    plot = workspace:WaitForChild('MatterloomPlots'):WaitForChild('Plot_' .. player.UserId)
    refresh()

    -- Escape is consumed by Roblox's core menu; cancel its preview on menu open too.
    GuiService.MenuOpened:Connect(actions.cancel)
    UserInputService.InputBegan:Connect(function(input,processed)
        if processed or UserInputService:GetFocusedTextBox() then return end
        if input.KeyCode == Enum.KeyCode.R then actions.rotate()
        elseif input.KeyCode == Enum.KeyCode.Escape then actions.cancel()
        elseif input.UserInputType == Enum.UserInputType.MouseButton1 and not pending then
            local position = UserInputService:GetMouseLocation()
            if ui:containsPoint(position) then return end
            if isBuilding() then targetGround(position); actions.confirm()
            else selectAt(position) end
        end
    end)
    UserInputService.TouchTapInWorld:Connect(function(position,processed)
        if processed or pending or ui:containsPoint(position) then return end
        if isBuilding() then targetGround(position)
        else selectAt(position) end
    end)
    -- Recalculate at 20 Hz, not once per rendered frame; only pointer devices follow the cursor.
    local accumulated = 0
    RunService.RenderStepped:Connect(function(dt)
        accumulated += dt
        if accumulated < 0.05 then return end
        accumulated = 0
        if not pending and isBuilding() and UserInputService.PreferredInput ~= Enum.PreferredInput.Touch then
            local position = UserInputService:GetMouseLocation()
            if not ui:containsPoint(position) then targetGround(position) end
        end
        if selectedId and highlight.Adornee == nil then refresh() end
    end)
    player.CharacterAdded:Connect(function()
        -- Preview and selection are local; never remove an authoritative machine on respawn.
        if not pending then actions.cancel() end
    end)
end

return Controller
