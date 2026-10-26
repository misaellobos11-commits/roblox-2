#!/usr/bin/env python3
"""Populate side service strips while preserving 8.15 gameplay and open ramps."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_815 import main as build_previous,OUTPUT as PREVIOUS
from world.side_districts import generate

OUTPUT=BASE.parent/'build'/'Matterloom_8_16_Sectores_Laterales.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_816.rbxmx'

def main():
    build_previous();original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    world=next(i for i in root.iter('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomWorld')
    districts=generate();world.append(districts)
    changed=0
    for source in root.findall('.//Properties/ProtectedString[@name="Source"]'):
        if source.text and 'PRUEBAS · 8.15' in source.text:
            source.text=replace_once(source.text,'PRUEBAS · 8.15','PRUEBAS · 8.16');changed+=1
    assert changed==1
    normalized=copy.deepcopy(root)
    restored=next(i for i in normalized.iter('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomWorld')
    restored.remove(next(i for i in restored.findall('Item') if i.findtext("Properties/string[@name='Name']")=='SideDistricts'))
    for source in normalized.findall('.//Properties/ProtectedString[@name="Source"]'):
        if source.text:source.text=source.text.replace('PRUEBAS · 8.16','PRUEBAS · 8.15')
    assert ET.tostring(normalized)==ET.tostring(original),'Change outside new scenery/version tag'
    refs=[i.get('referent') for i in root.iter('Item')];assert len(refs)==len(set(refs))
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    model=ET.Element('roblox',{'version':'4'});model.append(world)
    ET.ElementTree(model).write(WORLD,encoding='utf-8',xml_declaration=True)
    print('PASS exact 8.15 preservation except added side districts and version tag')
    print('Built',OUTPUT)

if __name__=='__main__':main()
