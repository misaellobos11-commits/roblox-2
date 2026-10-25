#!/usr/bin/env python3
"""Replace the unverified 8.7 mesh calibration with authoritative port geometry."""
import re
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_86 import main as build_previous, OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_8_Diseno_y_Direcciones.rbxlx'

def patch(name,source):
    if name=='MachineCatalog':
        # Facing +Z, the traveler's left is +X, not -X.
        source=source.replace('dx,dz=fz,-fx','dx,dz=__RIGHT__')
        source=source.replace('dx,dz=-fz,fx','dx,dz=fz,-fx')
        source=source.replace('dx,dz=__RIGHT__','dx,dz=-fz,fx')
    elif name=='BuildServer':
        # Preserve the demo layout by selecting the now-correct family variant.
        # Only literal demo entries change; purchases/player requests are untouched.
        def swap(match):
            return "t='"+match[1]+('Right' if match[2]=='Left' else 'Left')+"'"
        source,count=re.subn(r"t='(Splitter|Overflow|Filter)(Left|Right)'",swap,source)
        assert count==12,count
    elif name=='MachineVisual':
        start=source.index('local function makePorts(')
        end=source.index('local function styleProcessor(',start)
        source=source[:start]+(BASE/'patches/functional-ports.luau').read_text()+'\n'+source[end:]
        source=replace_once(source,'    local key=visualKeys[record.machineType]',
            "    local key=if record.machineType=='Belt' then visualKeys.Belt else nil")
        source=replace_once(source,"local foundation=block(model,'Base',", "local foundation=block(model,'Foundation',")
        source=replace_once(source,'    foundation.TopSurface=Enum.SurfaceType.Smooth',
            '    foundation.TopSurface=Enum.SurfaceType.Smooth\n    foundation.CanCollide=false;foundation.CanTouch=false;foundation.CanQuery=false')
        source=replace_once(source,'    if preview then\n        for _,item in ipairs(model:GetDescendants()) do',
            '''    local bounds,extent=model:GetBoundingBox()
    local height=math.max(1.1,bounds.Position.Y+extent.Y/2)
    local hitbox=block(model,'Base',Vector3.new(width-.14,height,width-.14),Vector3.new(0,height/2,0),dark)
    hitbox.Transparency=1;hitbox.CanCollide=false;hitbox.CanTouch=false;hitbox.CanQuery=not preview
    model:SetAttribute('SelectionHitbox',true)
    if preview then
        for _,item in ipairs(model:GetDescendants()) do''')
        source=replace_once(source,"model:GetAttribute('ImportedVisual')) then",
            "(model:GetAttribute('ImportedVisual') or model:GetAttribute('SelectionHitbox'))) then")
        source=replace_once(source,'Vector3.new(0,4.3,2.24)','Vector3.new(0,4.3,-2.24)')
        source=replace_once(source,'Vector3.new(0,4.60,2.23)','Vector3.new(0,4.60,-2.23)')
        start=source.index("    if machineType=='ElevatorUp' or machineType=='ElevatorDown' then")
        end=source.index('    local incomingX=',start)
        source=source[:start]+(BASE/'patches/elevator-cargo.luau').read_text()+source[end:]
        source=replace_once(source,'    local incomingX=if machineType==\'Belt\'',
            '''    if Catalog.isTransport(machineType) and machineType~='Belt' then
        -- Waiting cargo must not pretend to move toward the front output.
        cube.CFrame=root*CFrame.new(0,1.24,0)
        return
    end
    local incomingX=if machineType=='Belt' ''')
        source=replace_once(source,'return Visual', (BASE/'patches/transfer-cargo.luau').read_text()+'\nreturn Visual')
    elif name=='FactorySimulation':
        source=replace_once(source,'                        table.remove(r.output,1);r.totalMoved+=1',
            '''                        table.remove(r.output,1);r.totalMoved+=1
                        Visual.transferCargo(session.models[rec.id],move.item,route)''')
    elif name=='BuildUI':
        source=replace_once(source,'MATTERLOOM · 8.6 CINTAS','MATTERLOOM · 8.8 DIRECCIONES')
        source=replace_once(source,'08.6 / SENTIDO DE CINTAS Y ARRASTRE','08.8 / DISEÑO Y FLUJO UNIFICADOS')
    return source

def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot()
    changed=[]
    names={'MachineCatalog','MachineVisual','BuildServer','FactorySimulation','BuildUI'}
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if not path.startswith('/ServerStorage/') and name in names:
            prop=item.find("Properties/ProtectedString[@name='Source']")
            assert prop is not None,path
            prop.text=patch(name,prop.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==5,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
