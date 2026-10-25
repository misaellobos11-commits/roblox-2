-- Actual drawStroke output must visibly show forward direction at either height.
local cases=0
for r=0,3 do
 for level=0,1 do
  rotation=r;buildLevel=level
  dragStroke={cells={{x=10,z=10},{x=10,z=9},{x=11,z=9}}}
  drawStroke()
  local heads={}
  for _,part in ipairs(dragGhost.children) do
   if part.Name=='PuntaPrevista' then table.insert(heads,part) end
  end
  assert(#heads==6,'each preview belt needs two arrowhead legs')
  for i=1,3 do
   local a,b=heads[i*2-1],heads[i*2]
   local tip=a.CFrame.target
   assert((tip-b.CFrame.target).Magnitude<1e-5,'preview chevron tips must meet')
   local center=(a.CFrame.position+b.CFrame.position)*.5
   local direction=tip-center
   if i==1 then
    assert(direction.Z<0 and math.abs(direction.X)<1e-5,'preview opposes initial north stroke')
   else
    assert(direction.X>0 and math.abs(direction.Z)<1e-5,'preview opposes east turn')
   end
   assert(math.abs(tip.Y-(7+.66+.08+8*level))<1e-5,'preview at wrong build level')
  end
  cases+=1
 end
end
print('PASS visible stroke arrowheads and build height: '..cases..' cases')
