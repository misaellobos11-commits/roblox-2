"""Round-trip actual sky/cloud properties through Roblox's schema via Rojo."""
import copy,json,subprocess,sys,tempfile,math
from pathlib import Path
import xml.etree.ElementTree as ET
r=ET.parse(sys.argv[1]).getroot()
sky=next(i for i in r.iter('Item') if i.get('class')=='Sky')
clouds=next(i for i in r.iter('Item') if i.get('class')=='Clouds')
with tempfile.TemporaryDirectory() as d:
 p=Path(d)
 for name,item in (('Sky',sky),('Clouds',clouds)):
  root=ET.Element('roblox',{'version':'4'});root.append(copy.deepcopy(item))
  ET.ElementTree(root).write(p/(name+'.rbxmx'),encoding='utf-8')
 tree={'$className':'DataModel','Lighting':{'$className':'Lighting','MatterloomDesertSky':{'$path':'Sky.rbxmx'}},
       'Workspace':{'$className':'Workspace','Terrain':{'$className':'Terrain','CanyonClouds':{'$path':'Clouds.rbxmx'}}}}
 project=p/'sky.project.json';project.write_text(json.dumps({'name':'SkySchema','tree':tree}))
 subprocess.run(['/workspace/tools/bin/rojo','build',str(project),'-o',str(p/'roundtrip.rbxlx')],check=True)
 parsed=ET.parse(p/'roundtrip.rbxlx').getroot()
 for cls,original in (('Sky',sky),('Clouds',clouds)):
  out=next(i for i in parsed.iter('Item') if i.get('class')==cls)
  for value in original.find('Properties'):
   key=value.get('name');other=out.find(f"Properties/*[@name='{key}']")
   assert other is not None,(cls,key,'missing')
   if value.tag in ('float','int'):assert math.isclose(float(value.text),float(other.text),rel_tol=1e-6,abs_tol=1e-6)
   elif value.tag in ('Vector3','Color3'):
    for component in value:assert math.isclose(float(component.text),float(other.findtext(component.tag)),rel_tol=1e-6,abs_tol=1e-6)
   elif value.tag=='Content':assert value.findtext('url')==other.findtext('url')
   else:assert value.text==other.text,(key,value.text,other.text)
print('PASS Roblox Sky/Clouds schema: textures, celestial sizes, orientation, stars and cloud properties preserved')
