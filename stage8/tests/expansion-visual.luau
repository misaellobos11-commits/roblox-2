local signatures={}
for _,typ in ipairs(Catalog.expansionOrder) do
 for rotation=0,3 do
  local rec={id=1,machineType=typ,x=0,z=0,rotation=rotation,level=0}
  local model=Visual.create(Instance.new('Folder'),rec,Vector3.zero,false)
  assert(model:GetAttribute('ExpansionModel')==typ,'new machine has no authored design: '..typ)
  local ports=assert(model:FindFirstChild('Puertos'))
  local inverse=model.PrimaryPart.CFrame:Inverse()
  for _,p in ipairs(Catalog.inputPorts({machineType=typ,x=0,z=0,rotation=0,level=0}))do
   local mouth=assert(ports:FindFirstChild('input_'..p.tag)):FindFirstChild('Boca')
   local at=inverse:PointToWorldSpace(mouth.CFrame.Position)
   assert((at-Vector3.new((p.x-1)*4,.9,(p.z-1)*4)).Magnitude<.001,'mouth position mismatch '..typ)
  end
  assert(ports:FindFirstChild('output_front'),'no visible output')
  assert(model:FindFirstChild('Base').CanQuery,'machine cannot be selected')
  local signature={};local count=0
  for _,p in ipairs(model:GetDescendants())do
   if p:IsA('BasePart') and p.Name~='Base' and p.Name~='Anchor' then
    assert(not p.CanCollide and not p.CanTouch and not p.CanQuery)
    count+=1;table.insert(signature,p.Name)
   end
  end
  assert(count<100,'machine too heavy '..typ)
  if rotation==0 then
   local key=table.concat(signature,'|');assert(not signatures[key],'duplicate machine silhouette '..typ);signatures[key]=true
  end
  model:Destroy()
 end
end
print('PASS 20 distinct machine models, selectable hitboxes and ports in 80 placements')
