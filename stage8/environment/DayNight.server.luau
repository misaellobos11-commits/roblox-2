-- One authoritative epoch per server. Clients joining later see the same phase.
local Cycle = require(game:GetService('ReplicatedStorage'):WaitForChild('MatterloomDayNight'))
-- Adjust this attribute in Studio before Play to change the full cycle duration.
if workspace:GetAttribute('DayNightCycleSeconds') == nil then
    workspace:SetAttribute('DayNightCycleSeconds', Cycle.DEFAULT_SECONDS)
end
workspace:SetAttribute('DayNightStartHour', Cycle.START_HOUR)
workspace:SetAttribute('DayNightEpoch', workspace:GetServerTimeNow())
