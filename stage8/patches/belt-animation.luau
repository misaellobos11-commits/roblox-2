-- Follow the full visible strip, including the same cubic curve as its geometry.
local function animateBelt(model,cube)
    local root=model.PrimaryPart.CFrame
    local entry=model:GetAttribute('CornerFromX') or 0
    local progress=Instance.new('NumberValue')
    progress.Name='Recorrido';progress.Value=0;progress.Parent=cube
    local function update(t)
        local p
        if entry==0 then
            p=Vector3.new(0,1.52,-1.92+3.84*t)
        else
            local u=1-t
            p=Vector3.new(entry*1.92,1.52,0)*(u*u*u)
                +Vector3.new(entry*.77,1.52,0)*(3*u*u*t)
                +Vector3.new(0,1.52,.77)*(3*u*t*t)
                +Vector3.new(0,1.52,1.92)*(t*t*t)
        end
        cube.CFrame=root*CFrame.new(p)
    end
    update(0)
    local changed=progress.Changed:Connect(update)
    local tween=TweenService:Create(progress,TweenInfo.new(.58,Enum.EasingStyle.Linear),{Value=1})
    local destroying
    local function cleanup()
        changed:Disconnect()
        if destroying then destroying:Disconnect() end
        progress:Destroy()
    end
    destroying=cube.Destroying:Connect(function() tween:Cancel();cleanup() end)
    tween.Completed:Connect(function(state)
        if state==Enum.PlaybackState.Completed and cube.Parent then update(1) end
        cleanup()
    end)
    tween:Play()
end
