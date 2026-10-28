local function count(t)local n=0;for _ in pairs(t)do n+=1 end;return n end
assert(count(Catalog.types)==44,'expected 20 additional machines (44 types total)')
assert(count(Catalog.recipes)==53,'expected 40 new recipes')
assert(count(Catalog.items)==54,'expected 40 new resources')
assert(#Catalog.order==44 and #Catalog.filterOrder==54,'all types/items must be accessible')
local seen={}
for _,id in ipairs(Catalog.order)do assert(Catalog.types[id] and not seen[id]);seen[id]=true end
seen={}
for _,id in ipairs(Catalog.filterOrder)do assert(Catalog.items[id] and not seen[id]);seen[id]=true end
assert(Economy.tier(9999)==5 and Economy.tier(10000)==6 and Economy.tier(25000)==7 and Economy.tier(60000)==8)
assert(Economy.startCash==700 and Economy.price('Smelter')==720)
local owners={}
for typ,list in pairs(Catalog.recipeOrder)do
 assert(Catalog.types[typ] and Catalog.details[typ] and Economy.price(typ)>0)
 local threshold=Economy.unlockThresholds[Economy.tiers[typ]]
 assert(Economy.unlocked(typ,threshold))
 if threshold>0 then assert(not Economy.unlocked(typ,threshold-1))end
 for _,id in ipairs(list)do assert(not owners[id]);owners[id]=typ end
end
-- Reachability at EACH advertised unlock tier, including alternative recipes.
for tier=1,8 do
 local reachable={RawMatter=true}
 for _=1,54 do
  for id,r in pairs(Catalog.recipes)do
   if Economy.tiers[owners[id]]<=tier then
    local ready=true;for item in pairs(r.inputs)do if not reachable[item]then ready=false end end
    if ready then for item in pairs(r.outputs)do reachable[item]=true end end
   end
  end
 end
 for id,r in pairs(Catalog.recipes)do
  if Economy.tiers[owners[id]]<=tier then
   for item in pairs(r.outputs)do assert(reachable[item],'unreachable at unlock tier: '..id)end
  end
 end
 if tier==8 then assert(count(reachable)==54)end
end
local function session(records)
 local s={state={buildings=records},models={}};Simulation.newSession(s);return s
end
local function tick(s,t)clockNow=t;Simulation.tick(s)end
local function slots(input,output)return {input=input or {},output=output or {},last=0,alternate=false,totalMade=0,totalMoved=0,nextRoute=0}end
local function ingredients(r)
 local t={};for item,n in pairs(r.inputs)do for _=1,n do table.insert(t,item)end end;return t
end
local function rotation(dx,dz)
 for r=0,3 do local x,z=Catalog.forward(r);if x==dx and z==dz then return r end end
 error('invalid direction')
end
for id,r in pairs(Catalog.recipes)do
 local typ=assert(owners[id]);local inValue,outValue,total=0,0,0
 assert(count(r.inputs)<=2 and count(r.outputs)==1 and r.seconds>0)
 for item,n in pairs(r.inputs)do assert(Catalog.items[item] and n>=1 and n<=2);total+=n;inValue+=Catalog.items[item].value*n end
 for item,n in pairs(r.outputs)do assert(Catalog.items[item] and n==1);outValue+=Catalog.items[item].value*n end
 assert(total<=12 and outValue>inValue,'invalid capacity/value: '..id)
 local rec={id=1,machineType=typ,x=10,z=10,rotation=0,level=0,recipeId=id}
 local s=session({[1]=rec});s.runtime[1]=slots(ingredients(r))
 tick(s,0);assert(s.runtime[1].totalMade==0)
 tick(s,20);assert(s.runtime[1].totalMade==1 and #s.runtime[1].input==0 and #s.runtime[1].output==1,'recipe failed '..id)
 for item in pairs(r.outputs)do assert(s.runtime[1].output[1]==item)end
 tick(s,40);assert(s.runtime[1].totalMade==1,'made product without ingredients')
 s=session({[1]=rec});local missing=ingredients(r);table.remove(missing);s.runtime[1]=slots(missing)
 tick(s,20);assert(#s.runtime[1].input==#missing and #s.runtime[1].output==0,'partial recipe consumed '..id)
 s=session({[1]=rec});s.runtime[1]=slots(ingredients(r),{'Carbon','Carbon','Carbon','Carbon','Carbon'})
 tick(s,20);assert(#s.runtime[1].input==total and #s.runtime[1].output==5,'blocked output consumed input '..id)
 for rot=0,3 do
  rec=table.clone(rec);rec.rotation=rot
  local ports=Catalog.inputPorts(rec)
  assert(#ports>=count(r.inputs),'not enough independent input ports '..typ)
  local records={[1]=rec};local j=0
  s=session(records)
  for item,n in pairs(r.inputs)do
   j+=1;local p=ports[j];local source={id=j+1,machineType='Belt',x=p.x+p.dx*.5-.5,z=p.z+p.dz*.5-.5,rotation=rotation(-p.dx,-p.dz),level=0}
   assert(Catalog.connected(source,rec),'input disconnected '..typ..' rotation '..rot)
   local wrong=table.clone(source);wrong.rotation=(wrong.rotation+2)%4;assert(not Catalog.connected(wrong,rec))
   records[source.id]=source
   local buffer={};for _=1,n do table.insert(buffer,item)end
   s.runtime[source.id]=slots({},buffer)
  end
  local p=Catalog.outputs(rec)[1]
  local seller={id=10,machineType='Seller',x=p.x+p.dx-1,z=p.z+p.dz-1,rotation=rot,level=0}
  assert(Catalog.connected(rec,seller),'output disconnected '..typ)
  records[10]=seller
  tick(s,0);tick(s,.6);tick(s,20)
  assert(s.sales==1 and s.cash==Economy.startCash+outValue,'delivery/sale failed '..id..' '..rot)
 end
 -- Real placement/configuration validators accept every registered recipe.
 local state=Construction.newState(1)
 local ok,err,buildingId=Construction.apply(state,1,{kind='place',machineType=typ,x=10,z=10,rotation=0})
 assert(ok,err)
 ok,err=Construction.apply(state,1,{kind='configure_recipe',id=buildingId,recipeId=id});assert(ok,err)
 local invalid=Construction.apply(state,1,{kind='configure_recipe',id=buildingId,recipeId='missing_recipe'})
 assert(not invalid and state.buildings[buildingId].recipeId==id)
end
for item in pairs(Catalog.items)do
 local state=Construction.newState(1)
 local ok,err,id=Construction.apply(state,1,{kind='place',machineType='FilterLeft',x=10,z=10,rotation=0});assert(ok,err)
 ok,err=Construction.apply(state,1,{kind='configure_filter',id=id,item=item});assert(ok,err)
 assert(Catalog.routeOrder(state.buildings[id],item)[1]=='left')
end
print('PASS 44 types / 53 recipes / 54 items; tier reachability, consumption, blockages, 212 rotated deliveries, sales, placement and filters')
