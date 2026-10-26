"""Contextual controls over the existing horizontal catalog and live thumbnails."""
from build import BASE,replace_once
from build_813 import between

def patch_ui(s):
    s=replace_once(s,"    -- HUD visible even with the construction catalog closed.",
        "    local adapt\n    local activeContext,activeActionCount=false,0\n    -- Compact HUD; factory controls only appear with a target.")
    s=replace_once(s,"UDim2.new(.91,0,0,85),Vector2.new(.5,0),580)","UDim2.new(.91,0,0,64),Vector2.new(.5,0),520)")
    s=replace_once(s,'MATTERLOOM · 8.13 CONSTRUCCIÓN','MATTERLOOM')
    s=replace_once(s,"label(header,'Stage','08.13 / CATÁLOGO HORIZONTAL',10,UDim2.fromOffset(13,32),UDim2.new(1,-26,0,17),colors.muted)",
        "label(header,'Stage','8.14',10,UDim2.fromOffset(13,32),UDim2.new(1,-26,0,17),colors.muted).Visible=false")
    s=s.replace('UDim2.fromOffset(13,57)','UDim2.fromOffset(13,37)').replace('UDim2.new(.43,0,0,57)','UDim2.new(.43,0,0,37)')
    s=replace_once(s,"    -- Actions remain accessible while the catalog is collapsed.",'''    local demoPanel=frame(screen,'Pruebas',UDim2.fromOffset(12,132),UDim2.fromOffset(250,160),Vector2.new(0,0),250)
    demoPanel.Visible=false;demoPanel.ZIndex=22
    label(demoPanel,'Title','PRUEBAS · 8.14',13,UDim2.fromOffset(12,8),UDim2.fromOffset(198,22),colors.cyan).ZIndex=23
    local closeTests=button(demoPanel,'CerrarPruebas','✕',function()
        demoPanel.Visible=false;if adapt then adapt() end
    end)
    closeTests.Position=UDim2.new(1,-35,0,5);closeTests.Size=UDim2.fromOffset(28,28);closeTests.ZIndex=24
    local demoActions=Instance.new('Frame');demoActions.Name='Demos';demoActions.BackgroundTransparency=1
    demoActions.Position=UDim2.fromOffset(12,40);demoActions.Size=UDim2.fromOffset(226,112);demoActions.Parent=demoPanel
    local demoLayout=Instance.new('UIListLayout');demoLayout.Padding=UDim.new(0,5);demoLayout.SortOrder=Enum.SortOrder.LayoutOrder;demoLayout.Parent=demoActions
    local testsButton=button(screen,'AbrirPruebas','Pruebas',function()
        local open=not demoPanel.Visible
        if callbacks.catalog and screen:FindFirstChild('Catalogo').Visible then callbacks.catalog() end
        demoPanel.Visible=open;if adapt then adapt() end
    end)
    testsButton.Size=UDim2.fromOffset(92,32);testsButton.ZIndex=22
    local idleHint=label(screen,'IdleHint','B: construir · clic: seleccionar · arrastra: marcar un área',11,
        UDim2.new(.5,0,1,-12),UDim2.fromOffset(540,34),colors.muted)
    idleHint.AnchorPoint=Vector2.new(.5,1);idleHint.TextWrapped=true;idleHint.TextXAlignment=Enum.TextXAlignment.Center
    idleHint.BackgroundColor3=colors.panel;idleHint.BackgroundTransparency=.25;rounded(idleHint,8)
    -- Contextual actions.
''')
    s=replace_once(s,'actionFrame.Position=UDim2.fromOffset(12,62)','actionFrame.Position=UDim2.fromOffset(12,56)')
    s=replace_once(s,"{'cancel','Limpiar selección'},{'recipe','Receta · G'},{'bulkRemove','Borrar selección'},",
        "{'cancel','Limpiar selección'},{'recipe','Receta · G'},{'filter','Filtro · F'},{'bulkRemove','Borrar selección'},")
    s=replace_once(s,'        actions[item[1]]=b','''        if item[1]=='demo' or item[1]=='productionDemo' or item[1]=='megaDemo' then
            b.Parent=demoActions;b.Size=UDim2.fromOffset(226,32);b.ZIndex=24
        end
        actions[item[1]]=b''')
    s=replace_once(s,'    info.TextTruncate=Enum.TextTruncate.AtEnd','    info.TextTruncate=Enum.TextTruncate.AtEnd\n    info.Visible=false')
    s=replace_once(s,"    local adapt\n    local self=",'    local self=')
    s=replace_once(s,"        catalog.Visible=open",'        catalog.Visible=open\n        if open then demoPanel.Visible=false end')
    s=replace_once(s,"        local placing=mode=='place' or mode=='move'",'''        local placing=mode=='place' or mode=='move'
        activeContext=placing or bulkCount>0
        activeActionCount=0
        testsButton.Visible=not placing
        testsButton.Interactable=not pending and not placing
        testsButton.Active=testsButton.Interactable
        if placing then demoPanel.Visible=false end''')
    s=replace_once(s,'recipe=selectedId~=nil and not placing and not multi,',
        '''recipe=selectedId~=nil and not placing and not multi and Catalog.recipeOrder[kind]~=nil and #Catalog.recipeOrder[kind]>1,
            filter=selectedId~=nil and not placing and not multi and Catalog.isFilter(kind),''')
    s=replace_once(s,'        for key,b in pairs(actions) do\n            b.Interactable=',
        '''        for key,b in pairs(actions) do
            local isDemo=key=='demo' or key=='productionDemo' or key=='megaDemo'
            b.Visible=isDemo or enabled[key]==true
            if not isDemo and b.Visible then activeActionCount+=1 end
            b.Interactable=''')
    s=replace_once(s,"            else string.format('BORRAR (%d)',bulkCount)\n    end",
        "            else string.format('BORRAR (%d)',bulkCount)\n        if adapt then adapt() end\n    end")
    s=replace_once(s,'        status.Text=message','        status.Text=message\n        idleHint.Text=message')
    s=between(s,'    adapt=function()','    local function bindCamera()',
        (BASE/'patches/contextual-layout.luau').read_text()+'\n')
    return s
