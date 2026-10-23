--!nonstrict
local Players = game:GetService('Players')
local ReplicatedStorage = game:GetService('ReplicatedStorage')
local Shared = ReplicatedStorage:WaitForChild('Shared')
local Construction = require(Shared.Construction)
local Visual = require(Shared.MachineVisual)
local BuildServer = {}

local function slab(parent,name,size,position,color)
    local part = Instance.new('Part')
    part.Name = name
    part.Anchored = true
    part.Size = size
    part.Position = position
    part.Color = color
    part.Material = Enum.Material.SmoothPlastic
    part.TopSurface = Enum.SurfaceType.Smooth
    part.BottomSurface = Enum.SurfaceType.Smooth
    part.Parent = parent
    return part
end

local function createPlot(parent, player, slot)
    local origin = Vector3.new(((slot-1)%4)*Construction.PLOT_SPACING,0,math.floor((slot-1)/4)*Construction.PLOT_SPACING)
    local plot = Instance.new('Model')
    plot.Name = 'Plot_' .. player.UserId
    plot:SetAttribute('OwnerUserId',player.UserId)
    plot.Parent = parent
    local width = Construction.GRID_SIZE*Construction.CELL_SIZE
    local floor = slab(plot,'BuildFloor',Vector3.new(width,1,width),origin+Vector3.new(width/2,-0.5,width/2),Color3.fromRGB(24,38,49))
    floor:SetAttribute('OwnerUserId',player.UserId)
    local grid = Instance.new('Folder')
    grid.Name = 'Grid'
    grid.Parent = plot
    for i = 0, Construction.GRID_SIZE do
        local coordinate = i*Construction.CELL_SIZE
        local color = if i%4 == 0 then Color3.fromRGB(61,90,105) else Color3.fromRGB(38,58,73)
        for _, line in {
            slab(grid,'Line',Vector3.new(0.045,0.015,width),origin+Vector3.new(coordinate,0.012,width/2),color),
            slab(grid,'Line',Vector3.new(width,0.015,0.045),origin+Vector3.new(width/2,0.012,coordinate),color),
        } do
            line.CanCollide = false
            line.CanTouch = false
            line.CanQuery = false
        end
    end
    slab(plot,'Entry',Vector3.new(28,1,20),origin+Vector3.new(width/2,-0.5,-10),Color3.fromRGB(34,57,69))
    local spawn = Instance.new('SpawnLocation')
    spawn.Name = 'EntrySpawn'
    spawn.Size = Vector3.new(8,0.3,8)
    spawn.Position = origin+Vector3.new(width/2,0.15,-10)
    spawn.Anchored = true
    spawn.Neutral = true
    spawn.Duration = 0
    spawn.Material = Enum.Material.Neon
    spawn.Color = Color3.fromRGB(66,198,201)
    spawn.Parent = plot
    local sign = slab(plot,'PlotSign',Vector3.new(18,5,0.5),origin+Vector3.new(width/2,4,-20),Color3.fromRGB(15,26,35))
    local surface = Instance.new('SurfaceGui')
    surface.Face = Enum.NormalId.Back
    surface.CanvasSize = Vector2.new(720,200)
    surface.Parent = sign
    local label = Instance.new('TextLabel')
    label.BackgroundTransparency = 1
    label.Size = UDim2.fromScale(1,1)
    label.Text = 'MATTERLOOM\n' .. player.DisplayName .. ' · parcela experimental'
    label.Font = Enum.Font.GothamBold
    label.TextSize = 28
    label.TextColor3 = Color3.fromRGB(153,239,240)
    label.Parent = surface
    local machines = Instance.new('Folder')
    machines.Name = 'Machines'
    machines.Parent = plot
    return {state=Construction.newState(player.UserId),origin=origin,model=plot,
        machines=machines,models={},slot=slot,spawn=spawn,tokens=12,lastRequest=os.clock()}
end

function BuildServer.start()
    local plots = Instance.new('Folder')
    plots.Name = 'MatterloomPlots'
    plots.Parent = workspace
    local remotes = Instance.new('Folder')
    remotes.Name = 'Matterloom'
    local getState = Instance.new('RemoteFunction')
    getState.Name = 'GetState'
    getState.Parent = remotes
    local commandEvent = Instance.new('RemoteEvent')
    commandEvent.Name = 'Command'
    commandEvent.Parent = remotes
    local sessions, slots = {}, {}

    local function setup(player)
        if sessions[player] then return sessions[player] end
        local slot
        for candidate = 1, Construction.MAX_PLOTS do
            if not slots[candidate] then slot = candidate; break end
        end
        if not slot then return nil end
        slots[slot] = player
        local session = createPlot(plots,player,slot)
        sessions[player] = session
        player.RespawnLocation = session.spawn
        local function moveCharacter(character)
            local root = character:WaitForChild('HumanoidRootPart',10)
            if root and sessions[player] == session and player.Character == character then
                character:PivotTo(CFrame.new(session.spawn.Position+Vector3.new(0,4,0)) * CFrame.Angles(0,math.pi,0))
            end
        end
        session.characterConnection = player.CharacterAdded:Connect(moveCharacter)
        if player.Character then task.spawn(moveCharacter,player.Character) end
        return session
    end

    local function packet(session)
        return {state=Construction.snapshot(session.state),origin=session.origin}
    end

    getState.OnServerInvoke = function(player)
        local session = setup(player)
        if not session then
            return {error='Este servidor tiene sus ocho parcelas ocupadas. Prueba otro servidor.'}
        end
        return packet(session)
    end

    commandEvent.OnServerEvent:Connect(function(player,command)
        local session = sessions[player]
        if not session then return end
        local now = os.clock()
        session.tokens = math.min(12,session.tokens+(now-session.lastRequest)*6)
        session.lastRequest = now
        if session.tokens < 1 then
            -- At most one rate-limit response per second, even to a flooding client.
            if not session.lastBusy or now-session.lastBusy >= 1 then
                session.lastBusy = now
                commandEvent:FireClient(player,{ok=false,code='busy'})
            end
            return
        end
        session.tokens -= 1
        local ok, code, id = Construction.apply(session.state,player.UserId,command)
        if ok then
            if command.kind == 'remove' then
                local model = session.models[id]
                if model then model:Destroy() end
                session.models[id] = nil
            elseif command.kind == 'move' then
                Visual.pivot(session.models[id],session.state.buildings[id],session.origin)
            else
                local model = Visual.create(session.machines,session.state.buildings[id],session.origin,false)
                model:SetAttribute('OwnerUserId',player.UserId)
                session.models[id] = model
            end
        end
        local response = packet(session)
        response.ok = ok
        response.code = code
        response.id = id
        commandEvent:FireClient(player,response)
    end)

    Players.PlayerRemoving:Connect(function(player)
        local session = sessions[player]
        if not session then return end
        sessions[player] = nil
        slots[session.slot] = nil
        session.characterConnection:Disconnect()
        session.model:Destroy()
    end)
    Players.PlayerAdded:Connect(setup)
    for _, player in Players:GetPlayers() do setup(player) end
    -- Publish only after handlers are ready, so clients cannot race initialization.
    remotes.Parent = ReplicatedStorage
end

return BuildServer
