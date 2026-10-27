local Cycle = require('../environment/DayNight')
local function near(a,b,eps) assert(math.abs(a-b)<(eps or 1e-6),tostring(a)..' vs '..tostring(b)) end
near(Cycle.hour(100,100,1200,16.2),16.2)
near(Cycle.hour(100+1200,100,1200,16.2),16.2)
near(Cycle.hour(100+600,100,1200,16.2),4.2)
near(Cycle.hour(90,100,1200,16.2),16.2)
near(Cycle.hour(500,100,0,16.2),Cycle.hour(500,100,1200,16.2))
near(Cycle.hour(500,100,math.huge,16.2),Cycle.hour(500,100,1200,16.2))
for _,duration in ipairs({60,600,1200,1800}) do
 for _,hour in ipairs({0,5,6.5,8,12,16.2,18,19.5,23.999}) do
  near(Cycle.hour(100+duration*hour/24,100,duration,0),hour)
  near(Cycle.hour(100+duration*(hour/24+100),100,duration,0),hour)
 end
end
local previous=Cycle.sample(23.9999)
for minute=0,24*60 do
 local s=Cycle.sample(minute/60)
 assert(s.brightness>=.65 and s.brightness<=2.8)
 assert(s.night>=0 and s.night<=1)
 assert(math.abs(s.brightness-previous.brightness)<.04,'Sunlight discontinuity')
 assert(math.abs(s.night-previous.night)<.02,'Lamp discontinuity')
 for _,key in ipairs({'ambient','outdoor','atmosphere','tint'}) do
  for c=1,3 do
   assert(s[key][c]>=50 and s[key][c]<=255,'Night visibility floor/color range')
   assert(math.abs(s[key][c]-previous[key][c])<3,'Color discontinuity')
  end
 end
 previous=s
end
assert(Cycle.sample(0).night==1 and Cycle.sample(12).night==0)
print('PASS cycle math: wraparound, duration settings, long sessions, smooth 24-hour palette, night visibility floor')
