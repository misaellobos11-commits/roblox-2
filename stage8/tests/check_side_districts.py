"""Keep scenery outside factory plots, roads and ramp approaches."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.side_districts import generate
from world.canyon import SLOTS

root=ET.parse(sys.argv[1]).getroot()
def name(item):return item.findtext("Properties/string[@name='Name']")
districts=next(i for i in root.iter('Item') if name(i)=='SideDistricts')
assert ET.tostring(districts)==ET.tostring(generate()),'Side scenery is not deterministic'
assert {name(i) for i in districts.findall('Item')}=={'ServiceWalkways','WestEnergy','WestCooling','EastLogistics','EastMaintenance'}
def bounds(item):
    props=item.find('Properties');cf=props.find("CoordinateFrame[@name='CFrame']")
    pos=[float(cf.findtext(a)) for a in 'XYZ']
    size=[float(props.findtext(f"Vector3[@name='size']/{a}")) for a in 'XYZ']
    extent=[sum(abs(float(cf.findtext(f'R{r}{c}')))*size[c]/2 for c in range(3)) for r in range(3)]
    return [pos[i]-extent[i] for i in range(3)],[pos[i]+extent[i] for i in range(3)]
parts=[i for i in districts.iter('Item') if i.get('class') in ('Part','WedgePart')]
assert 150<len(parts)<500,len(parts)
assert not any(i.get('class') in ('Script','LocalScript','ModuleScript','PointLight','SpawnLocation') for i in districts.iter('Item'))
for p in parts:
    low,high=bounds(p)
    assert p.findtext("Properties/bool[@name='Anchored']")=='true'
    assert max(abs(low[0]),abs(high[0]))<540,'Scenery enters upper terrace'
    inner=min(abs(low[0]),abs(high[0]))
    assert inner>=(443 if name(p)=='StreetConnection' else 449),'Scenery enters street/sidewalk'
    if name(p)=='StreetConnection':assert inner==443,'Service path does not meet the existing outer sidewalk'
    assert high[1]<32,'Scenery blocks campus view above terrace'
    assert low[2]>=40 or high[2]<=-40,('Ramp approach obstructed',name(p),low,high)
    for x,z,_,_ in SLOTS:
        assert not (min(high[0],x+96)>max(low[0],x-96) and min(high[2],z+96)>max(low[2],z-96)),('Plot obstructed',name(p))
    if high[1]>.7 and p.findtext("Properties/bool[@name='CanCollide']")=='true':
        assert min(abs(low[0]),abs(high[0]))>466,'Pedestrian service walk obstructed'
    # Existing supply pipe runs at |x|=500 and y=10; only new connection tubes may touch it.
    if name(p) not in ('ConduitConnection','CoolingConnection'):
        intersects_x=low[0]<502.5 and high[0]>497.5 or low[0]<-497.5 and high[0]>-502.5
        assert not(intersects_x and low[1]<12.5 and high[1]>7.5),('Existing pipe intersects new equipment',name(p))
print(f'PASS {len(parts)} added anchored pieces: four distinct sectors, clear plots/streets/walkways/ramps, no pipe conflicts or extra lights')
