-- With T removed, every transport device needs to adopt the target port's level.
local total=0
for _,typ in ipairs(Catalog.order)do
 if not Catalog.isTransport(typ) or Catalog.isElevator(typ) then continue end
 testKind=typ
 for _,lift in ipairs({'ElevatorUp','ElevatorDown'})do for turn=0,3 do
  state=Construction.newState(1);dragStroke=nil;rotationOverride=false
  local ok,_,id=Construction.apply(state,1,{kind='place',machineType=lift,x=10,z=10,rotation=turn,level=0})
  assert(ok)
  local elevator=state.buildings[id]
  for _,portKind in ipairs({'input','output'})do
   local port=Catalog.port(elevator,portKind)
   local x,z=port.x+port.dx*.5-.5,port.z+port.dz*.5-.5
   buildLevel=1-port.level;rotation=(turn+2)%4
   aim(x,z,port.level);groundAt({})
   assert(buildLevel==port.level,typ..' did not change height at '..lift..' '..portKind)
   assert(candidate.x==x and candidate.z==z,typ..' did not adopt port coordinates')
   local rec={id=100,machineType=typ,x=candidate.x,z=candidate.z,rotation=rotation,level=buildLevel}
   assert(if portKind=='output' then Catalog.connected(elevator,rec) else Catalog.connected(rec,elevator),typ..' remains disconnected')
   assert(Construction.canPlace(state,typ,rec.x,rec.z,rec.rotation,nil,rec.level))
   total+=1
  end
 end end
end
print('PASS automatic upper/lower placement for every non-elevator transport: '..total..' cases')
