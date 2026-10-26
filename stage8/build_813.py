#!/usr/bin/env python3
"""Default multi-selection and a compact horizontal construction catalog."""
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_812 import main as build_previous,OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_13_Catalogo_Horizontal.rbxlx'

def between(source,start,end,replacement):
    a=source.index(start);b=source.index(end,a)
    return source[:a]+replacement+source[b:]

def patch(name,s):
    if name=='BuildController':
        s=replace_once(s,'local function beltPlacement(state,rayOrigin,rayDirection,origin,level,rotation,ignoreId,lockedLevel,rotationLocked)',
            '''local function beltPlacement(state,rayOrigin,rayDirection,origin,level,rotation,ignoreId,lockedLevel,rotationLocked,machineType)
    machineType=machineType or 'Belt' ''')
        s=replace_once(s,"local belt={id=0,machineType='Belt',x=x,z=z,rotation=r,level=port.level}",
                         'local belt={id=0,machineType=machineType,x=x,z=z,rotation=r,level=port.level}')
        s=replace_once(s,"Construction.canPlace(state,'Belt',x,z,r,ignoreId,port.level)",
                         'Construction.canPlace(state,machineType,x,z,r,ignoreId,port.level)')
        s=replace_once(s,"if kind()=='Belt' and state and origin then",
                         'if Catalog.isTransport(kind()) and not Catalog.isElevator(kind()) and state and origin then')
        s=replace_once(s,"if mode=='move' then selectedId else nil,locked,rotationOverride)",
                         "if mode=='move' then selectedId else nil,locked,rotationOverride,kind())")
        s=replace_once(s,"then 'CINTA ELEVADA' else 'SUELO'", "then 'NIVEL ELEVADO' else 'SUELO'")
        s=between(s,'    actions.height=function()','    actions.filter=function()','')
        s=between(s,'    actions.bulk=function()','    actions.bulkRemove=function()','')
        s=s.replace("        elseif input.KeyCode==Enum.KeyCode.T then actions.height()\n",'')
        s=s.replace("        elseif input.KeyCode==Enum.KeyCode.V then actions.bulk()\n",'')
        s=replace_once(s,'local heightOverride,rotationOverride=false,false','local rotationOverride=false')
        s=s.replace('heightOverride=false;rotationOverride=false','rotationOverride=false')
        s=replace_once(s,'if heightOverride or stroking then buildLevel else nil','if stroking then buildLevel else nil')
        s=replace_once(s,"..' · T cambia altura.'","..' · altura automática.'")
        s=replace_once(s,'    -- The explicit height button can select the occluded lower plane.',
                         '    -- Move the camera to expose a lower port hidden by the upper one.')
        # Default select mode now always supports toggling and area selection.
        s=replace_once(s,"if pending or not selectedId or placing() or mode=='bulk' then return end",
                         "if pending or not selectedId or placing() or bulkCount()>1 then return end")
        s=s.replace("if pending or placing() or mode=='bulk' then return end",'if pending or placing() then return end')
        s=replace_once(s,"if mode~='bulk' and selectedId and state and plot then","if selectedId and state and plot then")
        s=s.replace("mode=='bulk'","mode=='select'").replace("mode~='bulk'","mode~='select'")
        s=replace_once(s,"if mode~='select' or not state or not plot then return end", "if mode~='select' or not state or not plot or bulkCount()<2 then return end")
        s=replace_once(s,'    local function refresh()\n        local count=bulkCount()',
            '''    local function refresh()
        -- A sole member remains available to move/configure; groups have no single target.
        if mode=='select' then
            selectedId=nil
            for id in pairs(selectedBulk) do
                if not state or not state.buildings[id] then selectedBulk[id]=nil end
            end
            if bulkCount()==1 then selectedId=next(selectedBulk) end
        end
        local count=bulkCount()''')
        s=replace_once(s,"                selectedBulk[id]=if selectedBulk[id] then nil else true\n                confirmDelete=false\n                refresh()\n                feedback(string.format('%d estructuras marcadas. Arrastra para seleccionar un área.',bulkCount()),true)\n            end",
            """                selectedBulk[id]=if selectedBulk[id] then nil else true
            else
                selectedBulk={}
            end
            confirmDelete=false
            refresh()
            feedback(string.format('%d estructuras marcadas. Arrastra para seleccionar un área.',bulkCount()),true)""")
        s=replace_once(s,"                selectedId=if result.code=='removed' or result.code=='removed_many' or result.code=='demo' or result.code=='demo_production' or result.code=='demo_mega' then nil else result.id",
            """                selectedId=if result.code=='removed' or result.code=='removed_many' or result.code=='demo' or result.code=='demo_production' or result.code=='demo_mega' then nil else result.id
                if selectedId and state and state.buildings[selectedId] then selectedBulk[selectedId]=true end""")
        s=replace_once(s,"feedback('Acción cancelada.',nil)","feedback('Clic para marcar o desmarcar; arrastra para seleccionar un área.',nil)")
    elif name=='BuildUI':
        s=replace_once(s,"{'remove','Retirar 1'},{'bulk','Elegir varios · V'},{'bulkRemove','Borrar grupo'},\n        {'cancel','Cancelar'},{'recipe','Receta · G'},{'height','Altura: suelo · T'},",
                         "{'cancel','Limpiar selección'},{'recipe','Receta · G'},{'bulkRemove','Borrar selección'},")
        s=replace_once(s,"        actions.height.Text=if level==1 then 'Altura: elevada · T' else 'Altura: suelo · T'\n",'')
        s=replace_once(s,"        actions.bulk.Text=if multi then 'Salir de selección' else 'Elegir varios · V'\n",'')
        s=replace_once(s,"local multi=mode=='bulk'","local multi=bulkCount>1")
        s=replace_once(s,'local enabled={height=placing and Catalog.isTransport(kind) and not Catalog.isElevator(kind),rotate=placing,confirm=placing,',
                         'local enabled={rotate=placing,confirm=placing,')
        s=replace_once(s,'bulk=not placing,bulkRemove=multi and bulkCount>0,','bulkRemove=not placing and bulkCount>0,')
        s=s.replace('productionDemo=not placing and not multi','productionDemo=not placing').replace('megaDemo=not placing and not multi','megaDemo=not placing').replace('demo=not placing and not multi','demo=not placing')
        s=replace_once(s,"elseif mode=='bulk' then string.format('SELECCIÓN MÚLTIPLE · %d marcadas',bulkCount)",
                         "elseif bulkCount>1 then string.format('SELECCIÓN · %d marcadas',bulkCount)")
        s=replace_once(s,"else 'Elige una máquina en CONSTRUIR o selecciona una del terreno.'", "else 'Clic para marcar · arrastra para seleccionar varias · CONSTRUIR para añadir.'")
        s=replace_once(s,"if mode=='bulk' then\n            info.Text", "if (bulkCount or 0)>1 then\n            info.Text")
        s=replace_once(s,"        actions.confirm.Text=", "        actions.cancel.Text=if placing then 'Cancelar' else 'Limpiar selección'\n        actions.confirm.Text=")
        s=replace_once(s,"items.AutomaticCanvasSize=Enum.AutomaticSize.Y", "items.AutomaticCanvasSize=Enum.AutomaticSize.X\n    items.ScrollingDirection=Enum.ScrollingDirection.X")
        s=replace_once(s,"    itemGrid.SortOrder=Enum.SortOrder.LayoutOrder", "    itemGrid.SortOrder=Enum.SortOrder.LayoutOrder\n    itemGrid.FillDirection=Enum.FillDirection.Vertical\n    itemGrid.FillDirectionMaxCells=2")
        s=replace_once(s,'    local total=math.min(1080,viewport.X-28)','    local total=math.min(1460,viewport.X-28)')
        s=replace_once(s,'    local detailWidth=math.min(302,math.floor(total*.34))','    local detailWidth=math.min(270,math.floor(total*.30))')
        s=replace_once(s,'    local height=math.clamp(viewport.Y-370,160,330)','    local height=288')
        s=replace_once(s,'    local bottom=266','    local bottom=226')
        s=replace_once(s,'if short and catalog.Visible then bottom=12;height=math.max(160,viewport.Y-76) end',
                         'if short and catalog.Visible then bottom=12;height=math.min(288,viewport.Y-76) end')
        s=replace_once(s,'dock.Size=UDim2.fromOffset(catalogWidth,250)','dock.Size=UDim2.fromOffset(catalogWidth,210)')
        s=replace_once(s,'actionFrame.Size=UDim2.new(1,-24,0,155)','actionFrame.Size=UDim2.new(1,-24,0,114)')
        s=replace_once(s,'UDim2.fromOffset(12,227)','UDim2.fromOffset(12,187)')
        s=replace_once(s,"        itemGrid.CellSize=if catalogWidth<500 then UDim2.new(.5,-6,0,118) else UDim2.new(.333,-8,0,132)",
            """        local cardWidth=math.clamp(math.floor((catalogWidth-24-5*8)/6),76,100)
        local cardHeight=math.min(88,math.floor((height-112)/2))
        itemGrid.CellSize=UDim2.fromOffset(cardWidth,cardHeight)""")
        s=replace_once(s,'MATTERLOOM · 8.12 CAÑÓN','MATTERLOOM · 8.13 CONSTRUCCIÓN')
        s=replace_once(s,'08.12 / COMPLEJO DEL CAÑÓN','08.13 / CATÁLOGO HORIZONTAL')
    return s

def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot();changed=[]
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if not path.startswith('/ServerStorage/') and name in ('BuildController','BuildUI'):
            prop=item.find("Properties/ProtectedString[@name='Source']");assert prop is not None
            prop.text=patch(name,prop.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert len(changed)==2,changed
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
