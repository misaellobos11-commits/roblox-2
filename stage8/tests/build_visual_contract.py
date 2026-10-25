"""Unit-test Visual.create's selectable-footprint contract; this does not emulate Roblox raycasts."""
from pathlib import Path
import sys
folder=Path(sys.argv[1])
source=(folder/'MachineVisual.luau').read_text()
factory=source[source.index('function Visual.create('):source.index('function Visual.setCargo(')]
catalog=(folder/'MachineCatalog.luau').read_text()
code="local Color3={fromRGB=function(...) return {...} end}\nlocal Catalog=(function()\n"+catalog+'\nend)()\n'
code+='''
-- Rendering/import/scaling are external collaborators for this factory unit test.
-- Their geometry and actual click behavior must be checked in Roblox Studio.
local Construction={CELL_SIZE=4}
local Vector3={new=function(...) return {...} end,zero={0,0,0}}
local Enum={SurfaceType={Smooth=0}}
local Instance={new=function(class)
 local object={children={},attributes={}}
 function object:SetAttribute(k,v) self.attributes[k]=v end
 function object:GetAttribute(k) return self.attributes[k] end
 function object:GetDescendants() return self.children end
 function object:GetBoundingBox() return {Position={Y=3.4}},{Y=6.8} end
 function object:FindFirstChild(name)
  if name=='VisualBlender' then return self.visual end
  for _,child in ipairs(self.children) do if child.Name==name then return child end end
 end
 return object
end}
local function block(parent,name,size,pos,color)
 local object={Name=name,Size=size,Position=pos,Color=color}
 function object:IsA(name) return name=='BasePart' end
 table.insert(parent.children,object)
 return object
end
local visualKeys={}
for name in pairs(Catalog.types) do visualKeys[name]=name end
local installBlenderAsset=function(wrapper,key)
 wrapper:SetAttribute('ImportedVisual',true)
 wrapper:SetAttribute('VisualAssetKey',key)
 wrapper.visual={GetBoundingBox=function() return nil,{Y=6.8} end}
 return true
end
local importedLabel=function() end
local makePorts=function() end
local styleTransport=function() end
local styleProcessor=function() end
local label=function() end
local dark,graphite,orange={},{},{}
local Visual={pivot=function() end,setBeltIncoming=function() end}
'''+factory+'''
local cases=0
for machineType,data in pairs(Catalog.types) do
 for _,preview in ipairs({false,true}) do
  local model=Visual.create({}, {machineType=machineType,id=1,x=0,z=0,rotation=0},Vector3.zero,preview)
  local hitbox=model:FindFirstChild('Base')
  assert(hitbox,'imported '..machineType..' must have a selectable wrapper footprint')
  assert(hitbox.CanQuery==not preview,'ghosts must not intercept selection rays')
  assert(hitbox.CanCollide==false and hitbox.CanTouch==false,'selection must not block walking')
  assert(hitbox.Transparency==1,'selection footprint must be invisible')
  assert(hitbox.Size[2]==6.8 and hitbox.Position[2]==3.4,'selection must cover visible height')
  assert(hitbox.Size[1]==data.size*4-.14 and hitbox.Size[3]==data.size*4-.14)
  if preview then
   Visual.setPreview(model,true)
   assert(hitbox.Transparency==1 and hitbox.CanQuery==false)
  end
  cases+=1
 end
end
print('PASS imported selection footprint: '..cases..' factory cases (rendering adapters, not engine execution)')
'''
if '--belt-only' in sys.argv:
    code=code.replace('for machineType,data in pairs(Catalog.types) do',
        "for machineType,data in pairs(Catalog.types) do\n if machineType~='Belt' then continue end")
if '--machines' in sys.argv:
    code=code.replace('for machineType,data in pairs(Catalog.types) do',
        'for machineType,data in pairs(Catalog.types) do\n if data.size~=2 then continue end')
    code=code.replace("  local hitbox=model:FindFirstChild('Base')",
        "  assert(model:GetAttribute('ImportedVisual'),'original machine model was not restored: '..machineType)\n  local hitbox=model:FindFirstChild('Base')")
(folder/'visual-contract.luau').write_text(code)
