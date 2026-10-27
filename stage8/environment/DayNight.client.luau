-- Render locally from server time: smooth sun movement without per-frame replication.
local Lighting = game:GetService('Lighting')
local RunService = game:GetService('RunService')
local Cycle = require(game:GetService('ReplicatedStorage'):WaitForChild('MatterloomDayNight'))
local world = workspace:WaitForChild('MatterloomWorld')
while workspace:GetAttribute('DayNightEpoch') == nil do
    workspace:GetAttributeChangedSignal('DayNightEpoch'):Wait()
end
local atmosphere = Lighting:FindFirstChildOfClass('Atmosphere')
local correction = Lighting:FindFirstChildOfClass('ColorCorrectionEffect')
local lamps = {}
local function track(item)
    if item:IsA('PointLight') or item:IsA('SurfaceLight') or item:IsA('SpotLight') then
        lamps[item] = item.Brightness
    end
end
for _, item in ipairs(world:GetDescendants()) do track(item) end
world.DescendantAdded:Connect(track)
world.DescendantRemoving:Connect(function(item) lamps[item] = nil end)
local function color(rgb) return Color3.fromRGB(rgb[1], rgb[2], rgb[3]) end
local function update()
    local hour = Cycle.hour(workspace:GetServerTimeNow(), workspace:GetAttribute('DayNightEpoch'),
        workspace:GetAttribute('DayNightCycleSeconds'), workspace:GetAttribute('DayNightStartHour'))
    local look = Cycle.sample(hour)
    Lighting.ClockTime = hour
    Lighting.Brightness = look.brightness
    Lighting.Ambient = color(look.ambient)
    Lighting.OutdoorAmbient = color(look.outdoor)
    Lighting.ColorShift_Top = Color3.fromRGB(33 * (1 - look.night), 19 * (1 - look.night), 8 * (1 - look.night))
    Lighting.ExposureCompensation = .08 * look.night
    if atmosphere then
        atmosphere.Color = color(look.atmosphere)
        atmosphere.Decay = color(look.atmosphere)
        atmosphere.Density = .16 + .025 * look.night
        atmosphere.Glare = .04 * (1 - look.night)
    end
    if correction then correction.TintColor = color(look.tint) end
    for lamp, base in pairs(lamps) do
        lamp.Brightness = base * (.15 + 2.35 * look.night)
    end
end
update()
local elapsed = 0
RunService.Heartbeat:Connect(function(dt)
    elapsed += dt
    if elapsed < .05 then return end
    elapsed %= .05
    update()
end)
