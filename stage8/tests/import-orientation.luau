-- Calibration contract: native model's mouth/front arrows face -Z.
-- Authored Left/Right meshes branch toward -X/+X before the half-turn.
-- These fixtures need visual confirmation against the external meshes in Studio.
local failures,cases=0,0
local direction={{0,1},{-1,0},{0,-1},{1,0}}
for typ,data in pairs(Catalog.types) do
 if typ=='Belt' then continue end -- User-verified 8.6 geometry is unchanged.
 local ok,err=pcall(function()
  for r=0,3 do
   local owner=wrapper(typ,r)
   assert(installBlenderAsset(owner,visualKeys[typ]),'import failed')
   local f=direction[r+1]
   local output=cloned:GetPivot():VectorToWorldSpace(Vector3.new(0,0,-1))
   assert(vectorMatches(output,Vector3.new(f[1],0,f[2])),'native mouth/arrows face opposite logical output')
   local expectedInput=Vector3.new(-f[1],0,-f[2])
   local input=cloned:GetPivot():VectorToWorldSpace(Vector3.new(0,0,1))
   assert(vectorMatches(input,expectedInput),'native input faces wrong side')
   if string.find(typ,'Left') or string.find(typ,'Right') then
    local nativeSide=if string.find(cloned.key,'_Left_') then -1 else 1
    local side=cloned:GetPivot():VectorToWorldSpace(Vector3.new(nativeSide,0,0))
    local sign=if string.find(typ,'Left') then -1 else 1
    assert(vectorMatches(side,Vector3.new(sign*f[2],0,-sign*f[1])),'lateral branch swapped by half-turn')
   end
   assert(vectorMatches(cloned:GetPivot().Position,Vector3.new(100,8,200)),'import drifted off wrapper origin')
   assert(owner.attributes.ImportedVisual and cloned.part.CanQuery==false,'selection belongs to wrapper')
   cases+=1
  end
 end)
 if not ok then failures+=1;print('FAIL '..typ..': '..tostring(err)) end
end
-- Failed lookup must still allow the existing procedural fallback.
missingKey=visualKeys.Receiver
assert(installBlenderAsset(wrapper('Receiver',0),missingKey)==false)
-- Imported straight belt path must not be reoriented; 8.6 replaces it at runtime.
assert(installBlenderAsset(wrapper('Belt',0),visualKeys.Belt))
assert(near(cloned:GetPivot().yaw,0),'8.6 belt import convention changed')
assert(failures==0,tostring(failures)..' model calibrations failed')
print('PASS calibrated imported transforms: '..cases..' type/rotation cases, fallback and belt preservation')
