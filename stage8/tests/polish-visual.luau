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
