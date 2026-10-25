#!/usr/bin/env python3
"""Calibrate imported machine artwork on top of the user-verified 8.6 belts."""
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_86 import main as build_previous, OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_7_Orientacion_Maquinas.rbxlx'

def patch(name,source):
    if name=='MachineVisual':
        # A half-turn reverses native side ports too. Use the mirrored member of
        # each artwork family so logical Left/Right retain their existing ports.
        for family in ('Splitter','Overflow','Filter'):
            source=replace_once(source,
                f"{family}Left='{family}_Left_v4',\n    {family}Right='{family}_Right_v4',",
                f"{family}Left='{family}_Right_v4',\n    {family}Right='{family}_Left_v4',")
        source=replace_once(source,'local function assetFolder()',
            (BASE/'patches/import-calibration.luau').read_text()+'\nlocal function assetFolder()')
        source=replace_once(source,'        imported:PivotTo(CFrame.identity)',
            '''        -- Normalize position but retain the calibrated visual axis.
        -- Applying this inside the wrapper leaves ports, cargo and R untouched.
        imported:PivotTo(CFrame.Angles(0,importYaw[key] or 0,0))''')
    elif name=='BuildUI':
        source=replace_once(source,'MATTERLOOM · 8.6 CINTAS','MATTERLOOM · 8.7 MÁQUINAS')
        source=replace_once(source,'08.6 / SENTIDO DE CINTAS Y ARRASTRE','08.7 / ORIENTACIÓN DE MÁQUINAS')
    return source

def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot()
    changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'')
        path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('MachineVisual','BuildUI'):
            prop=item.find("Properties/ProtectedString[@name='Source']")
            assert prop is not None,path
            prop.text=patch(name,prop.text)
            changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==2,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
