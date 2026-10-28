"""Small tested patches to the existing catalog, filter action and demo entry."""
from pathlib import Path
from build import replace_once
BASE=Path(__file__).parent

def ui(s):
    s=replace_once(s,'PRUEBAS · 8.20','PRUEBAS · 8.21')
    s=replace_once(s,'UDim2.fromOffset(250,160)','UDim2.fromOffset(250,200)')
    s=replace_once(s,'UDim2.fromOffset(226,112)','UDim2.fromOffset(226,150)')
    s=replace_once(s,"{'megaDemo','MEGA DEMO ★'}", "{'megaDemo','MEGA DEMO ★'},{'expansionDemo','Demo: 20 máquinas nuevas'}")
    s=replace_once(s,"or item[1]=='megaDemo' then", "or item[1]=='megaDemo' or item[1]=='expansionDemo' then")
    start=s.index('    local entries={');end=s.index('    local tabButtons={}',start)
    s=s[:start]+'''    local entries={}
    local categoryOrder={'Especial','Transporte','Producción','Metalurgia','Química','Cristales','Electrónica','Componentes','Avanzada','Edificio','Decoración'}
    for _,category in ipairs(categoryOrder)do entries[category]={} end
    for _,typ in ipairs(Catalog.order)do
        local category=Catalog.types[typ].group
        if not entries[category]then entries[category]={};table.insert(categoryOrder,category)end
        table.insert(entries[category],typ)
    end
'''+s[end:]
    s=replace_once(s,"    local self={screen=screen",(BASE/'filter-picker.luau').read_text()+"\n    local self={screen=screen")
    s=replace_once(s,'    function self:setCatalogOpen(open)', '''    function self:toggleFilterPicker()
        if currentType==nil or not Catalog.isFilter(currentType) then return end
        local open=not picker.Visible
        if open and catalog.Visible then
            if callbacks.catalog then callbacks.catalog() else self:setCatalogOpen(false) end
        end
        picker.Visible=open
        search.Text=''
        for item,b in pairs(materialButtons)do
            b.Visible=true;b.BackgroundColor3=if item==(filterSelection or 'Carbon') then Color3.fromRGB(18,103,112) else colors.button
        end
        if picker.Visible then demoPanel.Visible=false end
        if adapt then adapt()end
    end
    function self:closeFilterPicker()picker.Visible=false end
    function self:setCatalogOpen(open)''')
    s=replace_once(s,'        catalog.Visible=open','        picker.Visible=false\n        catalog.Visible=open')
    s=replace_once(s,"        bulkCount=bulkCount or 0", "        bulkCount=bulkCount or 0\n        if filterOwnerId~=selectedId or pending or mode~='select' or bulkCount>1 or not Catalog.isFilter(kind) then picker.Visible=false end\n        filterOwnerId=selectedId")
    s=replace_once(s,'            megaDemo=not placing,','            megaDemo=not placing,\n            expansionDemo=not placing,')
    s=replace_once(s,"key=='megaDemo'", "key=='megaDemo' or key=='expansionDemo'")
    s=replace_once(s,'        local short=viewport.Y<640', "        picker.Size=UDim2.fromOffset(math.min(420,viewport.X-24),math.min(320,viewport.Y-24))\n        local short=viewport.Y<640")
    return s

def controller(s):
    start=s.index('        local index=table.find(Catalog.filterOrder');end=s.index('    actions.recipe=function()',start)
    s=s[:start]+'''        ui:toggleFilterPicker()
    end
    actions.chooseFilter=function(item)
        if pending or mode~='select' or not selectedId or not state or not Catalog.items[item] then return end
        local rec=state.buildings[selectedId]
        if not rec or not Catalog.isFilter(rec.machineType)then return end
        send({kind='configure_filter',id=selectedId,item=item})
    end
'''+s[end:]
    s=replace_once(s,'    actions.megaDemo=function()', '''    actions.expansionDemo=function()
        if pending or placing() then return end
        send({kind='demo_expansion'})
    end
    actions.megaDemo=function()''')
    s=replace_once(s,"or result.code=='demo_mega' then nil", "or result.code=='demo_mega' or result.code=='demo_expansion' then nil")
    s=replace_once(s,"            elseif result.code=='mega_requires_empty'", "            elseif result.code=='demo_expansion' then 'Laboratorio listo: 20 máquinas, suministros para 12 ciclos y créditos de prueba. G cambia recetas.'\n            elseif result.code=='expansion_requires_empty' then 'La demo de expansión necesita una parcela vacía. Tu fábrica se conserva.'\n            elseif result.code=='expansion_blocked' then 'No se pudo crear el laboratorio: '..tostring(result.detail or 'terreno ocupado')\n            elseif result.code=='mega_requires_empty'")
    s=replace_once(s,'    actions.cancel=function()', '    actions.cancel=function()\n        ui:closeFilterPicker()')
    return s

def server(s):
    s=replace_once(s,'local BuildServer = {}',"local ExpansionDemo = require(Shared.ExpansionDemo)\nlocal BuildServer = {}")
    s=replace_once(s,"        if order.kind=='demo' then",'''        if order.kind=='demo_expansion' then
            local staged,seeds,detail=ExpansionDemo.stage(session.state,player.UserId)
            if not staged then
                local reply=packet(session);reply.ok=false;reply.code=seeds;reply.detail=detail
                command:FireClient(player,reply);return
            end
            session.state=staged
            for id,items in pairs(seeds)do
                session.runtime[id]={input={},output=items,last=0,alternate=false,totalMade=0,totalMoved=0,nextRoute=0}
            end
            -- Explicit laboratory action, same availability as existing demos.
            session.cash=math.max(session.cash,60000)
            session.lifetimeRevenue=math.max(session.lifetimeRevenue or 0,60000)
            for id,record in pairs(session.state.buildings)do
                local model=Visual.create(session.machines,record,session.origin,false)
                model:SetAttribute('OwnerUserId',player.UserId);session.models[id]=model
            end
            redrawBelts(session)
            local reply=packet(session);reply.ok=true;reply.code='demo_expansion'
            command:FireClient(player,reply)
            factoryUpdate:FireClient(player,Simulation.report(session));return
        end
        if order.kind=='demo' then''')
    return s
