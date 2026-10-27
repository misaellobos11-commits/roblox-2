"""Check real scene bounds, connections and static lighting budget."""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.perimeter_817 import generate
root=ET.parse(sys.argv[1]).getroot()
def name(i):return i.findtext("Properties/string[@name='Name']")
world=next(i for i in root.iter('Item') if name(i)=='MatterloomWorld')
new=next(i for i in world.iter('Item') if name(i)=='PerimeterUtilities')
assert ET.tostring(new)==ET.tostring(generate())
assert len(new.findall('Item'))==4
count=0
for group in new.findall('Item'):
    east_west=name(group) in ('WallESTE','WallOESTE')
    assert len([i for i in group if name(i)=='WallCladding'])==(2 if east_west else 4)
    for p in group.iter('Item'):
        if p.get('class')!='Part':continue
        count+=1;props=p.find('Properties');cf=props.find("CoordinateFrame[@name='CFrame']")
        pos=[float(cf.findtext(a)) for a in 'XYZ']
        size=[float(props.findtext(f"Vector3[@name='size']/{a}")) for a in 'XYZ']
        ext=[sum(abs(float(cf.findtext(f'R{r}{c}')))*size[c]/2 for c in range(3)) for r in range(3)]
        radial=0 if east_west else 2;tangent=2 if east_west else 0
        inner=abs(pos[radial])-ext[radial];outer=abs(pos[radial])+ext[radial]
        assert inner>=(443 if name(p)=='StreetConnection' else 449),(name(p),inner)
        assert outer<540,(name(p),outer)
        assert abs(pos[tangent])-ext[tangent]>=40,('Central ramp clearance',name(p))
        assert abs(pos[tangent])+ext[tangent]<=448
        assert pos[1]+ext[1]<39,'Upper terrace view blocked'
        if east_west:assert inner>=513,'Existing side equipment/pipe conflict'
        if name(p)=='StreetConnection':assert inner==443 and outer>=474
        assert props.findtext("bool[@name='Anchored']")=='true'
lights=[i for i in world.iter('Item') if i.get('class')=='PointLight']
assert len(lights)==20,len(lights)
assert all(i.findtext("Properties/bool[@name='Shadows']")=='false' for i in lights)
assert 300<count<600,count
assert not any(i.get('class') in ('Script','LocalScript','ModuleScript') for i in new.iter('Item'))
print(f'PASS {count} new static pieces: all four walls, clear ramps/roads/plots, existing equipment clear; 20 total unshadowed lights')
