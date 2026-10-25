local cases=0
for _,typ in ipairs({'ElevatorUp','ElevatorDown'})do
 for r=0,3 do for _,offset in ipairs({0,.5})do
  state=Construction.newState(1)
  local ok,_,id=Construction.apply(state,1,{kind='place',machineType=typ,x=10+offset,z=10+offset,rotation=r,level=0})
  assert(ok)
  local elevator=state.buildings[id]
  for _,portKind in ipairs({'input','output'})do
   local port=Catalog.port(elevator,portKind)
   local x,z=port.x+port.dx*.5-.5,port.z+port.dz*.5-.5
   buildLevel=0;rotation=(r+2)%4;dragStroke=nil;heightOverride=false
   aim(x,z,port.level);groundAt({X=0,Y=0})
   assert(candidate and candidate.x==x and candidate.z==z,typ..' r='..r..' '..portKind..' expected '..x..','..z..' got '..tostring(candidate and candidate.x)..','..tostring(candidate and candidate.z)..' level '..buildLevel)
   assert(buildLevel==port.level,'belt failed to adopt elevator port height')
   local belt={id=100,machineType='Belt',x=candidate.x,z=candidate.z,rotation=rotation,level=buildLevel}
   local connects=if portKind=='output' then Catalog.connected(elevator,belt) else Catalog.connected(belt,elevator)
   assert(connects,'snapped belt points away from elevator')
   assert(Construction.canPlace(state,'Belt',belt.x,belt.z,belt.rotation,nil,belt.level),'snap overlaps elevator footprint')
   cases+=1
  end
 end end
end
-- Elevated drawing must stay on its plane after leaving the magnetic port.
state=Construction.newState(1);buildLevel=1;rotation=0
dragStroke={cells={{x=10,z=10}},level=1}
aim(10,14,1);groundAt({})
assert(candidate.x==10 and candidate.z==14 and buildLevel==1,'elevated stroke drifted toward the ground plane')
-- A lower outlet cannot silently lower an in-progress elevated stroke.
Construction.apply(state,1,{kind='place',machineType='ElevatorDown',x=10,z=13,rotation=0,level=0})
aim(10,14,1);groundAt({})
assert(buildLevel==1,'stroke changed height halfway through')
-- Explicit height choice wins over automatic detection.
dragStroke=nil;heightOverride=true;buildLevel=0
aim(10,12,1);groundAt({})
assert(buildLevel==0,'manual height selection was ignored')
print('PASS actual groundAt elevator snapping: '..cases..' port/rotation/subgrid cases and height locks')

-- Reproduce an entire manually built route, not a preconfigured demo.
state=Construction.newState(1);dragStroke=nil;heightOverride=false;rotationOverride=false;buildLevel=0
for _,rec in ipairs({
 {machineType='Receiver',x=10,z=2},
 {machineType='ElevatorUp',x=10.5,z=5},
 {machineType='ElevatorDown',x=10.5,z=9},
 {machineType='Seller',x=10,z=11},
})do
 rec.kind='place';rec.rotation=0;rec.level=0
 assert(Construction.apply(state,1,rec))
end
aim(10.5,4,0);groundAt({})
assert(Construction.apply(state,1,{kind='place',machineType='Belt',x=candidate.x,z=candidate.z,level=buildLevel,rotation=rotation}))
aim(10.5,6,1);groundAt({})
assert(buildLevel==1)
beginStroke({})
aim(10.5,8,1);strokeTo({})
assert(#dragStroke.cells==3 and buildLevel==1,'real stroke did not remain elevated')
endStroke()
assert(lastSent.kind=='place_many' and #lastSent.placements==3,'stroke did not submit its three belts')
assert(Construction.applyMany(state,1,lastSent.placements))
aim(10.5,10,0);groundAt({})
assert(buildLevel==0,'down elevator did not reconnect to ground')
assert(Construction.apply(state,1,{kind='place',machineType='Belt',x=candidate.x,z=candidate.z,level=buildLevel,rotation=rotation}))
local session={state=state,models={}}
Simulation.newSession(session)
for tick=1,100 do clockNow=tick*.6;Simulation.tick(session)end
assert(session.sales>0,'manually snapped elevator circuit never sold anything')
print('PASS manually placed up / elevated drag / down / seller: '..session.sales..' sales')

-- At coincident screen projections, choose the nearer port; T can expose the lower one.
state=Construction.newState(1);buildLevel=0;rotation=0;heightOverride=false
assert(Construction.apply(state,1,{kind='place',machineType='ElevatorUp',x=10,z=10,rotation=2,level=0}))
cameraRay={Origin={X=42,Y=40,Z=6.9},Direction={X=0,Y=-1,Z=1}}
groundAt({})
assert(candidate.x==10 and candidate.z==9 and buildLevel==1,'occluded lower port won over visible upper port')
heightOverride=true;buildLevel=0;groundAt({})
assert(candidate.x==10 and candidate.z==11 and buildLevel==0,'manual height cannot select the lower coincident port')

-- The actual T handler cancels a live stroke and fixes the new plane.
heightOverride=false;buildLevel=1
aim(10,9,1);beginStroke({})
assert(#dragStroke.cells==1)
lastSent=nil
actions.height()
assert(buildLevel==0 and heightOverride and dragStroke==nil,'T did not cancel and lock the stroke')
endStroke()
assert(lastSent==nil,'cancelled stroke sent a construction request')
groundAt({})
assert(buildLevel==0,'automatic detection overrode the T handler')

-- Manual rotation must not be replaced with the nearby port direction.
heightOverride=false;rotationOverride=true;rotation=0;buildLevel=1
aim(10,9,1);groundAt({})
assert(rotation==0,'automatic snap overrode manual rotation')
print('PASS real stroke submission/cancellation, T callback and manual rotation priority')
