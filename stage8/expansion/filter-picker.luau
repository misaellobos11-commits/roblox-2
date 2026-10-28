    -- Direct selection stays usable as the resource catalog grows.
    local filterOwnerId=nil
    local picker=frame(screen,'SelectorMaterial',UDim2.new(.5,0,.5,0),UDim2.fromOffset(420,320),Vector2.new(.5,.5),420)
    picker.Visible=false;picker.ZIndex=30
    label(picker,'Titulo','MATERIAL DEL FILTRO',14,UDim2.fromOffset(12,8),UDim2.new(1,-54,0,25),colors.cyan).ZIndex=31
    local closePicker=button(picker,'Cerrar','✕',function()picker.Visible=false end)
    closePicker.Position=UDim2.new(1,-38,0,5);closePicker.Size=UDim2.fromOffset(30,30);closePicker.ZIndex=32
    local search=Instance.new('TextBox');search.Name='Buscar';search.Text=''
    search.PlaceholderText='Buscar material…';search.ClearTextOnFocus=false
    search.Font=Enum.Font.Gotham;search.TextSize=13;search.TextColor3=colors.text
    search.BackgroundColor3=colors.button;search.BorderSizePixel=0
    search.Position=UDim2.fromOffset(12,40);search.Size=UDim2.new(1,-24,0,32)
    search.ZIndex=31;search.Parent=picker;rounded(search,6)
    local results=Instance.new('ScrollingFrame');results.Name='Materiales';results.BackgroundTransparency=1
    results.BorderSizePixel=0;results.ScrollBarThickness=5
    results.Position=UDim2.fromOffset(12,80);results.Size=UDim2.new(1,-24,1,-92)
    results.AutomaticCanvasSize=Enum.AutomaticSize.Y;results.CanvasSize=UDim2.fromOffset(0,0)
    results.ScrollingDirection=Enum.ScrollingDirection.Y;results.ZIndex=31;results.Parent=picker
    local resultLayout=Instance.new('UIListLayout');resultLayout.Padding=UDim.new(0,4);resultLayout.SortOrder=Enum.SortOrder.LayoutOrder;resultLayout.Parent=results
    local materialButtons={}
    for index,item in ipairs(Catalog.filterOrder)do
        local b=button(results,item,Catalog.items[item].name,function()
            picker.Visible=false
            if callbacks.chooseFilter then callbacks.chooseFilter(item)end
        end)
        b.Size=UDim2.new(1,-8,0,30);b.LayoutOrder=index;b.ZIndex=32
        b.TextSize=12;b.TextColor3=Catalog.items[item].color
        materialButtons[item]=b
    end
    local function normalize(text)
        text=string.lower(text)
        for from,to in pairs({['Á']='a',['É']='e',['Í']='i',['Ó']='o',['Ú']='u',['á']='a',['é']='e',['í']='i',['ó']='o',['ú']='u',['ñ']='n',['Ñ']='n'})do text=string.gsub(text,from,to)end
        return text
    end
    search:GetPropertyChangedSignal('Text'):Connect(function()
        local query=normalize(search.Text)
        for item,b in pairs(materialButtons)do b.Visible=string.find(normalize(Catalog.items[item].name),query,1,true)~=nil end
        results.CanvasPosition=Vector2.zero
    end)
