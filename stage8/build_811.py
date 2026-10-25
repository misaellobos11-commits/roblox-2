#!/usr/bin/env python3
"""Fix manual elevator connections and expose the existing height control."""
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_810 import main as build_previous, OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_11_Conexiones_Ascensores.rbxlx'

def patch(name,source):
    if name=='BuildController':
        source=replace_once(source,'function Controller.start(initialPacket)',
            (BASE/'patches/elevator-placement.luau').read_text()+'\nfunction Controller.start(initialPacket)')
        source=replace_once(source,'    local buildLevel=0',
            '    local buildLevel=0\n    local dragStroke=nil\n    local heightOverride,rotationOverride=false,false')
        source=replace_once(source,"    local dragStroke=nil\n    local dragGhost=", "    local dragGhost=")
        source=replace_once(source,'    local function groundAt(position)\n', '''    local function groundAt(position)
        if kind()=='Belt' and state and origin then
            local camera=workspace.CurrentCamera
            if not camera then return end
            local rayInfo=PointerRay.fromScreen(camera,position,GuiService:GetGuiInset())
            local stroking=dragStroke and #dragStroke.cells>0
            local locked=if heightOverride or stroking then buildLevel else nil
            local result=beltPlacement(state,rayInfo.Origin,rayInfo.Direction,origin,buildLevel,rotation,
                if mode=='move' then selectedId else nil,locked,rotationOverride)
            if not result then clearPreview();return end
            candidate={x=result.x,z=result.z}
            buildLevel=result.level
            if not stroking then rotation=result.rotation end
            ui:setHeight(buildLevel)
            previewAt()
            if result.snapped and not stroking then
                ui:setStatus('Acoplado al puerto · '..(if buildLevel==1 then 'CINTA ELEVADA' else 'SUELO')..' · T cambia altura.',true)
            end
            return
        end
''')
        source=replace_once(source,'        chosen=machineType\n        buildLevel=0',
            '''        chosen=machineType
        if not Catalog.isTransport(machineType) or Catalog.isElevator(machineType) then buildLevel=0 end
        heightOverride=false;rotationOverride=false''')
        source=replace_once(source,'        buildLevel=(buildLevel+1)%2',
            '        clearStroke()\n        heightOverride=true\n        buildLevel=(buildLevel+1)%2')
        source=replace_once(source,'        rotation=Construction.rotate(rotation)',
            '        rotation=Construction.rotate(rotation)\n        rotationOverride=true')
        source=replace_once(source,'        buildLevel=record.level or 0',
            '        buildLevel=record.level or 0\n        heightOverride=false;rotationOverride=false')
    elif name=='BuildUI':
        source=replace_once(source,"{'cancel','Cancelar'},{'recipe','Receta · G'},",
            "{'cancel','Cancelar'},{'recipe','Receta · G'},{'height','Altura: suelo · T'},")
        source=replace_once(source,"        info:SetAttribute('BuildLevel',level)",
            "        info:SetAttribute('BuildLevel',level)\n        actions.height.Text=if level==1 then 'Altura: elevada · T' else 'Altura: suelo · T'")
        source=replace_once(source,'local enabled={rotate=placing,confirm=placing,',
            "local enabled={height=placing and Catalog.isTransport(kind) and not Catalog.isElevator(kind),rotate=placing,confirm=placing,")
        source=replace_once(source,'MATTERLOOM · 8.10 AJUSTE','MATTERLOOM · 8.11 ASCENSORES')
        source=replace_once(source,'08.10 / ORIENTACIÓN DE TRES MODELOS','08.11 / CONEXIONES EN DOS ALTURAS')
    return source

def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot();changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('BuildController','BuildUI'):
            prop=item.find("Properties/ProtectedString[@name='Source']");assert prop is not None,path
            prop.text=patch(name,prop.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==2,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
