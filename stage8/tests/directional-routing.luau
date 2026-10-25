-- Independent cardinal fixtures: left is the player's left looking down the belt.
local forwards={{0,1},{-1,0},{0,-1},{1,0}}
local lefts={{1,0},{0,1},{-1,0},{0,-1}}
check('left and right are relative to travel, in all four rotations',function()
 for r=0,3 do
  local rec={id=1,machineType='SplitterThree',x=10,z=10,rotation=r,level=0}
  local left=Catalog.port(rec,'output','left')
  local right=Catalog.port(rec,'output','right')
  assert(left.dx==lefts[r+1][1] and left.dz==lefts[r+1][2],'left goes to the travelers right')
  assert(right.dx==-lefts[r+1][1] and right.dz==-lefts[r+1][2],'right goes to the travelers left')
 end
end)
check('actual splitter overflow and filter transfers use the labeled side',function()
 local function rot(dx,dz)
  for i,v in ipairs(forwards) do if v[1]==dx and v[2]==dz then return i-1 end end
  error('non cardinal direction')
 end
 local cases=0
 for r=0,3 do
  for _,side in ipairs({'Left','Right'}) do
   for _,family in ipairs({'Splitter','Overflow','Filter'}) do
    for _,alternate in ipairs({false,true}) do
     local f,l=forwards[r+1],lefts[r+1]
     local sx,sz=l[1],l[2]
     if side=='Right' then sx,sz=-sx,-sz end
     local a={id=1,machineType=family..side,x=10,z=10,rotation=r,level=0,filterItem='Carbon'}
     local front={id=2,machineType='Belt',x=10+f[1],z=10+f[2],rotation=r,level=0}
     local lateral={id=3,machineType='Belt',x=10+sx,z=10+sz,rotation=rot(sx,sz),level=0}
     local session={state={buildings={[1]=a,[2]=front,[3]=lateral}},models={}}
     Simulation.newSession(session);Simulation.tick(session)
     local item=if family=='Filter' and alternate then 'Oxygen' else 'Carbon'
     session.runtime[1].output={item}
     if family=='Overflow' and alternate then session.runtime[2].output={'Iron'} end
     if family=='Splitter' and alternate then session.runtime[3].output={'Iron'} end
     transfers={}
     clockNow+=.6;Simulation.tick(session)
     local useSide=(family=='Splitter' and not alternate) or (family=='Overflow' and alternate) or (family=='Filter' and not alternate)
     local dest=if useSide then 3 else 2
     assert(#session.runtime[1].output==0 and session.runtime[dest].output[1]==item,
      family..side..' rotation '..r..' sent to opposite side or got blocked')
     local route=if useSide then string.lower(side) else 'front'
     assert(#transfers==1 and transfers[1].route==route and transfers[1].item==item,'visual animation was not told the accepted route')
     cases+=1
    end
   end
  end
 end
 print('  actual transfers:',cases)
end)
