"""Spatial and preservation checks on the delivered scene, not a rendering claim."""
from pathlib import Path
import sys
import math
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.canyon import SLOTS,generate

before=ET.parse(sys.argv[1]).getroot();after=ET.parse(sys.argv[2]).getroot()
def name(i):return i.findtext("Properties/string[@name='Name']")
def find(root,n):return next(i for i in root.iter('Item') if name(i)==n)
world=find(after,'MatterloomWorld')
parts=[i for i in world.iter('Item') if i.get('class') in ('Part','WedgePart','SpawnLocation')]
assert 1000<len(parts)<4500,len(parts)
assert len([i for i in world.iter('Item') if i.get('class')=='PointLight'])<=12
assert len([i for i in world.iter('Item') if i.get('class')=='SpawnLocation'])==1
refs=[i.get('referent') for i in after.iter('Item')]
assert len(refs)==len(set(refs)),'Duplicate instance referents'
preview=find(world,'PreviewPlots');assert len(preview.findall('Item'))==8
for i,(x,z,dx,dz) in zip(preview.findall('Item'),SLOTS):
    floor=find(i,'BuildFloor')
    assert floor.findtext("Properties/Vector3[@name='size']/X")=='192'
    assert float(floor.findtext("Properties/CoordinateFrame[@name='CFrame']/X"))==x
    assert float(floor.findtext("Properties/CoordinateFrame[@name='CFrame']/Z"))==z
    assert abs((x+dx*140) if dx else (z+dz*140))==140

def aabb(p):
    props=p.find('Properties')
    size=[float(props.findtext(f"Vector3[@name='size']/{v}")) for v in 'XYZ']
    cf=props.find("CoordinateFrame[@name='CFrame']")
    pos=[float(cf.findtext(v)) for v in 'XYZ']
    matrix=[[float(cf.findtext(f'R{r}{c}')) for c in range(3)] for r in range(3)]
    for row in matrix:assert abs(sum(v*v for v in row)-1)<1e-6,(name(p),matrix)
    extent=[sum(abs(matrix[r][c])*size[c]/2 for c in range(3)) for r in range(3)]
    return [pos[i]-extent[i] for i in range(3)],[pos[i]+extent[i] for i in range(3)]

preview_parts=set(preview.iter('Item'))
for p in parts:
    assert p.findtext("Properties/bool[@name='Anchored']")=='true'
    low,high=aabb(p)
    if p in preview_parts or high[1]<=.1:continue
    for x,z,_,_ in SLOTS:
        overlap=min(high[0],x+96)-max(low[0],x-96)>.01 and min(high[2],z+96)-max(low[2],z-96)>.01
        assert not overlap,('Decoration enters build footprint',name(p),low,high,(x,z))

# A player walking up the ramp must not hit a solid terrace wall before reaching it.
colliders=[(p,*aabb(p)) for p in parts if p not in preview_parts
           and p.findtext("Properties/bool[@name='CanCollide']")=='true']
for x,z,dx,dz in SLOTS:
    for distance in range(97,151,2):
        point=(x+dx*distance,1,z+dz*distance)
        for p,low,high in colliders:
            assert not all(low[i]+.01<point[i]<high[i]-.01 for i in range(3)),('Plot entrance obstructed',name(p),point)
for prefix in ('Boulevard','Sidewalk'):
    surfaces=[(p,low,high) for p,low,high in colliders if name(p).startswith(prefix)]
    for index,(p,low,high) in enumerate(surfaces):
        for q,other_low,other_high in surfaces[index+1:]:
            coplanar=abs(high[1]-other_high[1])<1e-6
            overlap=all(min(high[i],other_high[i])-max(low[i],other_low[i])>.01 for i in (0,2))
            assert not(coplanar and overlap),('Overlapping road surfaces',name(p),name(q),low,other_low)
for ramp in (p for p in parts if name(p)=='AccessRamp'):
    cf=ramp.find("Properties/CoordinateFrame[@name='CFrame']")
    pos=[float(cf.findtext(v)) for v in 'XYZ']
    matrix=[[float(cf.findtext(f'R{r}{c}')) for c in range(3)] for r in range(3)]
    half=float(ramp.findtext("Properties/Vector3[@name='size']/Z"))/2
    for step in range(41):
        local_z=-half+2*half*step/40
        point=[pos[r]+matrix[r][2]*local_z+matrix[r][1]*.3 for r in range(3)]
        point[1]+=.8
        for other,low,high in colliders:
            if other is ramp:continue
            assert not all(low[i]+.01<point[i]<high[i]-.01 for i in range(3)),('Ramp blocked',name(other),point)

# Script changes are limited to presentation, layout, loader and build version.
def scripts(root):
    result={}
    def visit(i,path=''):
        path+='/'+name(i)
        source=i.find("Properties/ProtectedString[@name='Source']")
        if source is not None:result[path]=source.text
        for c in i.findall('Item'):visit(c,path)
    for i in root.findall('Item'):visit(i)
    return result
old,new=scripts(before),scripts(after);assert old.keys()==new.keys()
expected={'/ReplicatedStorage/Shared/MapConfig','/ServerScriptService/Server/MapGenerator',
          '/ServerScriptService/Server/BuildServer','/StarterPlayer/StarterPlayerScripts/Client/BuildUI'}
assert {k for k in old if old[k]!=new[k]}==expected
for service in ('ReplicatedStorage','ServerStorage','StarterPlayer','ServerScriptService'):
    a=ET.fromstring(ET.tostring(find(before,service)));b=ET.fromstring(ET.tostring(find(after,service)))
    for tree in (a,b):
        for source in tree.findall(".//Properties/ProtectedString[@name='Source']"):source.text=''
    assert ET.tostring(a)==ET.tostring(b),('Non-source asset changed',service)
assert ET.tostring(generate().world)==ET.tostring(world),'Scene must be reproducible'
print(f'PASS canyon: {len(parts)} anchored parts, 8 clear plots, one spawn, bounded lights, unique IDs, unchanged gameplay/assets')
