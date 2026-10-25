-- A waiting distributor must not animate a speculative front exit.
local transferCases=0
for _,typ in ipairs({'SplitterLeft','SplitterRight','SplitterThree','OverflowLeft','OverflowRight','FilterLeft','FilterRight'})do
 for r=0,3 do
  local model=Instance.new('Model')
  local anchor=Instance.new('Part');anchor.Parent=model;model.PrimaryPart=anchor
  anchor.CFrame=CFrame.new(10,5,20)*CFrame.Angles(0,-r*math.pi/2,0)
  model:SetAttribute('MachineType',typ)
  tweens={}
  Visual.setCargo(model,'Carbon')
  assert(#tweens==0,'waiting cargo falsely animates toward front')
  local rec={machineType=typ,x=0,z=0,rotation=r,level=0}
  for _,port in ipairs(Catalog.outputs(rec))do
   tweens={}
   Visual.transferCargo(model,'Carbon',port.tag)
   assert(#tweens==1,'accepted delivery needs a single outward tween')
   local goal=tweens[1].goal.CFrame.Position
   assert((goal-Vector3.new(10+port.dx*1.8,6.24,20+port.dz*1.8)).Magnitude<1e-4,'animation opposes accepted output')
   transferCases+=1
  end
 end
end
print('PASS waiting and delivered cargo visualization: '..transferCases..' route/rotation cases')
for _,typ in ipairs({'ElevatorUp','ElevatorDown'})do
 for r=0,3 do
  local model=Instance.new('Model')
  local anchor=Instance.new('Part');anchor.Parent=model;model.PrimaryPart=anchor
  anchor.CFrame=CFrame.new(10,5,20)*CFrame.Angles(0,-r*math.pi/2,0)
  model:SetAttribute('MachineType',typ)
  tweens={}
  Visual.setCargo(model,'Carbon')
  local cube=model:FindFirstChild('Producto')
  local entryY=if typ=='ElevatorUp' then 1.24 else 9.24
  local exitY=if typ=='ElevatorUp' then 9.24 else 1.24
  local expected=anchor.CFrame:PointToWorldSpace(Vector3.new(0,entryY,-1.8))
  assert((cube.CFrame.Position-expected).Magnitude<1e-4,'elevator cargo starts at wrong inlet or height')
  -- Complete the two first tweens to check the full horizontal/vertical route.
  for i=1,2 do
   local tween=tweens[i]
   assert(tween and tween.Completed.callback,'missing elevator movement stage')
   cube.CFrame=tween.goal.CFrame;tween.Completed.callback()
  end
  assert(#tweens==3,'elevator needs entry, vertical movement and exit')
  expected=anchor.CFrame:PointToWorldSpace(Vector3.new(0,exitY,1.8))
  assert((tweens[3].goal.CFrame.Position-expected).Magnitude<1e-4,'elevator cargo misses output deck')
  Visual.transferCargo(model,'Carbon','front')
  tweens={}
  Visual.setCargo(model,'Carbon')
  assert(#tweens==1,'next identical package must restart elevator entry after delivery')
 end
end
print('PASS elevator inlet, vertical travel and outlet heights in all rotations')
