    local localGrid={}
    local gridIsVisible=false
    local gridAtLevel=nil
    local function updateBuildGrid()
        if not plot or not origin then return end
        local show=placing() and not catalogOpen
        if show==gridIsVisible and (not show or gridAtLevel==buildLevel) then return end
        if show and #localGrid==0 then
            local folder=plot:FindFirstChild('Grid')
            if not folder then folder=Instance.new('Folder');folder.Name='Grid';folder.Parent=plot end
            local width=Construction.GRID_SIZE*Construction.CELL_SIZE
            for i=0,Construction.GRID_SIZE do
                local c=i*Construction.CELL_SIZE
                for _,axis in ipairs({'X','Z'}) do
                    local line=Instance.new('Part')
                    line.Name='BuildGrid_Local'
                    line.Anchored=true;line.CanCollide=false;line.CanQuery=false;line.CanTouch=false
                    line.CastShadow=false;line.Material=Enum.Material.SmoothPlastic
                    line.Color=Color3.fromRGB(119,128,132)
                    line.Size=if axis=='X' then Vector3.new(.12,.015,width) else Vector3.new(width,.015,.12)
                    line.Parent=folder
                    table.insert(localGrid,{part=line,x=if axis=='X' then c else width/2,
                        z=if axis=='Z' then c else width/2,alpha=if i%4==0 then .66 else .84})
                end
            end
        end
        for _,entry in ipairs(localGrid) do
            entry.part.Position=origin+Vector3.new(entry.x,.035+buildLevel*8,entry.z)
            entry.part.Transparency=if show then entry.alpha else 1
        end
        gridIsVisible=show;gridAtLevel=buildLevel
    end
