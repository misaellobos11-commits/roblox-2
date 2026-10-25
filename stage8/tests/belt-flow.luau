-- Regression: stale R must not reverse a multi-cell mouse gesture.
check('drag follows the gesture despite any previous R rotation',function()
 local paths={
  {{x=10,z=10},{x=10,z=9},{x=11,z=9},{x=11,z=8}},
  {{x=10,z=10},{x=11,z=10},{x=11,z=11}},
  {{x=10,z=10},{x=10,z=11},{x=9,z=11}},
  {{x=10,z=10},{x=9,z=10},{x=9,z=9}},
  -- Two consecutive opposite bends, like the reported screenshot.
  {{x=10,z=10},{x=10,z=11},{x=11,z=11},{x=11,z=12}},
  {{x=10,z=10},{x=11,z=10},{x=11,z=9},{x=12,z=9}},
 }
 for r=0,3 do
  rotation=r
  for _,path in ipairs(paths) do
   local orders=pathRotations(path)
   assert(orders[1].x==path[1].x and orders[1].z==path[1].z,'stroke was reversed by stale R')
   for i=1,#orders-1 do
    local dx,dz=Catalog.forward(orders[i].rotation)
    assert(dx==path[i+1].x-path[i].x and dz==path[i+1].z-path[i].z,'output opposes mouse movement')
   end
  end
  local single=pathRotations({{x=1,z=2}})
  assert(single[1].rotation==r,'single click must retain R')
 end
end)
check('opposed belts do not transfer cargo, all four rotations',function()
 for r=0,3 do
  local dx,dz=Catalog.forward(r)
  local source={id=1,machineType='Belt',x=10,z=10,rotation=r,level=0}
  local target={id=2,machineType='Belt',x=10+dx,z=10+dz,rotation=(r+2)%4,level=0}
  assert(not Catalog.connected(source,target),'output must not enter another output')
  local session={state={buildings={[1]=source,[2]=target}},models={}}
  Simulation.newSession(session)
  Simulation.tick(session)
  session.runtime[1].output={'RawMatter'}
  for tick=1,5 do clockNow+=.6;Simulation.tick(session) end
  assert(#session.runtime[1].output==1 and #session.runtime[2].output==0,'cargo crossed an opposed belt')
 end
end)
