"""Extract the shipped Luau catalog and build a reproducible production audit."""
from pathlib import Path
import hashlib,json,math,subprocess,sys,xml.etree.ElementTree as ET
BASE=Path(__file__).resolve().parents[2]
place=BASE/'build/Matterloom_8_20_Recursos_Transportables.rbxlx'
out=BASE/'stage8/production';tmp=BASE/'build/production-audit';tmp.mkdir(exist_ok=True)
r=ET.parse(place).getroot();sources={}
def walk(i,path=''):
 name=i.findtext("Properties/string[@name='Name']",'');path+='/'+name
 if path.startswith('/ReplicatedStorage/Shared/') and i.get('class')=='ModuleScript':
  sources[name]=i.findtext("Properties/ProtectedString[@name='Source']")
 for c in i.findall('Item'):walk(c,path)
for i in r.findall('Item'):walk(i)
code="local Color3={fromRGB=function(...)return {...}end}\nlocal C=(function()\n"+sources['MachineCatalog']+'\nend)()\nlocal E=(function()\n'+sources['Economy']+'''\nend)()
local function quantities(map)
 local lines={};for key,value in pairs(map)do table.insert(lines,key..':'..value)end
 table.sort(lines);return table.concat(lines,',')
end
print('START\\t'..E.startCash)
for tier,threshold in ipairs(E.unlockThresholds)do print('TIER\\t'..tier..'\\t'..threshold..'\\t'..E.levelNames[tier])end
for id,item in pairs(C.items)do print('ITEM\\t'..id..'\\t'..item.name..'\\t'..item.value)end
for id,machine in pairs(C.types)do print('MACHINE\\t'..id..'\\t'..machine.name..'\\t'..E.prices[id]..'\\t'..E.tiers[id]..'\\t'..table.concat(C.recipeOrder[id]or{},','))end
for id,recipe in pairs(C.recipes)do print('RECIPE\\t'..id..'\\t'..recipe.name..'\\t'..recipe.seconds..'\\t'..quantities(recipe.inputs)..'\\t'..quantities(recipe.outputs))end
print('FILTERS\\t'..table.concat(C.filterOrder,','))
'''
(tmp/'extract.luau').write_text(code)
text=subprocess.check_output(['/workspace/tools/luau-0.744/luau',str(tmp/'extract.luau')],text=True)
(tmp/'catalog.tsv').write_text(text)
d={'version':'8.20','source_sha256':hashlib.sha256(place.read_bytes()).hexdigest(),'items':{},'machines':{},'recipes':{},'tiers':[]}
def quantities(s):return {k:int(v) for k,v in (entry.split(':') for entry in s.split(','))}
for line in text.splitlines():
 p=line.split('\t');kind=p[0]
 if kind=='START':d['start_cash']=int(p[1])
 elif kind=='TIER':d['tiers'].append({'tier':int(p[1]),'threshold':int(p[2]),'name':p[3]})
 elif kind=='ITEM':d['items'][p[1]]={'name':p[2],'value':int(p[3])}
 elif kind=='MACHINE':d['machines'][p[1]]={'name':p[2],'cost':int(p[3]),'tier':int(p[4]),'recipes':p[5].split(',') if p[5] else []}
 elif kind=='RECIPE':d['recipes'][p[1]]={'name':p[2],'seconds':float(p[3]),'inputs':quantities(p[4]),'outputs':quantities(p[5])}
 elif kind=='FILTERS':d['filters']=p[1].split(',')
for rid,recipe in d['recipes'].items():
 recipe['machines']=[mid for mid,m in d['machines'].items() if rid in m['recipes']]
 assert len(recipe['machines'])==1,(rid,'Recipe is orphaned or assigned ambiguously')
 for item in recipe['inputs']|recipe['outputs']:assert item in d['items'],item
 recipe['input_sale_value']=sum(d['items'][item]['value']*n for item,n in recipe['inputs'].items())
 recipe['output_sale_value']=sum(d['items'][item]['value']*n for item,n in recipe['outputs'].items())
 recipe['added_sale_value']=recipe['output_sale_value']-recipe['input_sale_value']
 recipe['ideal_tick_interval']=math.ceil((recipe['seconds']-1e-9)/.6)*.6
reachable={'RawMatter'}
for _ in range(len(d['items'])):
 for recipe in d['recipes'].values():
  if set(recipe['inputs'])<=reachable:reachable.update(recipe['outputs'])
assert reachable==set(d['items']),'Unreachable resource'
d['terminal_items']=sorted(set(d['items'])-{i for recipe in d['recipes'].values() for i in recipe['inputs']})
assert len(d['items'])==14 and len(d['recipes'])==13
assert set(d['terminal_items'])=={'Hydrogen','CarbonCompound','ConductiveMix','BasicCrystal','Ingot'}
assert all(recipe['added_sale_value']>0 for recipe in d['recipes'].values())
d['tiers'].sort(key=lambda t:t['tier'])
(out/'catalogo_8_20.json').write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
# Generate current recipes, without mixing proposed future content into the game data.
order=[rid for mid in ['CarbonProcessor','OxygenProcessor','SiliconProcessor','IronProcessor','CopperProcessor','HydrogenProcessor','FusionChamber','ElementSynthesizer','Crystallizer','MineralFormer','Smelter'] for rid in d['machines'][mid]['recipes']]
def names(q):return ' + '.join(f"{d['items'][k]['name']} ×{v}" for k,v in q.items())
rows=['| Máquina · nivel | Entradas | Salida | Intervalo nominal | Venta entradas → salida | Diferencia |','|---|---|---|---:|---:|---:|']
for rid in order:
 recipe=d['recipes'][rid];machine=d['machines'][recipe['machines'][0]]
 rows.append(f"| {machine['name']} · N{machine['tier']} | {names(recipe['inputs'])} | {names(recipe['outputs'])} | {recipe['seconds']:g} s | ${recipe['input_sale_value']} → ${recipe['output_sale_value']} | +${recipe['added_sale_value']} |")
(out/'RECETAS_ACTUALES.md').write_text('# Recetas actuales — Matterloom 8.20\n\nDatos extraídos del catálogo Luau del archivo entregado. Todas las cantidades actuales son una unidad.\n\n'+'\n'.join(rows)+'\n\nLa diferencia compara el valor de venta del producto con el de sus ingredientes. No es beneficio por segundo: no descuenta maquinaria, cintas, esperas ni cuellos de botella.\n\nLos tiempos son intervalos mínimos entre producciones de una máquina. La simulación revisa cada 0,6 s; en condiciones ideales los intervalos se redondean al siguiente tick y la ejecución real puede demorarse más.\n')
print('PASS audit: 14 reachable resources, 13 assigned recipes, 5 terminal resources; catalog and economy extracted from shipped Luau')
