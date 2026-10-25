#!/usr/bin/env python3
"""Correct only the three rear-facing bodies reported in the 8.9 playtest."""
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_89 import main as build_previous, OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_10_Tres_Modelos.rbxlx'

def patch(name,source):
    if name=='MachineVisual':
        source=replace_once(source,'local function assetFolder()', '''-- 8.10: only these three imported bodies face away from their real output.
-- Keep the wrapper, ports, transport artwork and all other meshes unchanged.
local importedYaw={
    MatterReceiver_v1=math.pi,
    ElementSynthesizer_v2=math.pi,
    FusionChamber_v3=math.pi,
}
local function assetFolder()''')
        source=replace_once(source,'        imported:PivotTo(CFrame.identity)',
            '        imported:PivotTo(CFrame.Angles(0,importedYaw[key] or 0,0))')
    elif name=='BuildUI':
        source=replace_once(source,'MATTERLOOM · 8.9 CATÁLOGO','MATTERLOOM · 8.10 AJUSTE')
        source=replace_once(source,'08.9 / OBJETOS Y ANIMACIONES','08.10 / ORIENTACIÓN DE TRES MODELOS')
    return source

def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot();changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('MachineVisual','BuildUI'):
            prop=item.find("Properties/ProtectedString[@name='Source']");assert prop is not None,path
            prop.text=patch(name,prop.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==2,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
