-- Finite test supplies; never replace a populated parcel or bypass ownership.
local Catalog=require(script.Parent.MachineCatalog)
local Construction=require(script.Parent.Construction)
local Demo={}
function Demo.stage(state,owner)
 if Construction.count(state)>0 then return nil,'expansion_requires_empty' end
 local staged=Construction.fromSnapshot(Construction.snapshot(state))
 local seeds={}
 local function place(typ,x,z,rot)
  local ok,reason,id=Construction.apply(staged,owner,{kind='place',machineType=typ,x=x,z=z,rotation=rot,level=0})
  if not ok then error(reason) end
  return id
 end
 local ok,err=pcall(function()
  for index,typ in ipairs(Catalog.expansionOrder)do
   local x=4+(index-1)%4*12;local z=3+math.floor((index-1)/4)*9
   local id=place(typ,x,z,0)
   local recipe=Catalog.recipeFor(staged.buildings[id]);local ingredients={}
   for item in pairs(recipe.inputs)do table.insert(ingredients,item)end
   table.sort(ingredients)
   for n,item in ipairs(ingredients)do
    local storageId
    if Catalog.dualInput(staged.buildings[id]) then
     if n==1 then
      storageId=place('Storage',x-4,z,3)
      place('Belt',x-2,z+.5,3);place('Belt',x-1,z+.5,3)
     else
      storageId=place('Storage',x+4,z,1)
      place('Belt',x+3,z+.5,1);place('Belt',x+2,z+.5,1)
     end
    else
     storageId=place('Storage',x,z-2,0)
    end
    seeds[storageId]={}
    for _=1,12*recipe.inputs[item]do table.insert(seeds[storageId],item)end
   end
   place('Belt',x+.5,z+2,0);place('Seller',x,z+3,0)
  end
 end)
 if not ok then return nil,'expansion_blocked',tostring(err) end
 return staged,seeds
end
return Demo
