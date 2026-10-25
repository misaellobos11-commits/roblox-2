local failures=0
for _,entry in ipairs({0,-1,1}) do
 local ok,err=pcall(function()
  parts={};segments={}
  local model=object('Belt')
  model.attributes={MachineType='Belt',ImportedVisual=true}
  model.PrimaryPart={CFrame=frame()}
  model.PrimaryPart.CFrame.VectorToObjectSpace=function(_,v)return v end
  installBlenderAsset(model,'Belt_Straight_v2')
  Visual.setBeltIncoming(model,if entry==0 then nil else {dx=-entry,dz=0})
  assert(not model:FindFirstChild('VisualBlender'),'straight mesh still owns unverified baked arrows')
  local arrows=0
  local previous=nil
  for _,s in ipairs(segments) do
   if string.find(s.name,'Flecha') then
    arrows+=1
    -- Direction is from the midpoint of the two tails to their shared tip.
    if previous then
     local tail=(previous.a+s.a)*.5
     assert((previous.b-s.b).Magnitude<1e-5,'chevron must share one tip')
     assert(s.b.Z-tail.Z>=-1e-5,'arrow points opposite to logical +Z output')
     if entry~=0 then assert((s.b.X-tail.X)*entry<=1e-5,'curve arrow points toward inlet') end
     previous=nil
    else previous=s end
   end
  end
  assert(arrows>=6,'belt must draw visible direction markers')
  -- Changing incoming must replace straight/curve geometry without leaving two tracks.
  Visual.setBeltIncoming(model,{dx=1,dz=0})
  assert(model:FindFirstChild('Curva90') and not model:FindFirstChild('RutaCinta'))
  Visual.setBeltIncoming(model,nil)
  assert(model:FindFirstChild('RutaCinta') and not model:FindFirstChild('Curva90'))
 end)
 print(if ok then 'PASS rendered belt entry '..entry else 'FAIL rendered belt entry '..entry..': '..tostring(err))
 if not ok then failures+=1 end
end
assert(failures==0,'belt geometry regressions failed')
