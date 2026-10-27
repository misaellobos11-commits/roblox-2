"""Check the replaced horizon, continuous exterior bounds and clear sky settings."""
import sys,math
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.horizon_819 import generate
r=ET.parse(sys.argv[1]).getroot()
def name(i):return i.findtext("Properties/string[@name='Name']")
def value(i,key):return i.findtext(f"Properties/*[@name='{key}']")
world=next(i for i in r.iter('Item') if name(i)=='MatterloomWorld')
assert not any(name(i)=='CanyonRockFormations' for i in world.iter('Item'))
horizon=next(i for i in world.iter('Item') if name(i)=='StratifiedCanyon')
assert ET.tostring(horizon)==ET.tostring(generate())
parts=[i for i in horizon.iter('Item') if i.get('class') in ('Part','WedgePart')]
assert len(parts)<1500,len(parts)
def bounds(p):
 cf=p.find("Properties/CoordinateFrame[@name='CFrame']")
 pos=[float(cf.findtext(a)) for a in 'XYZ']
 size=[float(p.findtext(f"Properties/Vector3[@name='size']/{a}")) for a in 'XYZ']
 vertices=[(x,y,z) for x in (-.5,.5) for y in (-.5,.5) for z in (-.5,.5)]
 if p.get('class')=='WedgePart':vertices=[v for v in vertices if v[1]<0 or v[2]>0]
 points=[[pos[a]+sum(float(cf.findtext(f'R{a}{b}'))*size[b]*v[b] for b in range(3)) for a in range(3)] for v in vertices]
 return [min(v[i] for v in points) for i in range(3)],[max(v[i] for v in points) for i in range(3)]
for p in parts:
 low,high=bounds(p)
 assert low[0]>=623 or high[0]<=-623 or low[2]>=623 or high[2]<=-623,('Encroaches on buildings/terraces',name(p),low,high)
 assert value(p,'Anchored')=='true'
 assert value(p,'CanCollide')=='true'
feet=[bounds(p) for p in parts if name(p)=='BedrockFoot']
barriers=[bounds(p) for p in parts if name(p)=='OuterSafetyBoundary']
assert len(feet)==len(barriers)==4
# Every point around each rectangular contour is inside a solid wall, including corners.
def contains(box,point):return all(box[0][i]-1e-5<=point[i]<=box[1][i]+1e-5 for i in range(3))
for radius,boxes,heights in ((634,feet,(-.5,40,64)),(884,barriers,(-.5,40,150,300,599))):
 for along in range(-radius,radius+1,2):
  for x,z in ((along,radius),(along,-radius),(radius,along),(-radius,along)):
   for y in heights:assert any(contains(box,(x,y,z)) for box in boxes),('Open perimeter',x,y,z)
clouds=[i for i in r.iter('Item') if i.get('class')=='Clouds'];assert len(clouds)==1
assert .5<=float(value(clouds[0],'Cover'))<=.7
assert value(clouds[0],'Enabled')=='true'
skies=[i for i in r.iter('Item') if i.get('class')=='Sky'];assert len(skies)==1
sky=skies[0];assert float(value(sky,'MoonAngularSize'))<=8
assert int(value(sky,'StarCount'))>=1500
for face in ('Bk','Dn','Ft','Lf','Rt','Up'):
 assert sky.findtext(f"Properties/Content[@name='Skybox{face}']/url").startswith('rbxasset://textures/sky/')
for i in r.iter('Item'):
 if i.get('class')=='Atmosphere':
  for key in ('Density','Haze','Glare'):assert float(value(i,key))==0,'Fog reintroduced'
print(f'PASS {len(parts)} connected cliff pieces; buildings untouched, solid perimeter at all four corners, clear sky/cloud settings')
