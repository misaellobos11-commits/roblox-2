-- Same local +Z output as curved belts, cargo animation and Catalog.forward.
-- Direction marks are geometry, independent of imported mesh/texture axes.
local function createBeltStraight(model,root)
    local folder=Instance.new('Folder')
    folder.Name='RutaCinta'
    folder.Parent=model
    local graphite=Color3.fromRGB(32,44,55)
    local rubber=Color3.fromRGB(22,32,43)
    local steel=Color3.fromRGB(119,140,153)
    local gold=Color3.fromRGB(212,164,76)
    local yellow=Color3.fromRGB(255,199,67)
    local base=block(folder,'BaseRecta',Vector3.new(3.93,.32,3.93),Vector3.zero,graphite)
    base.CFrame=root.CFrame*CFrame.new(0,.20,0)
    base.CanCollide=false;base.CanTouch=false;base.CanQuery=false
    bendStrip(folder,root,'BandaRecta',Vector3.new(0,.83,-1.92),Vector3.new(0,.83,1.92),3.05,.18,rubber,Enum.Material.SmoothPlastic)
    for _,side in ipairs({-1,1}) do
        bendStrip(folder,root,'RailRecta',Vector3.new(side*1.525,1.03,-1.92),Vector3.new(side*1.525,1.03,1.92),.17,.30,steel)
        bendStrip(folder,root,'BordeDorado',Vector3.new(side*1.455,1.19,-1.92),Vector3.new(side*1.455,1.19,1.92),.085,.045,gold,Enum.Material.SmoothPlastic)
    end
    for _,z in ipairs({-1.20,-.40,.40,1.20}) do
        local tip=Vector3.new(0,1.14,z+.25)
        bendStrip(folder,root,'FlechaRecta',Vector3.new(-.23,1.14,z-.22),tip,.16,.065,yellow,Enum.Material.Neon)
        bendStrip(folder,root,'FlechaRecta',Vector3.new(.23,1.14,z-.22),tip,.16,.065,yellow,Enum.Material.Neon)
    end
    bendStrip(folder,root,'SalidaRecta',Vector3.new(-1.36,1.17,1.80),Vector3.new(1.36,1.17,1.80),.12,.065,Color3.fromRGB(70,220,228),Enum.Material.Neon)
end
