#!/usr/bin/env python3
"""Visual-only art pass over 8.21: exact guards preserve every other game system."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_821 import main as build_previous,OUTPUT as PREVIOUS
from expansion.models import source as previous_models
from expansion.polish_822 import source as polished_models
OUTPUT=BASE.parent/'build'/'Matterloom_8_22_Maquinas_Redisenadas.rbxlx'

def name(item):return item.findtext("Properties/string[@name='Name']")
def main():
    if not PREVIOUS.exists():build_previous()
    original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    shared=next(i for i in root if i.get('class')=='ReplicatedStorage')
    shared=next(i for i in shared.findall('Item') if name(i)=='Shared')
    visual=next(i for i in shared.findall('Item') if name(i)=='MachineVisual')
    source=visual.find("Properties/ProtectedString[@name='Source']")
    source.text=replace_once(source.text,previous_models(),polished_models())
    changed={visual.get('referent')}
    for item in root.iter('Item'):
        source=item.find("Properties/ProtectedString[@name='Source']")
        if source is not None and 'PRUEBAS · 8.21' in (source.text or ''):
            source.text=replace_once(source.text,'PRUEBAS · 8.21','PRUEBAS · 8.22');changed.add(item.get('referent'))
    assert len(changed)==2
    old={i.get('referent'):i for i in original.iter('Item')};normalized=copy.deepcopy(root)
    for parent in normalized.iter():
        for item in list(parent):
            if item.get('referent') in changed:
                index=list(parent).index(item);parent.remove(item);parent.insert(index,copy.deepcopy(old[item.get('referent')]))
    assert ET.tostring(normalized)==ET.tostring(original),'Unexpected edit beyond expansion geometry/version'
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('PASS 8.22 visual-only: imported machines, cargo, ports, economy, recipes, HUD behavior, world and simulation preserved')
    print('Built',OUTPUT)
if __name__=='__main__':main()
