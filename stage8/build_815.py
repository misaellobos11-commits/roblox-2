#!/usr/bin/env python3
"""Remove the forty pointed rocks reported at the foot of the retaining walls."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_814 import main as build_previous,OUTPUT as PREVIOUS
from world.canyon import generate
from world.refine_814 import refine

OUTPUT=BASE.parent/'build'/'Matterloom_8_15_Perimetro_Despejado.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_815.rbxmx'

def main():
    build_previous()
    original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    world=next(i for i in root.iter('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomWorld')
    expected=refine(generate(),include_talus=False).world
    for item in expected.iter('Item'):item.set('referent',item.get('referent').replace('RBX_CANYON_','RBX_CANYON814_'))
    previous_ids={i.get('referent'):i for i in world.iter('Item')}
    remaining_ids={i.get('referent') for i in expected.iter('Item')}
    assert remaining_ids<=previous_ids.keys()
    removed=previous_ids.keys()-remaining_ids
    assert len(removed)==680,'Expected forty rocks: sixteen face wedges and one collision hull each'
    for ref in removed:
        item=previous_ids[ref]
        assert item.findtext("Properties/string[@name='Name']") in ('RockFacet','RockCollision')
        frame=item.find("Properties/CoordinateFrame[@name='CFrame']")
        assert max(abs(float(frame.findtext(axis))) for axis in ('X','Z'))<600,'Cannot remove a distant canyon formation'
    for parent in world.iter():
        for child in list(parent):
            if child.get('referent') in removed:parent.remove(child)
    assert ET.tostring(world)==ET.tostring(expected),'Unrelated scene geometry changed'
    changed=[]
    for item in root.iter('Item'):
        source=item.find("Properties/ProtectedString[@name='Source']")
        if source is not None and 'PRUEBAS · 8.14' in (source.text or ''):
            source.text=replace_once(source.text,'PRUEBAS · 8.14','PRUEBAS · 8.15');changed.append(source)
    assert len(changed)==1
    # Compare the complete place after normalizing precisely the authorized removals/tag.
    normalized=copy.deepcopy(root)
    for source in normalized.findall('.//Properties/ProtectedString[@name="Source"]'):
        if source.text:source.text=source.text.replace('PRUEBAS · 8.15','PRUEBAS · 8.14')
    for parent in original.iter():
        for child in list(parent):
            if child.get('referent') in removed:parent.remove(child)
    assert ET.tostring(normalized)==ET.tostring(original),'Change outside the removed rocks/version tag'
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    model=ET.Element('roblox',{'version':'4'});model.append(world)
    ET.ElementTree(model).write(WORLD,encoding='utf-8',xml_declaration=True)
    print('PASS removed 40 low pointed rocks and their collision hulls (680 parts); all other content preserved')
    print('Built',OUTPUT)

if __name__=='__main__':main()
