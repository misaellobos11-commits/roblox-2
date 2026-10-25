-- Only animate a branch after the server actually accepts that delivery.
function Visual.transferCargo(model,item,route)
    if not model or not model.PrimaryPart then return end
    local typ=model:GetAttribute('MachineType')
    if Catalog.isElevator(typ) then
        -- A new package can have the same material as the one just delivered.
        -- Clear only after a successful transfer so its entry animation restarts.
        local cargo=model:FindFirstChild('Producto')
        if cargo then cargo:Destroy() end
        return
    end
    if not Catalog.isTransport(typ) or typ=='Belt' or Catalog.isElevator(typ) then return end
    local data=Catalog.items[item]
    if not data then return end
    local old=model:FindFirstChild('ProductoSalida')
    if old then old:Destroy() end
    local cube=block(model,'ProductoSalida',Vector3.new(1.1,1.05,1.1),Vector3.zero,data.color,Enum.Material.Neon)
    cube.CanCollide=false;cube.CanTouch=false;cube.CanQuery=false
    local port=Catalog.port({machineType=typ,x=0,z=0,rotation=0,level=0},'output',route)
    local root=model.PrimaryPart.CFrame
    cube.CFrame=root*CFrame.new(0,1.24,0)
    local tween=TweenService:Create(cube,TweenInfo.new(.35,Enum.EasingStyle.Linear),{
        CFrame=root*CFrame.new(port.dx*1.8,1.24,port.dz*1.8)
    })
    tween.Completed:Connect(function() cube:Destroy() end)
    tween:Play()
end
