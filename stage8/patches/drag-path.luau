    -- A stroke flows from mouse-down toward mouse-up. R only sets isolated pieces.
    local function pathRotations(cells)
        local orders={}
        for i,cell in ipairs(cells) do
            local nextCell=cells[i+1]
            local prevCell=cells[i-1]
            local dx,dz=0,0
            if nextCell then
                dx,dz=nextCell.x-cell.x,nextCell.z-cell.z
            elseif prevCell then
                dx,dz=cell.x-prevCell.x,cell.z-prevCell.z
            end
            local rot=if dx==0 and dz==0 then rotation else flowRotation(dx,dz)
            table.insert(orders,{machineType='Belt',x=cell.x,z=cell.z,rotation=rot,level=buildLevel})
        end
        return orders
    end
