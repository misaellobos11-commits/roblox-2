local failures,cases=0,0
local function near(a,b)return (a-b).Magnitude<1e-4 end
for typ,def in pairs(Catalog.types) do
 if typ=='Belt' then continue end
 local ok,err=pcall(function()
  for r=0,3 do for _,preview in ipairs({false,true})do
   local rec={id=1,machineType=typ,x=4,z=7,rotation=r,level=0}
   local origin=Vector3.new(100,5,200)
   local before=importLookups
   local model=Visual.create(Instance.new('Folder'),rec,origin,preview)
   assert(importLookups==before,'functional visual still relies on unverified mesh orientation')
   local ports=model:FindFirstChild('Puertos')
   assert(ports,'machine has no renderable authoritative ports')
   local expected=Catalog.outputs(rec)
   local input=if typ=='Receiver' then {} else Catalog.inputPorts(rec)
   assert(#ports:GetChildren()==#expected+#input,'missing or extra visible port')
   for _,kind in ipairs({'input','output'})do
    for _,p in ipairs(if kind=='input' then input else expected)do
     local group=ports:FindFirstChild(kind..'_'..p.tag)
     assert(group,'missing visible '..kind..' '..p.tag)
     local marker=group:FindFirstChild('Boca')
     assert(near(marker.CFrame.Position,origin+Vector3.new(p.x*4,.90+p.level*8,p.z*4)),'mouth disagrees with simulation port')
     local legs={}
     for _,part in ipairs(group:GetChildren())do if part.Name=='FlechaPuerto'then table.insert(legs,part)end end
     assert(#legs==2,'port needs one unambiguous chevron')
     local tip=legs[1].CFrame:PointToWorldSpace(Vector3.new(0,0,-legs[1].Size.Z/2))
     local tip2=legs[2].CFrame:PointToWorldSpace(Vector3.new(0,0,-legs[2].Size.Z/2))
     local a=legs[1].CFrame:PointToWorldSpace(Vector3.new(0,0,legs[1].Size.Z/2))
     local b=legs[2].CFrame:PointToWorldSpace(Vector3.new(0,0,legs[2].Size.Z/2))
     local sign=if kind=='input' then -1 else 1
     local expectedFlow=Vector3.new(p.dx*sign,0,p.dz*sign)
     assert(near(tip,tip2) and near((tip-(a+b)*.5).Unit,expectedFlow),'visible arrow opposes real flow')
    end
   end
   local base=model:FindFirstChild('Base')
   assert(base and base.CanQuery==not preview and base.CanCollide==false and base.Transparency==1,'selection footprint broken')
   if preview then Visual.setPreview(model,true);assert(base.Transparency==1) end
   if Catalog.isElevator(typ) then
    local shaft=model.PrimaryPart.CFrame:PointToWorldSpace(Vector3.new(0,8.83,0))
    for _,part in ipairs(model:GetDescendants())do
     if part:IsA('BasePart') and part.Transparency~=1 then
      local p=part.CFrame:Inverse():PointToWorldSpace(shaft)
      assert(not (math.abs(p.X)<part.Size.X/2 and math.abs(p.Y)<part.Size.Y/2 and math.abs(p.Z)<part.Size.Z/2),'upper deck closes the elevator shaft')
     end
    end
   end
   cases+=1
  end end
 end)
 if not ok then failures+=1;print('FAIL '..typ..': '..tostring(err))end
end
assert(failures==0,tostring(failures)..' functional visual failures')
print('PASS actual generated mouths, chevrons and selection: '..cases..' type/rotation/preview cases')
