-- Pure Luau contract tests: removing validation or changing state atomics must fail these.
local Construction = require('../src/shared/Construction')
local passed = 0
local failed = 0
local function test(name, callback)
    local ok, message = pcall(callback)
    if ok then
        passed += 1
        print('PASS ' .. name)
    else
        failed += 1
        print('FAIL ' .. name .. ': ' .. tostring(message))
    end
end
local function equal(actual, expected)
    assert(actual == expected, 'expected ' .. tostring(expected) .. ', got ' .. tostring(actual))
end
local function place(state, x, z, rotation, actor)
    return Construction.apply(state, actor or 123, {
        kind = 'place', machineType = 'Decomposer', x = x, z = z, rotation = rotation or 0,
    })
end
local function count(state)
    local n = 0
    for _ in state.buildings do n += 1 end
    return n
end

test('construction exposes authoritative operations', function()
    equal(type(Construction.newState), 'function')
    equal(type(Construction.apply), 'function')
end)
test('floor snapping uses plot origin, including positions just outside it', function()
    local x, z = Construction.worldToCell(227.99, 8, 224, 0)
    equal(x, 0); equal(z, 2)
    x, z = Construction.worldToCell(223.99, -0.01, 224, 0)
    equal(x, -1); equal(z, -1)
end)
test('2x2 machine fits all four last legal corners', function()
    local state = Construction.newState(123)
    for _, coords in {{0,0}, {46,0}, {0,46}, {46,46}} do
        equal(place(state, coords[1], coords[2]), true)
    end
    equal(count(state), 4)
end)
test('outside edges are rejected without allocating IDs', function()
    local state = Construction.newState(123)
    for _, coords in {{-1,0}, {0,-1}, {47,0}, {0,47}, {48,48}} do
        local ok, code = place(state, coords[1], coords[2])
        equal(ok, false); equal(code, 'outside')
    end
    equal(count(state), 0); equal(state.nextId, 1)
end)
test('overlap blocks but sharing a boundary is allowed', function()
    local state = Construction.newState(123)
    equal(place(state, 0, 0), true)
    local ok, code = place(state, 1, 1)
    equal(ok, false); equal(code, 'occupied')
    equal(place(state, 2, 0), true)
    equal(count(state), 2)
end)
test('all orientations fit the same 2x2 footprint at the edge', function()
    for rotation = 0, 3 do
        equal(place(Construction.newState(123), 46, 46, rotation), true)
    end
end)
test('input and output connectors rotate clockwise around the center', function()
    local expected = {
        {11,20,0,-1, 11,22,0,1},
        {12,21,1,0, 10,21,-1,0},
        {11,22,0,1, 11,20,0,-1},
        {10,21,-1,0, 12,21,1,0},
    }
    for rotation = 0, 3 do
        local ports = Construction.ports(10,20,rotation)
        local e = expected[rotation+1]
        equal(ports.input.x,e[1]); equal(ports.input.z,e[2])
        equal(ports.input.dx,e[3]); equal(ports.input.dz,e[4])
        equal(ports.output.x,e[5]); equal(ports.output.z,e[6])
        equal(ports.output.dx,e[7]); equal(ports.output.dz,e[8])
    end
    equal(Construction.rotate(3),0)
end)
test('foreign actor cannot place move or remove', function()
    local state = Construction.newState(123)
    place(state, 0, 0)
    for _, command in {
        {kind='place',machineType='Decomposer',x=5,z=5,rotation=0},
        {kind='move',id=1,x=5,z=5,rotation=1},
        {kind='remove',id=1},
    } do
        local ok, code = Construction.apply(state, 999, command)
        equal(ok,false); equal(code,'not_owner')
    end
    equal(count(state),1); equal(state.buildings[1].x,0)
end)
test('failed move preserves original ID position and orientation', function()
    local state = Construction.newState(123)
    place(state,0,0,1); place(state,4,0)
    for _, x in {3,47,-1} do
        equal(Construction.apply(state,123,{kind='move',id=1,x=x,z=0,rotation=2}),false)
        equal(state.buildings[1].x,0); equal(state.buildings[1].rotation,1)
        equal(count(state),2)
    end
end)
test('moving across its own old footprint preserves ID and frees cells', function()
    local state = Construction.newState(123)
    place(state,0,0)
    equal(Construction.apply(state,123,{kind='move',id=1,x=1,z=0,rotation=2}),true)
    equal(state.buildings[1].x,1); equal(state.buildings[1].rotation,2)
    equal(state.nextId,2)
    equal(Construction.apply(state,123,{kind='move',id=1,x=10,z=10,rotation=3}),true)
    equal(place(state,0,0),true)
end)
test('remove releases cells; replay cannot delete a replacement', function()
    local state = Construction.newState(123)
    place(state,0,0)
    equal(Construction.apply(state,123,{kind='remove',id=1}),true)
    equal(place(state,0,0),true)
    local ok, code = Construction.apply(state,123,{kind='remove',id=1})
    equal(ok,false); equal(code,'not_found')
    equal(count(state),1); equal(state.buildings[2].id,2)
end)
test('missing machines cannot be moved or removed', function()
    local state = Construction.newState(123)
    for _, command in {{kind='remove',id=9},{kind='move',id=9,x=0,z=0,rotation=0}} do
        local ok, code = Construction.apply(state,123,command)
        equal(ok,false); equal(code,'not_found')
    end
    equal(count(state),0)
end)
test('malformed commands and unsupported types leave state unchanged', function()
    local state = Construction.newState(123)
    for _, command in {false, 'place', 5, {}, {kind='buy'}, {kind='place',machineType='Generator',x=0,z=0,rotation=0}, {kind='remove',id='1'}} do
        equal(Construction.apply(state,123,command),false)
    end
    equal(Construction.apply(state,123,nil),false)
    equal(count(state),0)
end)
test('fractions NaN infinities strings and huge numbers are rejected', function()
    local invalid = {0/0, math.huge, -math.huge, 0.5, '0', false, {}, 1e20}
    for _, field in {'x','z','rotation'} do
        for _, value in invalid do
            local state = Construction.newState(123)
            local cmd = {kind='place',machineType='Decomposer',x=0,z=0,rotation=0}
            cmd[field] = value
            equal(Construction.apply(state,123,cmd),false)
            equal(count(state),0)
        end
    end
end)
test('orientation must be one of four quarter turns', function()
    for _, rotation in {-1,4,360} do
        equal(place(Construction.newState(123),0,0,rotation),false)
    end
end)
test('snapshots cannot mutate authoritative machines', function()
    local state = Construction.newState(123)
    place(state,2,4,1)
    local snapshot = Construction.snapshot(state)
    snapshot.buildings[1].x = 40
    snapshot.buildings[1] = nil
    snapshot.nextId = 800
    equal(state.buildings[1].x,2)
    equal(state.nextId,2)
end)
test('capacity limits placement but still permits moving and removing', function()
    local state = Construction.newState(123)
    for n = 0, 63 do
        equal(place(state, (n%8)*2, math.floor(n/8)*2),true)
    end
    local ok, code = place(state,40,40)
    equal(ok,false); equal(code,'limit')
    equal(Construction.apply(state,123,{kind='move',id=1,x=40,z=40,rotation=1}),true)
    equal(Construction.apply(state,123,{kind='remove',id=1}),true)
    equal(place(state,0,0),true)
    equal(count(state),64)
end)
test('independent plots never share state', function()
    local a, b = Construction.newState(123), Construction.newState(456)
    place(a,0,0)
    equal(place(b,0,0,0,456),true)
    Construction.apply(a,123,{kind='remove',id=1})
    equal(count(b),1)
end)
test('wire snapshots remain dense after deletion and reconstruct stable IDs', function()
    local state = Construction.newState(123)
    place(state,0,0); place(state,4,0); place(state,8,0)
    Construction.apply(state,123,{kind='remove',id=2})
    local wire = Construction.snapshot(state)
    equal(#wire.buildings,2)
    equal(wire.buildings[1].id,1)
    assert(wire.buildings[2], 'network snapshot must not contain holes')
    equal(wire.buildings[2].id,3)
    local restored = Construction.fromSnapshot(wire)
    equal(restored.buildings[2],nil)
    equal(restored.buildings[3].x,8)
    equal(Construction.apply(restored,123,{kind='move',id=3,x=10,z=0,rotation=1}),true)
    equal(state.buildings[3].x,8)
    equal(Construction.canPlace(restored,10,0,1,3),true)
end)
print(string.format('%d passed, %d failed',passed,failed))
assert(failed == 0, 'construction suite failed')
