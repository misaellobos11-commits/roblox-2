    if Catalog.isElevator(machineType) then
        local localRec={machineType=machineType,x=0,z=0,rotation=0,level=0}
        local entryY=1.24+8*Catalog.height(localRec,'input')
        local exitY=1.24+8*Catalog.height(localRec,'output')
        cube.CFrame=root*CFrame.new(0,entryY,-1.8)
        local enter=TweenService:Create(cube,TweenInfo.new(.10,Enum.EasingStyle.Linear),{CFrame=root*CFrame.new(0,entryY,0)})
        enter.Completed:Connect(function()
            if not cube.Parent then return end
            local vertical=TweenService:Create(cube,TweenInfo.new(.26,Enum.EasingStyle.Linear),{CFrame=root*CFrame.new(0,exitY,0)})
            vertical.Completed:Connect(function()
                if cube.Parent then
                    TweenService:Create(cube,TweenInfo.new(.10,Enum.EasingStyle.Linear),{CFrame=root*CFrame.new(0,exitY,1.8)}):Play()
                end
            end)
            vertical:Play()
        end)
        enter:Play()
        return
    end
