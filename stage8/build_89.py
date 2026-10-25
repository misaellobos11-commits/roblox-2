#!/usr/bin/env python3
"""Restore production artwork, add object thumbnails, improve belt cargo motion."""
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_88 import main as build_previous, OUTPUT as PREVIOUS

OUTPUT=BASE.parent/'build'/'Matterloom_8_9_Catalogo_y_Animaciones.rbxlx'

def patch(name,source):
    if name=='MachineVisual':
        source=replace_once(source,"local key=if record.machineType=='Belt' then visualKeys.Belt else nil",
            "local key=if record.machineType=='Belt' or data.size==2 then visualKeys[record.machineType] else nil")
        source=replace_once(source,'function Visual.setCargo(',
            (BASE/'patches/belt-animation.luau').read_text()+'\nfunction Visual.setCargo(')
        source=replace_once(source,"    local machineType=model:GetAttribute('MachineType')",
            "    local machineType=model:GetAttribute('MachineType')\n    if machineType=='Belt' then animateBelt(model,cube);return end")
        source=replace_once(source,"    if Catalog.isElevator(typ) then\n        -- A new package",
            "    if typ=='Belt' or Catalog.isElevator(typ) then\n        -- A new package")
    elif name=='BuildUI':
        source=replace_once(source,'local function frame(parent,name,pos,sz,anchor,maxWidth)',
            'local function frame(parent,name,pos,sz,anchor,maxWidth,scrollable)')
        source=replace_once(source,"    local f=Instance.new('Frame')",
            "    local f=Instance.new(if scrollable then 'ScrollingFrame' else 'Frame')\n    if scrollable then f.CanvasSize=UDim2.fromOffset(0,376);f.ScrollBarThickness=4 end")
        source=replace_once(source,'Vector2.new(1,0),310)', 'Vector2.new(1,0),310,true)')
        source=replace_once(source,'    local selectedConnection=nil', '    layoutDetails(detail)\n    local selectedConnection=nil')
        source=replace_once(source,"local tabs=Instance.new('Frame')", "local tabs=Instance.new('ScrollingFrame')")
        source=replace_once(source,"    tabs.Name='Categories'", "    tabs.Name='Categories'\n    tabs.BorderSizePixel=0;tabs.ScrollBarThickness=3\n    tabs.AutomaticCanvasSize=Enum.AutomaticSize.X;tabs.CanvasSize=UDim2.fromOffset(0,0)")
        start=source.index("    local tabLayout=Instance.new('UIGridLayout')")
        end=source.index('    tabLayout.Parent=tabs',start)
        source=source[:start]+'''    local tabLayout=Instance.new('UIListLayout')
    tabLayout.FillDirection=Enum.FillDirection.Horizontal
    tabLayout.Padding=UDim.new(0,6)
    tabLayout.SortOrder=Enum.SortOrder.LayoutOrder
'''+source[end:]
        source=replace_once(source,'        b.TextSize=11\n        b.LayoutOrder=index',
            '        b.TextSize=11\n        b.Size=UDim2.fromOffset(92,30)\n        b.LayoutOrder=index')
        source=replace_once(source,'        b.TextSize=11\n        b.LayoutOrder=n',
            '''        b.TextSize=11;b.TextScaled=true;b.TextWrapped=true
        local textLimit=Instance.new('UITextSizeConstraint')
        textLimit.MinTextSize=8;textLimit.MaxTextSize=11;textLimit.Parent=b
        b.LayoutOrder=n''')
        source=replace_once(source,'local UI={}',
            "local Visual=require(game:GetService('ReplicatedStorage').Shared.MachineVisual)\nlocal UI={}")
        source=replace_once(source,'function UI.new(callbacks)',
            (BASE/'patches/catalog-thumbnails.luau').read_text()+'\nfunction UI.new(callbacks)')
        source=replace_once(source,'local economyReport={cash=Economy.startCash,lifetimeRevenue=0,techTier=1}',
            'local economyReport={cash=Economy.startCash,lifetimeRevenue=0,techTier=1}\n    local catalogPending=false')
        source=replace_once(source,"local b=button(items,kind,data.name..'  ·  $'..(Economy.price(kind) or 0),function()",
            "local b=button(items,kind,'',function()")
        source=replace_once(source,'        machineButtons[kind]=b',
            '        makeThumbnail(b,kind)\n        machineButtons[kind]=b')
        source=replace_once(source,'    local self={screen=screen,actions=actions,machineButtons=machineButtons,catalog=catalog}',
            '    local adapt\n    local self={screen=screen,actions=actions,machineButtons=machineButtons,catalog=catalog}')
        source=replace_once(source,'        catalog.Visible=open','        catalog.Visible=open\n        if adapt then adapt() end')
        source=replace_once(source,'    local function adapt()', '    adapt=function()')
        source=replace_once(source,'        b.MouseLeave:Connect(function() hoverType=nil;renderDetail() end)',
            '''        b.MouseLeave:Connect(function() hoverType=nil;renderDetail() end)
        b.SelectionGained:Connect(function() hoverType=kind;renderDetail() end)
        b.SelectionLost:Connect(function() hoverType=nil;renderDetail() end)''')
        source=replace_once(source,'        bulkCount=bulkCount or 0\n        local placing=',
            '        bulkCount=bulkCount or 0\n        catalogPending=pending==true\n        local placing=')
        start=source.index('            local unlocked=Economy.unlocked(typ,economyReport.')
        end=source.index('            b.BackgroundColor3=',start)
        source=source[:start]+'            updateCard(b,typ,economyReport,catalogPending)\n'+source[end:]
        start=source.index('            local unlocked=Economy.unlocked(typ,report.')
        end=source.index('\n        end',start)
        source=source[:start]+'            updateCard(b,typ,report,catalogPending)'+source[end:]
        start=source.index("        dock:FindFirstChildOfClass('UISizeConstraint').MaxSize=")
        end=source.index('\n    end\n    local function bindCamera()',start)
        source=source[:start]+'''        -- Keep the object grid and its description side by side, without overlap.
        local total=math.min(1080,camera.ViewportSize.X-28)
        local detailWidth=math.min(302,math.floor(total*.34))
        local catalogWidth=total-detailWidth-12
        local left=(camera.ViewportSize.X-total)/2
        local height=math.clamp(camera.ViewportSize.Y-370,160,330)
        local bottom=266
        if short and catalog.Visible then bottom=12;height=math.max(160,camera.ViewportSize.Y-76) end
        dock.Visible=not (short and catalog.Visible)
        dock:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(catalogWidth,2000)
        dock.Size=UDim2.fromOffset(catalogWidth,250)
        dock.Position=UDim2.new(0,left+catalogWidth/2,1,-8)
        catalog:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(catalogWidth,2000)
        catalog.AnchorPoint=Vector2.new(0,1)
        catalog.Position=UDim2.new(0,left,1,-bottom)
        catalog.Size=UDim2.fromOffset(catalogWidth,height)
        itemGrid.CellSize=if catalogWidth<500 then UDim2.new(.5,-6,0,118) else UDim2.new(.333,-8,0,132)
        detail:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(detailWidth,2000)
        detail.AnchorPoint=Vector2.new(0,0)
        local detailTop=if short and not catalog.Visible then 16 else camera.ViewportSize.Y-bottom-height
        detail.Position=UDim2.fromOffset(left+catalogWidth+12,detailTop)
        detail.Size=UDim2.fromOffset(detailWidth,math.min(376,camera.ViewportSize.Y-detailTop-12))
        detail.Visible=hoverType~=nil or currentType~=nil or catalog.Visible'''+source[end:]
        start=source.index('    adapt=function()')
        end=source.index('    local function bindCamera()',start)
        adapt=source[start:end].replace('camera.ViewportSize','viewport')
        adapt=adapt.replace('        if not camera then return end',
            '        if not camera then return end\n        local viewport=screen.AbsoluteSize\n        if viewport.X<=0 or viewport.Y<=0 then viewport=camera.ViewportSize end')
        source=source[:start]+adapt+source[end:]
        source=replace_once(source,"    workspace:GetPropertyChangedSignal('CurrentCamera'):Connect(bindCamera)",
            "    screen:GetPropertyChangedSignal('AbsoluteSize'):Connect(adapt)\n    workspace:GetPropertyChangedSignal('CurrentCamera'):Connect(bindCamera)")
        source=replace_once(source,'MATTERLOOM · 8.8 DIRECCIONES','MATTERLOOM · 8.9 CATÁLOGO')
        source=replace_once(source,'08.8 / DISEÑO Y FLUJO UNIFICADOS','08.9 / OBJETOS Y ANIMACIONES')
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
