-- Intersect the pointer ray with the actual build/port plane, not always the floor.
local function beltPlacement(state,rayOrigin,rayDirection,origin,level,rotation,ignoreId,lockedLevel,rotationLocked)
    local function pointAt(targetLevel)
        if math.abs(rayDirection.Y)<1e-6 then return nil end
        local t=(origin.Y+.90+targetLevel*8-rayOrigin.Y)/rayDirection.Y
        if t<0 then return nil end
        return rayOrigin.X+rayDirection.X*t,rayOrigin.Z+rayDirection.Z*t,t
    end
    local selected=lockedLevel or level
    local px,pz=pointAt(selected)
    if not px then return nil end
    local rx,rz=(px-origin.X)/Construction.CELL_SIZE,(pz-origin.Z)/Construction.CELL_SIZE
    local result={x=math.floor((rx-.5)*2+.5)/2,z=math.floor((rz-.5)*2+.5)/2,level=selected,rotation=rotation}
    local best=math.huge
    for id,machine in pairs(state.buildings) do
        if id==ignoreId then continue end
        for _,kind in ipairs({'input','output'}) do
            if kind=='input' and machine.machineType=='Receiver' then continue end
            local ports=if kind=='input' then Catalog.inputPorts(machine) else Catalog.outputs(machine)
            for _,port in ipairs(ports) do
                if lockedLevel~=nil and port.level~=lockedLevel then continue end
                local hx,hz,depth=pointAt(port.level)
                if not hx then continue end
                local x,z=port.x+port.dx*.5-.5,port.z+port.dz*.5-.5
                local wx,wz=origin.X+(x+.5)*Construction.CELL_SIZE,origin.Z+(z+.5)*Construction.CELL_SIZE
                local distance=math.sqrt((wx-hx)^2+(wz-hz)^2)
                if distance>=2.85 then continue end
                local sign=if kind=='output' then 1 else -1
                local r=rotation
                if not rotationLocked then
                    for turn=0,3 do
                        local dx,dz=Catalog.forward(turn)
                        if dx==port.dx*sign and dz==port.dz*sign then r=turn;break end
                    end
                end
                local belt={id=0,machineType='Belt',x=x,z=z,rotation=r,level=port.level}
                local connects=if kind=='output' then Catalog.connected(machine,belt) else Catalog.connected(belt,machine)
                local valid=Construction.canPlace(state,'Belt',x,z,r,ignoreId,port.level)
                -- Overlapping projections select the nearer port, like a raycast.
                -- The explicit height button can select the occluded lower plane.
                local score=distance+depth*1e-6+id*1e-10
                if connects and valid and score<best then
                    best=score
                    result={x=x,z=z,rotation=r,level=port.level,snapped=true}
                end
            end
        end
    end
    return result
end
