local count=0
local function partsOf(root)
 local result={}
 for _,p in ipairs(root:GetDescendants()) do if p:IsA('BasePart') then table.insert(result,p) end end
 return result
end
for item in pairs(Catalog.items) do
 count+=1
 for _,typ in ipairs({'Belt','SplitterLeft','FilterRight','ElevatorUp','ElevatorDown'}) do
  local model=Instance.new('Model')
  local anchor=Instance.new('Part');anchor.Parent=model;model.PrimaryPart=anchor
  model:SetAttribute('MachineType',typ)
  anchor.CFrame=CFrame.new(12,8,24)*CFrame.Angles(0,math.pi/2,0)
  Visual.setCargo(model,item)
  local carrier=model:FindFirstChild('Producto')
  assert(carrier.Transparency==1,'Resource is still an undifferentiated opaque cube: '..item)
  local parts=partsOf(carrier);assert(#parts>=3 and #parts<=6,'Resource part budget: '..item)
  local offsets={}
  for _,p in ipairs(parts) do
   assert(p.CanCollide==false and p.CanTouch==false and p.CanQuery==false,'Cargo blocks physics/selection')
   assert(p.Anchored==true and p.CastShadow==false)
   assert(p.Material~=Enum.Material.Neon,'Body is still a glowing cube')
   offsets[p]=carrier.CFrame:Inverse()*p.CFrame
  end
  -- The entire silhouette must follow arbitrary movement/rotation of the existing carrier.
  for _,angle in ipairs({0,math.pi/2,math.pi,math.pi*1.5}) do
   carrier.CFrame=CFrame.new(20,30,40)*CFrame.Angles(0,angle,0)
   for _,p in ipairs(parts) do
    local expected=carrier.CFrame*offsets[p]
    assert((p.CFrame.Position-expected.Position).Magnitude<1e-6,'Detail left behind on '..item)
    for k=1,9 do assert(math.abs(p.CFrame.m[k]-expected.m[k])<1e-6) end
   end
  end
  -- All packages sit above the actual 0.92-stud deck and within the belt width.
  carrier.CFrame=CFrame.new(0,if typ=='Belt' then 1.52 else 1.24,0)
  for _,p in ipairs(parts) do
   local size={p.Size.X,p.Size.Y,p.Size.Z}
   for _,x in ipairs({-.5,.5}) do for _,y in ipairs({-.5,.5}) do for _,z in ipairs({-.5,.5}) do
    if p.ClassName~='WedgePart' or y<0 or z>0 then
     local vertex=p.CFrame:PointToWorldSpace(Vector3.new(x*size[1],y*size[2],z*size[3]))
     assert(vertex.Y>=.99 and vertex.Y<=2.2,'Deck/height clearance: '..item..' '..vertex.Y)
     assert(math.abs(vertex.X)<.81 and math.abs(vertex.Z)<.81,'Cargo exceeds cell clearance: '..item)
    end
   end end end
  end
  local signal=carrier:GetPropertyChangedSignal('CFrame')
  Visual.setCargo(model,nil)
  assert(carrier.destroyed)
  for _,c in ipairs(signal.connections) do assert(not c.active,'Cargo motion callback leaked') end
 end
end
assert(count==14,'Missing/added catalog resources need design coverage')
-- Unknown future resources still get a safe fallback until their silhouette is registered.
Catalog.items.FutureMaterial={color=Color3.fromRGB(160,170,180)}
local m=Instance.new('Model');m.PrimaryPart=Instance.new('Part');m.PrimaryPart.Parent=m;m:SetAttribute('MachineType','Belt')
Visual.setCargo(m,'FutureMaterial');assert(#partsOf(m:FindFirstChild('Producto'))==1)
Catalog.items.FutureMaterial=nil
print('PASS all 14 resource models across belts, dividers, filters and lifts: motion, clearances, cleanup and future fallback')
