#!/usr/bin/env python3
"""8.21 overlay: industrial expansion; preserve the original imported world/assets."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_820 import main as build_previous,OUTPUT as PREVIOUS
from expansion.content import catalog_source,details_source,economy_source
from expansion.models import source as model_source
from expansion.cargo import source as cargo_source
from expansion import interface
from world.scene import prop
OUTPUT=BASE.parent/'build'/'Matterloom_8_21_Expansion_Industrial.rbxlx'

def patch(name,s):
    if name=='MachineCatalog':
        s=replace_once(s,'function C.hasRecipes(machineType)',catalog_source()+'\nfunction C.hasRecipes(machineType)')
        s=replace_once(s," return rec.machineType=='FusionChamber' or rec.machineType=='ElementSynthesizer'", " local tags=C.types[rec.machineType] and C.types[rec.machineType].inputTags\n return (tags and #tags==2) or rec.machineType=='FusionChamber' or rec.machineType=='ElementSynthesizer'")
        s=replace_once(s,"function C.inputPorts(rec)\n", "function C.inputPorts(rec)\n local tags=C.types[rec.machineType] and C.types[rec.machineType].inputTags\n if tags then\n  local ports={}\n  for _,tag in ipairs(tags)do table.insert(ports,C.port(rec,'input',tag))end\n  return ports\n end\n")
        s=replace_once(s,'return table.freeze(C)',details_source()+'\nreturn table.freeze(C)')
    if name=='Economy':s=replace_once(s,'function E.tier(revenue)',economy_source()+'\nfunction E.tier(revenue)')
    if name=='MachineVisual':
        s=replace_once(s,'function Visual.create(parent,record,origin,preview)',model_source()+'\nfunction Visual.create(parent,record,origin,preview)')
        s=replace_once(s,'        styleProcessor(model,record,data)',"        if data.expansion then styleExpansion(model,record) else styleProcessor(model,record,data) end")
        s=replace_once(s,'local function createCargo(model,name,item)',cargo_source()+'\nlocal function createCargo(model,name,item)')
    if name=='BuildUI':s=interface.ui(s)
    if name=='BuildController':s=interface.controller(s)
    if name=='BuildServer':s=interface.server(s)
    return s

def main():
    if not PREVIOUS.exists():build_previous()
    original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original);changed={}
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        source=item.find("Properties/ProtectedString[@name='Source']")
        if source is not None and not path.startswith('/ServerStorage/'):
            before=source.text or '';source.text=patch(name,before)
            if before!=source.text:changed[item.get('referent')]=path
        for child in item.findall('Item'):visit(child,path)
    for child in root.findall('Item'):visit(child)
    shared=next(i for i in root if i.get('class')=='ReplicatedStorage')
    shared=next(i for i in shared.findall('Item') if i.findtext("Properties/string[@name='Name']")=='Shared')
    module=ET.SubElement(shared,'Item',{'class':'ModuleScript','referent':'RBX_EXPANSION821_DEMO'})
    ET.SubElement(module,'Properties');prop(module,'string','Name','ExpansionDemo')
    prop(module,'ProtectedString','Source',(BASE/'expansion'/'ExpansionDemo.luau').read_text())
    normalized=copy.deepcopy(root);old={i.get('referent'):i for i in original.iter('Item')}
    for parent in normalized.iter():
        for item in list(parent):
            if item.get('referent')=='RBX_EXPANSION821_DEMO':parent.remove(item);continue
            if item.get('referent') in changed:
                index=list(parent).index(item);parent.remove(item);parent.insert(index,copy.deepcopy(old[item.get('referent')]))
    assert ET.tostring(normalized)==ET.tostring(original),'Unexpected world/asset modification'
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('PASS XML preserved outside:',', '.join(changed.values()))
    print('Built',OUTPUT)
if __name__=='__main__':main()
