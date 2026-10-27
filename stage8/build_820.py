#!/usr/bin/env python3
"""Give each transported resource a readable silhouette; preserve production/transport."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_819 import main as build_previous,OUTPUT as PREVIOUS
from visuals.cargo_shapes import lua_source
OUTPUT=BASE.parent/'build'/'Matterloom_8_20_Recursos_Transportables.rbxlx'

def name(i):return i.findtext("Properties/string[@name='Name']")
def main():
    build_previous();original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    shared=next(i for i in root if i.get('class')=='ReplicatedStorage')
    shared=next(i for i in shared if name(i)=='Shared')
    visual=next(i for i in shared if name(i)=='MachineVisual')
    source=visual.find("Properties/ProtectedString[@name='Source']")
    s=replace_once(source.text,'local function animateBelt(model,cube)',lua_source()+'\nlocal function animateBelt(model,cube)')
    before="local cube=block(model,'Producto',Vector3.new(1.1,1.05,1.1),Vector3.zero,data.color,Enum.Material.Neon)"
    s=replace_once(s,before,"local cube=createCargo(model,'Producto',item)")
    before="local cube=block(model,'ProductoSalida',Vector3.new(1.1,1.05,1.1),Vector3.zero,data.color,Enum.Material.Neon)"
    s=replace_once(s,before,"local cube=createCargo(model,'ProductoSalida',item)")
    source.text=s
    touched={visual.get('referent')}
    for i in root.iter('Item'):
        source=i.find("Properties/ProtectedString[@name='Source']")
        if source is not None and 'PRUEBAS · 8.19' in (source.text or ''):
            source.text=replace_once(source.text,'PRUEBAS · 8.19','PRUEBAS · 8.20');touched.add(i.get('referent'))
    assert len(touched)==2
    normalized=copy.deepcopy(root);old={i.get('referent'):i for i in original.iter('Item')}
    for parent in normalized.iter():
        for i in list(parent):
            if i.get('referent') in touched:
                index=list(parent).index(i);parent.remove(i);parent.insert(index,copy.deepcopy(old[i.get('referent')]));
    assert ET.tostring(normalized)==ET.tostring(original),'Unexpected change outside cargo visuals/version'
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    folder=OUTPUT.parent/'820-sources';folder.mkdir(exist_ok=True)
    for i in shared:
        source=i.findtext("Properties/ProtectedString[@name='Source']")
        if source:(folder/(name(i)+'.luau')).write_text(source)
    print('PASS only resource visualization and version label changed; geometry, prices, recipes and routing preserved')
    print('Built',OUTPUT)
if __name__=='__main__':main()
