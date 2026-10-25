#!/usr/bin/env python3
"""Apply the belt-only follow-up to the reproducible 8.5 baseline."""
import xml.etree.ElementTree as ET
from build import BASE, OUTPUT as PREVIOUS, build, replace_once

OUTPUT=BASE.parent/'build'/'Matterloom_8_6_Cintas.rbxlx'

def patch(name,source):
    if name=='MachineVisual':
        source=replace_once(source,'local function createBeltBend(',
                            (BASE/'patches/belt-straight.luau').read_text()+'\nlocal function createBeltBend(')
        start=source.index('    -- Si el transporte es una recta,')
        end=source.index("    local old=model:FindFirstChild('RutaCinta')",start)
        source=source[:start]+'''    -- Both paths use the same logical local axes; remove baked GLB arrows.
    if model:GetAttribute('ImportedVisual') then
        local imported=model:FindFirstChild('VisualBlender')
        if imported then imported:Destroy() end
        local bent=model:FindFirstChild('Curva90')
        local straight=model:FindFirstChild('RutaCinta')
        local oldEntry=model:GetAttribute('CornerFromX')
        if entryX==0 then
            if bent then bent:Destroy() end
            if not straight then createBeltStraight(model,root) end
        else
            if straight then straight:Destroy() end
            if oldEntry~=entryX or not bent then createBeltBend(model,root,entryX) end
        end
        model:SetAttribute('IsCorner',entryX~=0)
        model:SetAttribute('CornerFromX',entryX)
        return
    end
'''+source[end:]
    elif name=='BuildController':
        start=source.index('    -- Cuando una hilera se dibuja')
        end=source.index('    local function clearStroke()',start)
        source=source[:start]+(BASE/'patches/drag-path.luau').read_text()+source[end:]
        source=replace_once(source,'Construction.CELL_SIZE,.66,','Construction.CELL_SIZE,.66+buildLevel*8,')
        source=replace_once(source,'local dx,dz=Catalog.direction(record.rotation)\n            local flow=Vector3.new(-dx,0,-dz)',
                            'local dx,dz=Catalog.forward(record.rotation)\n            local flow=Vector3.new(dx,0,dz)')
        source=replace_once(source,'            arrow.Parent=dragGhost','''            arrow.Parent=dragGhost
            -- A shaft alone has no visible direction. Draw two chevron legs.
            local side=Vector3.new(-dz,0,dx)
            local tip=center+flow*.67+Vector3.new(0,.08,0)
            for _,sign in ipairs({-1,1}) do
                local tail=tip-flow*.42+side*(sign*.30)
                local head=arrow:Clone()
                head.Name='PuntaPrevista'
                head.Size=Vector3.new(.16,.10,(tip-tail).Magnitude)
                head.CFrame=CFrame.lookAt((tail+tip)*.5,tip)
                head.Parent=dragGhost
            end''')
        source=replace_once(source,'        rotation=Construction.rotate(rotation)\n        feedbackUntil=0',
                            '''        rotation=Construction.rotate(rotation)
        if dragStroke then
            drawStroke()
            return
        end
        feedbackUntil=0''')
        source=replace_once(source,'        local dx,dz=Catalog.direction(rotation)\n        -- direction() indica el lado de entrada; la salida es el opuesto.\n        local toward=if dz==1 then \'NORTE\' elseif dz==-1 then \'SUR\'\n            elseif dx==1 then \'OESTE\' else \'ESTE\'',
                            '''        local dx,dz=Catalog.forward(rotation)
        local toward=if dz==-1 then 'NORTE' elseif dz==1 then 'SUR'
            elseif dx==-1 then 'OESTE' else 'ESTE' ''')
    elif name=='BuildUI':
        source=replace_once(source,'MATTERLOOM · 8.5 TEST','MATTERLOOM · 8.6 CINTAS')
        source=replace_once(source,'08.3 / DEMOS Y CURVAS ANCHAS','08.6 / SENTIDO DE CINTAS Y ARRASTRE')
        source=replace_once(source,'Mantén clic y arrastra para construir cintas. R gira.',
                            'Arrastra desde la entrada hacia la salida. R orienta una cinta suelta.')
    return source

def main():
    build()
    root=ET.parse(PREVIOUS).getroot()
    changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'')
        path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('MachineVisual','BuildController','BuildUI'):
            prop=item.find("Properties/ProtectedString[@name='Source']")
            assert prop is not None,path
            prop.text=patch(name,prop.text)
            changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==3,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
