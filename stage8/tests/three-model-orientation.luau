-- The user's 8.9 screenshots identify these three rear-facing bodies only.
-- This checks transform composition, not the external mesh vertices in Studio.
local corrected={Receiver=true,ElementSynthesizer=true,FusionChamber=true}
local count=0
for typ in pairs(Catalog.types) do
 for r=0,3 do
  local owner=wrapper(typ,r)
  assert(installBlenderAsset(owner,visualKeys[typ]))
  local original=owner.PrimaryPart.CFrame:VectorToWorldSpace(Vector3.new(0,0,1))
  local actual=cloned:GetPivot():VectorToWorldSpace(Vector3.new(0,0,1))
  local expected=original*(if corrected[typ] then -1 else 1)
  assert(vectorMatches(actual,expected),'wrong artwork orientation for '..typ..' rotation '..r)
  assert(vectorMatches(cloned:GetPivot().Position,owner.PrimaryPart.CFrame.Position),'rotation displaced '..typ)
  if corrected[typ] then
   local x,z=Catalog.forward(r)
   local mouth=cloned:GetPivot():VectorToWorldSpace(Vector3.new(0,0,-1))
   assert(vectorMatches(mouth,Vector3.new(x,0,z)),'rear-facing mouth does not align with output')
  end
  count+=1
 end
end
print('PASS three corrected bodies and all other import orientations preserved: '..count..' rotation cases')
