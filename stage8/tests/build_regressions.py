"""Run actual extracted catalog/drag/demo logic in the Luau CLI, not a reimplementation."""
from pathlib import Path
import re,sys,xml.etree.ElementTree as ET
root=ET.parse(sys.argv[1]).getroot()
sources={}
def visit(item,path=''):
    name=item.findtext("Properties/string[@name='Name']",'')
    path+='/'+name
    if item.attrib['class'] in ('ModuleScript','Script','LocalScript') and not path.startswith('/ServerStorage/'):
        sources[name]=next((p.text or '' for p in item.find('Properties') if p.attrib.get('name')=='Source'),'')
    for child in item.findall('Item'):visit(child,path)
for child in root.findall('Item'):visit(child)
code="local Color3={fromRGB=function(...) return {...} end}\nlocal Catalog=(function()\n"+sources['MachineCatalog']+'\nend)()\n'
construction=sources['Construction'].replace('local Catalog = require(script.Parent.MachineCatalog)','')
code+='local Construction=(function()\n'+construction+'\nend)()\n'
code+="local clockNow=0\nlocal Visual={setCargo=function() end}\nlocal Economy=(function()\n"+sources['Economy']+'\nend)()\n'
simulation=sources['FactorySimulation']
simulation='\n'.join(line for line in simulation.splitlines() if not line.startswith(('local Catalog=require','local Visual=require','local Economy=require')))
simulation=simulation.replace('os.clock()', 'clockNow')
code+='local Simulation=(function()\n'+simulation+'\nend)()\n'
controller=sources['BuildController']
code+='local rotation=0; local buildLevel=0\n'+controller[controller.index('    local function flowRotation'):controller.index('    local function clearStroke')]
code+='''
local failures=0
local function check(name,fn)
 local ok,err=pcall(fn)
 print(if ok then 'PASS '..name else 'FAIL '..name..': '..tostring(err))
 if not ok then failures+=1 end
end
check('logical output agrees with visual +Z rotated pivot in all orientations',function()
 local expected={{0,1},{-1,0},{0,-1},{1,0}}
 for r=0,3 do local x,z=Catalog.forward(r);assert(x==expected[r+1][1] and z==expected[r+1][2]) end
end)
check('drag curves connect through all rotations and selected direction',function()
 local paths={
  {{x=10,z=10},{x=11,z=10},{x=11,z=11}},
  {{x=10,z=10},{x=10,z=11},{x=9,z=11}},
  {{x=10,z=10},{x=9,z=10},{x=9,z=9}},
  {{x=10,z=10},{x=10,z=9},{x=11,z=9}},
  {{x=10,z=10},{x=10,z=11},{x=10,z=12}},
 }
 for r=0,3 do
  rotation=r
  for _,path in paths do
   local orders=pathRotations(path)
   for id,rec in ipairs(orders) do rec.id=id end
   for id=1,#orders-1 do assert(Catalog.connected(orders[id],orders[id+1]),'broken segment at rotation '..r) end
  end
 end
end)
'''
for kind in ['demo','demo_production','demo_mega']:
    section=sources['BuildServer'].split("if order.kind=='"+kind+"' then",1)[1]
    demo=re.search(r'local demo=\{.*?\n\s*\}',section,re.S).group(0)
    code+='\ncheck('+repr(kind+' receivers reach a seller through valid connections')+',function()\n'+demo+'''
 local state=Construction.newState(1)
 for _,entry in ipairs(demo) do
  local ok,err,id=Construction.apply(state,1,{kind='place',machineType=entry.t,x=entry.x,z=entry.z,rotation=entry.r,level=entry.level})
  assert(ok,err)
  state.buildings[id].recipeId=entry.recipeId or state.buildings[id].recipeId
  state.buildings[id].filterItem=entry.filterItem or state.buildings[id].filterItem
 end
 local function reachesSeller(source,seen)
  if source.machineType=='Seller' then return true end
  if seen[source.id] then return false end
  seen[source.id]=true
  for _,target in pairs(state.buildings) do
   if Catalog.connected(source,target) and reachesSeller(target,seen) then return true end
  end
  return false
 end
 for _,rec in pairs(state.buildings) do
  if rec.machineType=='Receiver' then assert(reachesSeller(rec,{}),'receiver '..rec.id..' cannot reach seller') end
 end
 local session={state=state,models={}}
 Simulation.newSession(session)
 for tick=1,200 do clockNow=tick*.6;Simulation.tick(session) end
 assert(session.sales>0,'demo must sell products within 120 simulated seconds')
 print('  sales after 120s:',session.sales)
 for item,quantity in pairs(session.itemsSold) do print('  sold',item,quantity) end
end)
'''
code+="assert(failures==0,tostring(failures)..' regressions failed')\n"
out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
(out/'logic.luau').write_text(code)
for name,source in sources.items(): (out/(name+'.luau')).write_text(source)
print('Extracted',len(sources),'active scripts and generated logic regression harness')
