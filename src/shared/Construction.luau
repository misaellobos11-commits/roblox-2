--!strict
-- Engine-independent rules shared by preview, server authority and CLI tests.
local Construction = {}
Construction.GRID_SIZE = 48
Construction.CELL_SIZE = 4
Construction.MACHINE_SIZE = 2
Construction.MAX_MACHINES = 64
Construction.MAX_PLOTS = 8
Construction.PLOT_SPACING = 224

export type Placement = {
    id: number,
    machineType: string,
    x: number,
    z: number,
    rotation: number,
}
export type State = {
    ownerId: number,
    nextId: number,
    buildings: {[number]: Placement},
}

export type Snapshot = {
    ownerId: number,
    nextId: number,
    buildings: {Placement},
}

Construction.messages = table.freeze({
    placed = 'Descomponedor colocado.',
    moved = 'Descomponedor movido.',
    removed = 'Descomponedor retirado.',
    outside = 'La máquina debe quedar dentro de tu terreno.',
    occupied = 'Estas casillas están ocupadas.',
    limit = 'Límite de 64 máquinas en esta prueba.',
    not_owner = 'Solo puedes construir en tu propia parcela.',
    not_found = 'Esa máquina ya no está en tu parcela.',
    invalid = 'Orden de construcción no válida.',
    busy = 'Espera un momento antes de repetir la acción.',
    valid = 'Posición válida · entrada IN / salida OUT.',
})

local function integer(value: any): boolean
    return type(value) == 'number' and value == value
        and math.abs(value) <= 1e6 and value % 1 == 0
end

function Construction.newState(ownerId: number): State
    return {ownerId = ownerId, nextId = 1, buildings = {}}
end

function Construction.snapshot(state: State): Snapshot
    -- Remotes require dense arrays; deleting IDs must never leave holes on the wire.
    local buildings: {Placement} = {}
    for _, building in state.buildings do
        table.insert(buildings, table.clone(building))
    end
    table.sort(buildings, function(a: Placement, b: Placement) return a.id < b.id end)
    return {ownerId=state.ownerId, nextId=state.nextId, buildings=buildings}
end

function Construction.fromSnapshot(snapshot: Snapshot): State
    local state = Construction.newState(snapshot.ownerId)
    state.nextId = snapshot.nextId
    for _, building in snapshot.buildings do
        state.buildings[building.id] = table.clone(building)
    end
    return state
end

function Construction.worldToCell(worldX: number, worldZ: number, originX: number, originZ: number): (number, number)
    return math.floor((worldX - originX) / Construction.CELL_SIZE),
        math.floor((worldZ - originZ) / Construction.CELL_SIZE)
end

function Construction.rotate(rotation: number): number
    return (rotation + 1) % 4
end

function Construction.ports(x: number, z: number, rotation: number)
    -- Clockwise when looking down on X/Z: north -> east -> south -> west.
    local dx, dz = 0, -1
    for _ = 1, rotation do
        dx, dz = -dz, dx
    end
    return {
        input = {x = x + 1 + dx, z = z + 1 + dz, dx = dx, dz = dz},
        output = {x = x + 1 - dx, z = z + 1 - dz, dx = -dx, dz = -dz},
    }
end

function Construction.count(state: State): number
    local count = 0
    for _ in state.buildings do
        count += 1
    end
    return count
end

function Construction.canPlace(state: State, x: any, z: any, rotation: any, ignoreId: number?): (boolean, string)
    if not integer(x) or not integer(z) or not integer(rotation) or rotation < 0 or rotation > 3 then
        return false, 'invalid'
    end
    local size = Construction.MACHINE_SIZE
    if x < 0 or z < 0 or x + size > Construction.GRID_SIZE or z + size > Construction.GRID_SIZE then
        return false, 'outside'
    end
    for id, building in state.buildings do
        if id ~= ignoreId and x < building.x + size and x + size > building.x
            and z < building.z + size and z + size > building.z then
            return false, 'occupied'
        end
    end
    if ignoreId == nil and Construction.count(state) >= Construction.MAX_MACHINES then
        return false, 'limit'
    end
    return true, 'valid'
end

function Construction.apply(state: State, actorId: number, command: any): (boolean, string, number?)
    if actorId ~= state.ownerId then
        return false, 'not_owner', nil
    end
    if type(command) ~= 'table' then
        return false, 'invalid', nil
    end
    local kind = command.kind
    if kind ~= 'place' and kind ~= 'move' and kind ~= 'remove' then
        return false, 'invalid', nil
    end
    if kind ~= 'place' then
        if not integer(command.id) or command.id < 1 then
            return false, 'invalid', nil
        end
        if not state.buildings[command.id] then
            return false, 'not_found', nil
        end
    elseif command.machineType ~= 'Decomposer' then
        return false, 'invalid', nil
    end
    if kind == 'remove' then
        state.buildings[command.id] = nil
        return true, 'removed', command.id
    end
    local ignoreId = if kind == 'move' then command.id else nil
    local valid, code = Construction.canPlace(state, command.x, command.z, command.rotation, ignoreId)
    if not valid then
        return false, code, nil
    end
    local id = if kind == 'move' then command.id else state.nextId
    -- Validate everything before replacing a record. No partial mutation or yields.
    state.buildings[id] = {
        id = id, machineType = 'Decomposer', x = command.x, z = command.z,
        rotation = command.rotation,
    }
    if kind == 'place' then
        state.nextId += 1
    end
    return true, if kind == 'place' then 'placed' else 'moved', id
end

return table.freeze(Construction)
