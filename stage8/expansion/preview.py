"""Auxiliary XML gallery using the exact machine shape specifications."""
import math
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from world.scene import Scene
from expansion.models import MODELS
from expansion.content import MACHINES

def rotation(degrees):
    x,y,z=map(math.radians,degrees);cx,sx,cy,sy,cz,sz=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
    return (cy*cz,-cy*sz,sy,cx*sz+sx*sy*cz,cx*cz-sx*sy*sz,-sx*cy,sx*sz-cx*sy*cz,sx*cz+cx*sy*sz,cx*cy)

def main():
    scene=Scene()
    for index,m in enumerate(MACHINES):
        x=(index%4-1.5)*12;z=(index//4-2)*13
        group=scene.item(scene.world,'Model',m['id'])
        scene.part(group,'Expositor',(11,.25,12),(x,-.2,z),(27,40,48),'Metal')
        for part in MODELS[m['id']]:
            scene.part(group,part['name'],part['size'],(x+part['pos'][0],part['pos'][1],z+part['pos'][2]),part['color'],part['material'],rotation(part['rot']),False,shape={'Block':1,'Cylinder':2,'Ball':0}[part['shape']],kind=part['kind'])
        scene.part(group,'Salida',(2.2,.18,.14),(x,.9,z+4),(114,230,255),'Neon',collide=False)
        if any(len(r[2])>1 for r in m['recipes']):
            for side in (-1,1):scene.part(group,'Entrada',(.14,.18,2.2),(x+side*4,.9,z),(255,118,46),'Neon',collide=False)
        else:scene.part(group,'Entrada',(2.2,.18,.14),(x,.9,z-4),(255,118,46),'Neon',collide=False)
    ET.ElementTree(scene.root).write('build/Expansion_821_Preview.rbxmx',encoding='utf-8',xml_declaration=True)

if __name__=='__main__':main()
