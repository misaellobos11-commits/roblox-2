#!/usr/bin/env python3
"""Create 8.5 from the uploaded place, preserving its assets and inactive backups."""
from pathlib import Path
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parent
OUTPUT=BASE.parent/'build'/'Matterloom_8_5_Prueba_Conexiones.rbxlx'

def replace_once(source,old,new):
    assert source.count(old)==1, ('Source differs from reviewed 8.4',old[:80])
    return source.replace(old,new,1)

def patch(name,source):
    if name=='MachineCatalog':
        source=replace_once(source,''' -- La salida visual de las máquinas y cintas debe coincidir con la dirección elegida.
 -- En versiones anteriores esto estaba invertido.
 return x,z''',''' -- 8.5: all models, drag paths and demos use local +Z as output.
 -- direction() is the opposite axis; pivot rotates local +Z by -rotation*90°.
 return -x,-z''')
    if name=='MachineVisual':
        source=replace_once(source,'''    if key and installBlenderAsset(model,key) then
        importedLabel''','''    if key and installBlenderAsset(model,key) then
        -- A query-only footprint belongs directly to the authoritative wrapper.
        -- Meshes remain nonqueryable; their nested GLB Models have no ownership ID.
        local width=data.size*Construction.CELL_SIZE
        local _,visualSize=model:FindFirstChild('VisualBlender'):GetBoundingBox()
        local height=math.max(1.1,visualSize.Y)
        local hitbox=block(model,'Base',Vector3.new(width-.14,height,width-.14),Vector3.new(0,height/2,0),dark)
        hitbox.Transparency=1
        hitbox.CanCollide=false
        hitbox.CanTouch=false
        hitbox.CanQuery=not preview
        importedLabel''')
        source=replace_once(source,"if item:IsA('BasePart') and item.Name~='Anchor' then", "if item:IsA('BasePart') and item.Name~='Anchor' and not (item.Name=='Base' and model:GetAttribute('ImportedVisual')) then")
    if name=='BuildUI':
        # Mark the test build visibly without changing layout or economy.
        source=replace_once(source,"'MATTERLOOM  ·  FÁBRICA'", "'MATTERLOOM · 8.5 TEST'")
    return source

def build():
    root=ET.parse(BASE/'original-8.4.rbxlx').getroot()
    changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'')
        path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('MachineCatalog','MachineVisual','BuildUI'):
            node=next((p for p in item.find('Properties') if p.attrib.get('name')=='Source'),None)
            if node is not None:
                node.text=patch(name,node.text or '')
                changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for child in root.findall('Item'):visit(child)
    assert len(changed)==3,changed
    OUTPUT.parent.mkdir(exist_ok=True)
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)
    for path in changed: print('Patched',path)

if __name__=='__main__':build()
