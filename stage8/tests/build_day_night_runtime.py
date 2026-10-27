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
 local atmosphere,correction,clouds={},{},{}
 function clientWorkspace:FindFirstChildOfClass(name)
  if name=='Terrain' then return {FindFirstChildOfClass=function(_,cls)
   assert(cls=='Clouds');return clouds
  end} end
 end
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
 return {lighting=Lighting,lamp=lamp,world=world,beat=RunService.Heartbeat,atmosphere=atmosphere,correction=correction,clouds=clouds}
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
if '--clear-night' in sys.argv:
    code+='''
-- Revisit a full cycle: fog must not come back after the initial update.
for minute=0,1440 do
 local hour=minute/60
 now=attributes.DayNightEpoch+(hour+24-16.2)*attributes.DayNightCycleSeconds/24
 a.beat:Fire(.05)
 assert(a.atmosphere.Density==0 and a.atmosphere.Haze==0 and a.atmosphere.Glare==0,
        'Runtime cycle restored the atmospheric veil')
 assert(a.lighting.FogStart>=10000 and a.lighting.FogEnd>a.lighting.FogStart,
        'Legacy distance fog is still visible')
 local night=Cycle.sample(hour).night
 assert(a.lamp.Enabled==(night>.01),'Real lamps must illuminate at dusk and switch off by day')
 if night==1 then
  assert(a.lighting.Ambient[1]>=100 and a.lighting.OutdoorAmbient[1]>=125,
         'Unlit factory areas need a stronger ambient floor')
  assert(a.correction.Contrast<=.04,'Night contrast crushes the shadow detail')
 end
end
print('PASS full-day runtime: fog stays off, lamps enabled at night, improved ambient floor and night contrast')
'''
if '--sky' in sys.argv:
    code+='''
for _,hour in ipairs({0,6,12,18,24}) do
 now=attributes.DayNightEpoch+(hour+24-16.2)*attributes.DayNightCycleSeconds/24
 a.beat:Fire(.05)
 assert(a.clouds.Cover>=.43 and a.clouds.Cover<=.59)
 assert(a.clouds.Density>=.55 and a.clouds.Density<=.69)
 assert(a.atmosphere.Density==0 and a.atmosphere.Haze==0)
 if hour%24==0 then
  assert(a.clouds.Color[1]<160,'Night clouds must not remain bright cream')
 elseif hour==12 then assert(a.clouds.Color[1]>230) end
end
print('PASS clouds transition with shared clock while atmosphere stays clear')
'''
output=Path(sys.argv[2]);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(code)
