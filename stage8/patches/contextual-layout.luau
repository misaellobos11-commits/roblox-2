    adapt=function()
        local camera=workspace.CurrentCamera
        if not camera then return end
        local viewport=screen.AbsoluteSize
        if viewport.X<=0 or viewport.Y<=0 then viewport=camera.ViewportSize end
        local short=viewport.Y<640
        header.Visible=not short
        local top=if short then 12 else 86
        buildButton.Position=UDim2.fromOffset(12,top)
        buildButton.Size=UDim2.fromOffset(152,38)
        testsButton.Position=UDim2.fromOffset(174,top+3)
        demoPanel.Position=UDim2.fromOffset(12,top+46)
        local total=math.min(1460,viewport.X-28)
        local detailWidth=math.min(270,math.floor(total*.30))
        local catalogWidth=total-detailWidth-12
        local left=(viewport.X-total)/2
        local height=math.min(288,viewport.Y-76)
        local bottom=12
        dock.Visible=activeContext and not catalog.Visible and not demoPanel.Visible
        local dockWidth=math.min(620,catalogWidth)
        local columns=if dockWidth<480 then 2 else 4
        layout.CellSize=UDim2.new(1/columns,-6,0,34)
        layout.FillDirectionMaxCells=columns
        local dockHeight=64+math.ceil(activeActionCount/columns)*40
        dock:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(dockWidth,2000)
        dock.AnchorPoint=Vector2.new(0,1)
        dock.Position=UDim2.new(0,left,1,-12)
        dock.Size=UDim2.fromOffset(dockWidth,dockHeight)
        idleHint.Visible=not activeContext and not catalog.Visible and not demoPanel.Visible
        idleHint.Size=UDim2.fromOffset(math.min(540,viewport.X-28),34)
        catalog:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(catalogWidth,2000)
        catalog.AnchorPoint=Vector2.new(0,1)
        catalog.Position=UDim2.new(0,left,1,-bottom)
        catalog.Size=UDim2.fromOffset(catalogWidth,height)
        itemGrid.CellSize=UDim2.fromOffset(math.clamp(math.floor((catalogWidth-64)/6),76,100),math.min(88,math.floor((height-112)/2)))
        detail:FindFirstChildOfClass('UISizeConstraint').MaxSize=Vector2.new(detailWidth,2000)
        detail.AnchorPoint=Vector2.new(0,0)
        local detailTop=viewport.Y-bottom-height
        detail.Position=UDim2.fromOffset(left+catalogWidth+12,detailTop)
        detail.Size=UDim2.fromOffset(detailWidth,height)
        detail.Visible=hoverType~=nil or currentType~=nil or catalog.Visible
    end
