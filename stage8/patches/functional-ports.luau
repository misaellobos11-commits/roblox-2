-- Generate mouths and chevrons from the same ports used by the server.
-- Build in local coordinates; Visual.pivot applies the player's rotation once.
local function makePorts(model,rec)
    local folder=Instance.new('Folder')
    folder.Name='Puertos';folder.Parent=model
    local localRec={machineType=rec.machineType,x=0,z=0,rotation=0,level=rec.level or 0}
    local half=Catalog.types[rec.machineType].size/2
    local inputs=if rec.machineType=='Receiver' then {} else Catalog.inputPorts(localRec)
    for _,kind in ipairs({'input','output'}) do
        local ports=if kind=='input' then inputs else Catalog.outputs(localRec)
        for _,port in ipairs(ports) do
            local group=Instance.new('Folder')
            group.Name=kind..'_'..port.tag;group.Parent=folder
            local normal=Vector3.new(port.dx,0,port.dz)
            local pos=Vector3.new((port.x-half)*Construction.CELL_SIZE,
                .90+(port.level-localRec.level)*8,(port.z-half)*Construction.CELL_SIZE)
            local color=if kind=='input' then fusionOrange else plasma
            local width=if half==1 then 2.2 else 2.7
            local markerSize=if port.dx~=0 then Vector3.new(.14,.18,width) else Vector3.new(width,.18,.14)
            glow(group,'Boca',markerSize,pos,color)
            local traySize=if port.dx~=0 then Vector3.new(1.05,.18,width+.18) else Vector3.new(width+.18,.18,1.05)
            detail(group,'Bandeja',traySize,pos-normal*.52-Vector3.new(0,.15,0),graphite)
            local direction=normal*(if kind=='input' then -1 else 1)
            local center=pos-normal*.65+Vector3.new(0,.24,0)
            local side=Vector3.new(-direction.Z,0,direction.X)
            local tip=center+direction*.23
            for _,sign in ipairs({-1,1}) do
                local tail=center-direction*.23+side*(sign*.22)
                rod(group,'FlechaPuerto',{tail.X,tail.Y,tail.Z},{tip.X,tip.Y,tip.Z},.13,gold,Enum.Material.Neon)
            end
        end
    end
end

local function styleTransport(model,rec,data,anchor)
    local t=rec.machineType
    detail(model,'Lecho',Vector3.new(3.86,.30,3.86),Vector3.new(0,.40,0),graphite2)
    detail(model,'Banda',Vector3.new(3.55,.18,3.55),Vector3.new(0,.83,0),Color3.fromRGB(22,32,43),Enum.Material.SmoothPlastic)
    -- Corner guards leave every active mouth open.
    for _,x in ipairs({-1.72,1.72}) do for _,z in ipairs({-1.72,1.72}) do
        detail(model,'Protector',Vector3.new(.32,.40,.32),Vector3.new(x,.97,z),silver)
        glow(model,'Tornillo',Vector3.new(.16,.06,.16),Vector3.new(x,1.20,z),goldDark)
    end end
    if t=='Belt' then return end -- Only used if the optional straight mesh is absent.
    if Catalog.isElevator(t) then
        -- The two decks share the belt's exact 8-stud level spacing.
        for _,x in ipairs({-1.65,1.65}) do for _,z in ipairs({-1.52,1.52}) do
            detail(model,'ColumnaAscensor',Vector3.new(.25,8,.25),Vector3.new(x,4.83,z),silver)
        end end
        -- Ring deck leaves the central shaft open for the moving product.
        for _,side in ipairs({-1,1}) do
            detail(model,'CubiertaSuperior',Vector3.new(3.55,.18,.90),Vector3.new(0,8.83,side*1.325),graphite2)
            detail(model,'CubiertaSuperior',Vector3.new(.90,.18,1.75),Vector3.new(side*1.325,8.83,0),graphite2)
        end
        local sign=if t=='ElevatorUp' then 1 else -1
        for _,y in ipairs({2,4,6}) do
            for _,x in ipairs({-1.60,1.60}) do
                -- Vertical chevrons on the two side faces, leaving the shaft open.
                for _,side in ipairs({-1,1}) do
                    rod(model,'FlechaVertical',{x,y-sign*.24,side*.25},{x,y+sign*.24,0},.13,plasma,Enum.Material.Neon)
                end
            end
        end
    else
        local color=if Catalog.isFilter(t) then lime elseif string.find(t,'Overflow') then fusionOrange else gold
        -- Family badge offset from the center so the product remains visible.
        detail(model,'PlacaFamilia',Vector3.new(.55,.16,.55),Vector3.new(1.25,1.04,-1.25),graphite2)
        glow(model,'IndicadorFamilia',Vector3.new(.30,.07,.30),Vector3.new(1.25,1.16,-1.25),color)
    end
    makePorts(model,rec)
    label(anchor,'Etiqueta',data.name:upper(),if Catalog.isElevator(t) then 10.1 else 3.4)
end
