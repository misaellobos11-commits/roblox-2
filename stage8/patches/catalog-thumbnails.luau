local function makeThumbnail(card,machineType)
    local view=Instance.new('ViewportFrame')
    view.Name='Miniatura'
    view.BackgroundTransparency=1
    view.Position=UDim2.fromOffset(5,4)
    view.Size=UDim2.new(1,-10,1,-32)
    view.Active=false
    view.ZIndex=17
    view.Ambient=Color3.fromRGB(185,195,210)
    view.LightColor=Color3.fromRGB(255,245,228)
    view.LightDirection=Vector3.new(-1,-1,-.6)
    view.Parent=card
    local world=Instance.new('WorldModel')
    world.Parent=view
    -- Use the same factory as the placed object; no separate icon asset can drift.
    local model=Visual.create(world,{id=0,machineType=machineType,x=0,z=0,rotation=0,level=0},Vector3.zero,true)
    for _,item in ipairs(model:GetDescendants()) do
        if item:IsA('BillboardGui') then item:Destroy() end
    end
    local bounds,size=model:GetBoundingBox()
    local camera=Instance.new('Camera')
    camera.FieldOfView=35
    camera.Parent=view
    view.CurrentCamera=camera
    local function fit()
        local aspect=math.max(.25,view.AbsoluteSize.X/math.max(1,view.AbsoluteSize.Y))
        local vertical=math.rad(camera.FieldOfView)/2
        local halfAngle=math.min(vertical,math.atan(math.tan(vertical)*aspect))
        local distance=(size.Magnitude/2)/math.sin(halfAngle)*1.12
        camera.CFrame=CFrame.lookAt(bounds.Position+Vector3.new(1,.72,1).Unit*distance,bounds.Position)
    end
    view:GetPropertyChangedSignal('AbsoluteSize'):Connect(fit)
    fit()
    local price=label(card,'Precio','',12,UDim2.new(0,6,1,-25),UDim2.new(1,-12,0,20),colors.text)
    price.TextXAlignment=Enum.TextXAlignment.Center
    price.ZIndex=18
end

local function updateCard(card,typ,report,pending)
    local unlocked=Economy.unlocked(typ,report.lifetimeRevenue or 0)
    local affordable=(report.cash or 0)>=(Economy.price(typ) or 0)
    card.Active=not pending and unlocked and affordable
    card.Interactable=card.Active
    card.Text=''
    card:FindFirstChild('Precio').Text=if unlocked then '$'..tostring(Economy.price(typ) or 0) else 'NIVEL '..tostring(Economy.tiers[typ] or 1)
    card:FindFirstChild('Precio').TextTransparency=if card.Active then 0 else .4
    card:FindFirstChild('Miniatura').ImageColor3=if card.Active then Color3.fromRGB(255,255,255) else Color3.fromRGB(135,145,157)
end

local function layoutDetails(detail)
    detail.AutomaticCanvasSize=Enum.AutomaticSize.Y
    detail.CanvasSize=UDim2.fromOffset(0,0)
    local padding=Instance.new('UIPadding')
    padding.PaddingLeft=UDim.new(0,12)
    padding.PaddingTop=UDim.new(0,12)
    padding.PaddingBottom=UDim.new(0,12)
    padding.Parent=detail
    local layout=Instance.new('UIListLayout')
    layout.SortOrder=Enum.SortOrder.LayoutOrder
    layout.Padding=UDim.new(0,8)
    layout.Parent=detail
    for index,name in ipairs({'DetalleNombre','Descripcion','EncabezadoEntrada','Insumos',
        'EncabezadoSalida','Productos','Ciclo','Notas','Inventario','Conexion'}) do
        local text=detail:FindFirstChild(name)
        text.LayoutOrder=index
        text.TextWrapped=true
        text.TextYAlignment=Enum.TextYAlignment.Top
        text.Size=UDim2.new(1,-24,0,text.TextSize+4)
        text.AutomaticSize=Enum.AutomaticSize.Y
    end
end
