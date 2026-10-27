--!strict
-- Shared clock math and art direction; no frame-rate-dependent accumulated time.
local Cycle = {DEFAULT_SECONDS = 1200, START_HOUR = 16.2}
function Cycle.hour(now: number, epoch: number, seconds: number?, start: number?): number
    local duration = seconds or Cycle.DEFAULT_SECONDS
    if duration ~= duration or duration < 60 or duration == math.huge then duration = Cycle.DEFAULT_SECONDS end
    return ((start or Cycle.START_HOUR) + math.max(0, now - epoch) * 24 / duration) % 24
end
-- hour, sunlight, lamp strength, ambient RGB, outdoor RGB, atmosphere RGB, tint RGB
local keys = {
    {0, .65, 1, {67,79,106}, {88,99,126}, {115,139,176}, {222,233,255}},
    {5, .65, 1, {67,79,106}, {88,99,126}, {115,139,176}, {222,233,255}},
    {6.5, 1.6, .45, {91,77,76}, {130,115,109}, {226,167,130}, {255,234,215}},
    {8, 2.5, 0, {76,76,73}, {124,128,128}, {224,215,195}, {255,249,238}},
    {12, 2.8, 0, {78,78,75}, {132,133,129}, {228,219,201}, {255,250,240}},
    {16.2, 2.5, 0, {64,57,52}, {117,106,93}, {232,200,158}, {255,244,226}},
    {18, 1.8, .35, {84,66,72}, {119,95,100}, {230,162,122}, {255,226,206}},
    {19.5, .65, 1, {67,79,106}, {88,99,126}, {115,139,176}, {222,233,255}},
    {24, .65, 1, {67,79,106}, {88,99,126}, {115,139,176}, {222,233,255}},
}
function Cycle.sample(hour: number)
    hour %= 24
    for index = 1, #keys - 1 do
        local a, b = keys[index], keys[index + 1]
        if hour >= a[1] and hour <= b[1] then
            local t = (hour - a[1]) / (b[1] - a[1])
            t = t * t * (3 - 2 * t)
            local function lerp(x, y) return x + (y - x) * t end
            local function rgb(column)
                return {lerp(a[column][1], b[column][1]), lerp(a[column][2], b[column][2]), lerp(a[column][3], b[column][3])}
            end
            return {brightness = lerp(a[2], b[2]), night = lerp(a[3], b[3]),
                ambient = rgb(4), outdoor = rgb(5), atmosphere = rgb(6), tint = rgb(7)}
        end
    end
    error('Invalid clock hour')
end
return Cycle
