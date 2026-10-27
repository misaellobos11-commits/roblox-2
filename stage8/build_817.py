#!/usr/bin/env python3
"""Add perimeter bays and an independent synchronized day/night cycle to 8.16."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_816 import main as build_previous,OUTPUT as PREVIOUS
from world.perimeter_817 import generate
from world.scene import prop

OUTPUT=BASE.parent/'build'/'Matterloom_8_17_Perimetro_Dia_Noche.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_817.rbxmx'

def name(i):return i.findtext("Properties/string[@name='Name']")
def main():
    build_previous();original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    world=next(i for i in root.iter('Item') if name(i)=='MatterloomWorld')
    world.append(generate())
    def service(cls):return next(i for i in root if i.get('class')==cls)
    scripts=[
        (service('ReplicatedStorage'),'ModuleScript','MatterloomDayNight','DayNight.luau'),
        (service('ServerScriptService'),'Script','MatterloomDayNightServer','DayNight.server.luau'),
        (next(i for i in service('StarterPlayer') if i.get('class')=='StarterPlayerScripts'),
         'LocalScript','MatterloomDayNightClient','DayNight.client.luau')]
    for parent,cls,title,filename in scripts:
        assert not any(name(i)==title for i in parent.findall('Item'))
        item=ET.SubElement(parent,'Item',{'class':cls,'referent':'RBX_DAYNIGHT817_'+title})
        ET.SubElement(item,'Properties');prop(item,'string','Name',title)
        prop(item,'ProtectedString','Source',(BASE/'environment'/filename).read_text())
    changed=0
    for source in root.findall('.//ProtectedString[@name="Source"]'):
        if source.text and 'PRUEBAS · 8.16' in source.text:
            source.text=replace_once(source.text,'PRUEBAS · 8.16','PRUEBAS · 8.17');changed+=1
    assert changed==1
    normalized=copy.deepcopy(root)
    for parent in normalized.iter('Item'):
        for child in list(parent):
            if child.get('referent','').startswith(('RBX_PERIM817_','RBX_DAYNIGHT817_')):parent.remove(child)
    for source in normalized.findall('.//ProtectedString[@name="Source"]'):
        if source.text:source.text=source.text.replace('PRUEBAS · 8.17','PRUEBAS · 8.16')
    assert ET.tostring(normalized)==ET.tostring(original),'Unexpected change to existing game'
    refs=[i.get('referent') for i in root.iter('Item')];assert len(refs)==len(set(refs))
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    standalone=ET.Element('roblox',{'version':'4'});standalone.append(world)
    ET.ElementTree(standalone).write(WORLD,encoding='utf-8',xml_declaration=True)
    print('PASS existing 8.16 gameplay, HUD, machinery and geometry preserved')
    print('Built',OUTPUT)
if __name__=='__main__':main()
