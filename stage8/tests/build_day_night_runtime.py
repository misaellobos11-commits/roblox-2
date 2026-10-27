"""Exercise shipped scripts with deterministic Roblox service adapters (not an engine render)."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
root=ET.parse(sys.argv[1]).getroot()
def source(name):
    return next(i.findtext("Properties/ProtectedString[@name='Source']") for i in root.iter('Item')
                if i.findtext("Properties/string[@name='Name']")==name)
module=source('MatterloomDayNight');server=source('MatterloomDayNightServer');client=source('MatterloomDayNightClient')
code='local Cycle=(function()\n'+module+'\nend)()\n'+'''
local now=1000
local attributes={}
local workspace={}
function workspace:GetAttribute(k) return attributes[k] end
function workspace:SetAttribute(k,v) attributes[k]=v end
function workspace:GetServerTimeNow() return now end
local function signal()
 local handlers={}
 return {Connect=function(_,fn) table.insert(handlers,fn) end,
         Fire=function(_,...) for _,fn in ipairs(handlers) do fn(...) end end}
end
local ReplicatedStorage={WaitForChild=function(_,name) assert(name=='MatterloomDayNight');return name end}
local require=function(name) assert(name=='MatterloomDayNight');return Cycle end
local function bootServer()
 local game={GetService=function(_,name) assert(name=='ReplicatedStorage');return ReplicatedStorage end}
'''+server+'''
end
bootServer()
assert(attributes.DayNightEpoch==1000 and attributes.DayNightCycleSeconds==1200)
local function startClient()
 local lamp={Brightness=.5}
 function lamp:IsA(class) return class=='PointLight' end
 local world={DescendantAdded=signal(),DescendantRemoving=signal()}
 function world:GetDescendants() return {lamp} end
 local clientWorkspace=setmetatable({}, {__index=workspace})
 function clientWorkspace:WaitForChild(name) assert(name=='MatterloomWorld');return world end
 local workspace=clientWorkspace
 local atmosphere,correction={},{}
 local Lighting={}
 function Lighting:FindFirstChildOfClass(name)
  if name=='Atmosphere' then return atmosphere end
  if name=='ColorCorrectionEffect' then return correction end
 end
 local RunService={Heartbeat=signal()}
 local Color3={fromRGB=function(...) return {...} end}
 local game={GetService=function(_,name)
  return ({Lighting=Lighting,RunService=RunService,ReplicatedStorage=ReplicatedStorage})[name]
 end}
'''+client+'''
 return {lighting=Lighting,lamp=lamp,world=world,beat=RunService.Heartbeat,atmosphere=atmosphere}
end
local function near(a,b) assert(math.abs(a-b)<1e-6,tostring(a)..' vs '..tostring(b)) end
local a=startClient()
near(a.lighting.ClockTime,16.2)
now=1170
a.beat:Fire(170)
local b=startClient()
near(a.lighting.ClockTime,b.lighting.ClockTime)
near(a.lamp.Brightness,b.lamp.Brightness)
-- Midnight, noon and next cycle; a stalled client catches up instead of drifting.
for _,hour in ipairs({24,36,40.2,48}) do
 now=1000+(hour-16.2)*1200/24
 a.beat:Fire(30);b.beat:Fire(.05)
 near(a.lighting.ClockTime,hour%24);near(b.lighting.ClockTime,hour%24)
 near(a.lamp.Brightness,b.lamp.Brightness)
 if hour%24==0 then
  near(a.lamp.Brightness,1.25)
  assert(a.lighting.OutdoorAmbient[1]>=80)
 elseif hour%24==12 then near(a.lamp.Brightness,.075) end
end
local streamed={Brightness=.65,IsA=a.lamp.IsA}
a.world.DescendantAdded:Fire(streamed);a.beat:Fire(.05)
near(streamed.Brightness,.65*2.5)
a.world.DescendantRemoving:Fire(streamed)
now+=600;a.beat:Fire(.05)
near(streamed.Brightness,.65*2.5) -- detached light must no longer be updated
near(a.lamp.Brightness,.075)
attributes.DayNightCycleSeconds=600
now=1000+600
a.beat:Fire(.05);b.beat:Fire(.05)
near(a.lighting.ClockTime,16.2);near(a.lighting.ClockTime,b.lighting.ClockTime)
attributes.DayNightCycleSeconds=1800
bootServer()
assert(attributes.DayNightCycleSeconds==1800,'Configured duration must survive initialization')
print('PASS shipped server/client: common epoch, late join, midnight/noon, stalled frames, streamed lights, custom duration (service adapters)')
'''
output=Path(sys.argv[2]);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(code)
