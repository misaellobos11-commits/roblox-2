-- Art must stay inside the placement footprint at every supported rotation.
local maxParts=0
for _,typ in ipairs(Catalog.expansionOrder)do
 for rotation=0,3 do
  local record={id=1,machineType=typ,x=0,z=0,rotation=rotation,level=0}
  local model=Visual.create(Instance.new('Folder'),record,Vector3.zero,false)
  local inverse=model.PrimaryPart.CFrame:Inverse();local count=0
  for _,p in ipairs(model:GetDescendants())do
   if p:IsA('BasePart') and p.Transparency~=1 then
    count+=1
    if p.Name~='Foundation' then assert(p.CastShadow==false,'decorative shadow cost changed '..typ..'/'..p.Name)end
    local localFrame=inverse*p.CFrame
    for _,x in ipairs({-.5,.5})do for _,y in ipairs({-.5,.5})do for _,z in ipairs({-.5,.5})do
     if p.ClassName~='WedgePart' or y<0 or z>0 then
      local at=localFrame:PointToWorldSpace(Vector3.new(x*p.Size.X,y*p.Size.Y,z*p.Size.Z))
      assert(math.abs(at.X)<=4.1 and math.abs(at.Z)<=4.1,'decoration exceeds footprint: '..typ..'/'..p.Name)
      assert(at.Y>=-.01 and at.Y<=8,'height outside machine envelope: '..typ..'/'..p.Name)
     end
    end end end
   end
  end
  maxParts=math.max(maxParts,count)
  model:Destroy()
 end
end
print('PASS polished geometry footprint in 80 rotations; maximum visible parts: '..maxParts)
local sensor=Visual.create(Instance.new('Folder'),{id=1,machineType='SensorAssembler',x=0,z=0,rotation=0,level=0},Vector3.zero,false)
local inverse=sensor.PrimaryPart.CFrame:Inverse()
local lenses,rims={},{}
for _,p in ipairs(sensor:GetDescendants())do
 if p.Name=='CristalCalibracion' then table.insert(lenses,p)end
 if p.Name=='AnilloOptico' then table.insert(rims,p)end
end
assert(#lenses==2 and #rims==2)
for _,lens in ipairs(lenses)do
 local at=inverse:PointToWorldSpace(lens.CFrame.Position)
 for _,rim in ipairs(rims)do
  local rimAt=inverse:PointToWorldSpace(rim.CFrame.Position)
  if math.abs(at.X-rimAt.X)<.01 then
   assert(at.Z+lens.Size.X/2>rimAt.Z+rim.Size.X/2+.04,'solid optical rim hides the colored lens')
   assert(lens.Size.Y<rim.Size.Y,'lens hides surrounding rim')
  end
 end
end
sensor:Destroy()
print('PASS both sensor lenses remain visible in front of their optical rims')
