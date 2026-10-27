"""Make an auxiliary XML contact sheet from the exact authored resource definitions."""
import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.scene import Scene
from cargo_shapes import SHAPES
# Rotation convention matches Roblox CFrame.Angles (Rx*Ry*Rz).
def rotation(degrees):
 x,y,z=map(math.radians,degrees);cx,sx,cy,sy,cz,sz=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
 return (cy*cz,-cy*sz,sy,cx*sz+sx*sy*cz,cx*cz-sx*sy*sz,-sx*cy,sx*sz-cx*sy*cz,sx*cz+cx*sy*sz,cx*cy)
s=Scene()
for index,(item,pieces) in enumerate(SHAPES.items()):
 x=(index%4-1.5)*3.1;z=(index//4-1.5)*3.2
 group=s.item(s.world,'Model',item)
 s.part(group,'DisplayBase',(2.8,.12,2.9),(x,-.10,z),(46,59,66),'Metal')
 for p in pieces:
  at=(x+p['pos'][0],p['pos'][1],z+p['pos'][2])
  s.part(group,p['name'],p['size'],at,p['color'],p['material'],rotation(p['rot']),False,
         shape={'Block':1,'Cylinder':2,'Ball':0}[p['shape']],kind=p['kind'])
import xml.etree.ElementTree as ET
ET.ElementTree(s.root).write('build/Cargo_820_Preview.rbxmx',encoding='utf-8',xml_declaration=True)
