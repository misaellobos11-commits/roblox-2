local model=Instance.new('Model')
local anchor=Instance.new('Part');anchor.Parent=model;model.PrimaryPart=anchor
anchor.CFrame=CFrame.new(10,5,20)
model:SetAttribute('MachineType','Belt')
for _,entry in ipairs({0,-1,1})do
 Visual.setCargo(model,nil)
 model:SetAttribute('CornerFromX',entry)
 tweens={}
 Visual.setCargo(model,'Carbon')
 local cube=model:FindFirstChild('Producto')
 local start=anchor.CFrame:PointToWorldSpace(if entry==0 then Vector3.new(0,1.52,-1.92) else Vector3.new(entry*1.92,1.52,0))
 assert((cube.CFrame.Position-start).Magnitude<1e-4,'cargo starts inside cell instead of at its inlet')
 assert(#tweens==1,'one continuous progress tween should drive the complete belt path')
 local progress=tweens[1].object
 assert(progress:IsA('NumberValue'),'belt curve must use continuous path progress')
 for _,t in ipairs({.25,.5,.75,1})do
  progress.Value=t
  local p=anchor.CFrame:Inverse():PointToWorldSpace(cube.CFrame.Position)
  assert(math.abs(p.Y-1.52)<1e-4,'cargo clips into belt deck')
  if entry~=0 and t<1 then assert(p.X*entry>0 and p.Z>0,'curve cuts through center or makes a right-angle snap')end
 end
 local expected=anchor.CFrame:PointToWorldSpace(Vector3.new(0,1.52,1.92))
 assert((cube.CFrame.Position-expected).Magnitude<1e-4,'cargo ends before outlet edge')
 -- Blocked output holds one package still; it must not loop back to the inlet.
 local n=#tweens
 Visual.setCargo(model,'Carbon')
 assert(#tweens==n,'blocked package restarted itself')
 Visual.transferCargo(model,'Carbon','front')
 assert(progress.destroyed and tweens[n].cancelled,'delivered cargo did not clean up its old animation')
 Visual.setCargo(model,'Carbon')
 assert(#tweens==n+1,'next identical package did not restart after accepted delivery')
end
print('PASS continuous straight/curved belt paths, blocking and repeated identical cargo')
