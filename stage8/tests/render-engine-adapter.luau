-- Geometry-only Roblox adapter: actual Visual code generates all parts.
-- This does not run Roblox rendering, replication or raycasts.
local Vec={}
Vec.__index=function(v,k)
 if k=='Magnitude' then return math.sqrt(v.X*v.X+v.Y*v.Y+v.Z*v.Z) end
 if k=='Unit' then return v/v.Magnitude end
 return Vec[k]
end
local Vector3={new=function(x,y,z)return setmetatable({X=x,Y=y,Z=z},Vec)end}
Vector3.zero=Vector3.new(0,0,0)
Vec.__add=function(a,b)return Vector3.new(a.X+b.X,a.Y+b.Y,a.Z+b.Z)end
Vec.__sub=function(a,b)return Vector3.new(a.X-b.X,a.Y-b.Y,a.Z-b.Z)end
Vec.__mul=function(a,b)return Vector3.new(a.X*b,a.Y*b,a.Z*b)end
Vec.__div=function(a,b)return a*(1/b)end
function Vec:Dot(b)return self.X*b.X+self.Y*b.Y+self.Z*b.Z end
function Vec:Cross(b)return Vector3.new(self.Y*b.Z-self.Z*b.Y,self.Z*b.X-self.X*b.Z,self.X*b.Y-self.Y*b.X)end
local Frame={};Frame.__index=Frame
local function frame(p,m)return setmetatable({Position=p,m=m or {1,0,0,0,1,0,0,0,1}},Frame)end
local CFrame={}
function CFrame.new(x,y,z)return frame(if type(x)=='table' then x else Vector3.new(x or 0,y or 0,z or 0))end
function Frame:VectorToWorldSpace(v)
 local m=self.m
 return Vector3.new(m[1]*v.X+m[2]*v.Y+m[3]*v.Z,m[4]*v.X+m[5]*v.Y+m[6]*v.Z,m[7]*v.X+m[8]*v.Y+m[9]*v.Z)
end
function Frame:PointToWorldSpace(v)return self.Position+self:VectorToWorldSpace(v)end
function Frame:Inverse()
 local m=self.m
 local inv=frame(Vector3.zero,{m[1],m[4],m[7],m[2],m[5],m[8],m[3],m[6],m[9]})
 inv.Position=inv:VectorToWorldSpace(self.Position*-1)
 return inv
end
function Frame:VectorToObjectSpace(v)return self:Inverse():VectorToWorldSpace(v)end
Frame.__mul=function(a,b)
 local m={}
 for r=0,2 do for c=0,2 do
  local n=0
  for k=0,2 do n+=a.m[r*3+k+1]*b.m[k*3+c+1] end
  m[r*3+c+1]=n
 end end
 return frame(a:PointToWorldSpace(b.Position),m)
end
function CFrame.Angles(x,y,z)
 local cx,sx,cy,sy,cz,sz=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
 return frame(Vector3.zero,{1,0,0,0,cx,-sx,0,sx,cx})*frame(Vector3.zero,{cy,0,sy,0,1,0,-sy,0,cy})*frame(Vector3.zero,{cz,-sz,0,sz,cz,0,0,0,1})
end
function CFrame.lookAt(p,target)
 local f=(target-p).Unit
 local up=if math.abs(f.Y)>.99 then Vector3.new(0,0,1) else Vector3.new(0,1,0)
 local right=f:Cross(up).Unit
 up=right:Cross(f)
 return frame(p,{right.X,up.X,-f.X,right.Y,up.Y,-f.Y,right.Z,up.Z,-f.Z})
end
CFrame.identity=CFrame.new()
local Color3={fromRGB=function(...)return {...}end}
local Enum=setmetatable({},{__index=function(t,k)local v=setmetatable({},{__index=function(_,n)return n end});t[k]=v;return v end})
local UDim={new=function(...)return {...}end}
local UDim2={
 fromOffset=function(x,y)return {X={Scale=0,Offset=x},Y={Scale=0,Offset=y}}end,
 fromScale=function(x,y)return {X={Scale=x,Offset=0},Y={Scale=y,Offset=0}}end,
 new=function(x,ox,y,oy)return {X={Scale=x,Offset=ox},Y={Scale=y,Offset=oy}}end,
}
local TweenInfo={new=function(...)return {...}end}
local Methods={}
local function signal()
 local s={connections={}}
 function s:Connect(fn)
  local c={active=true,fn=fn};function c:Disconnect()self.active=false end
  table.insert(self.connections,c);return c
 end
 function s:Fire(...)
  for _,c in ipairs(self.connections)do if c.active then c.fn(...)end end
 end
 return s
end
local Instance={new=function(class)
 local o={values={ClassName=class,Name=class,CFrame=CFrame.identity,Size=Vector3.new(1,1,1),AbsoluteSize={X=180,Y=120}},children={},attributes={},signals={}}
 return setmetatable(o,{
  __index=function(t,k)
   if table.find({'Changed','Destroying','Activated','MouseEnter','MouseLeave','SelectionGained','SelectionLost'},k)then
    if not t.signals[k]then t.signals[k]=signal()end;return t.signals[k]
   end
   return Methods[k] or t.values[k]
  end,
  __newindex=function(t,k,v)
   if k=='Parent' then
    local old=t.values.Parent
    if old then local i=table.find(old.children,t);if i then table.remove(old.children,i) end end
    if v then table.insert(v.children,t) end
   end
   t.values[k]=v
   if t.signals[k]then t.signals[k]:Fire()end
   if k=='Value' and t.signals.Changed then t.signals.Changed:Fire(v)end
  end,
 })
end}
function Methods:IsA(class)return self.ClassName==class or (class=='BasePart' and self.ClassName=='Part')end
function Methods:GetChildren()return table.clone(self.children)end
function Methods:GetDescendants()
 local result={}
 for _,c in ipairs(self.children) do
  table.insert(result,c)
  for _,d in ipairs(c:GetDescendants()) do table.insert(result,d) end
 end
 return result
end
function Methods:FindFirstChild(name)for _,c in ipairs(self.children)do if c.Name==name then return c end end end
function Methods:FindFirstChildOfClass(class)for _,c in ipairs(self.children)do if c:IsA(class)then return c end end end
function Methods:WaitForChild(name)return assert(self:FindFirstChild(name),'missing child '..name)end
function Methods:GetPropertyChangedSignal(key)
 if not self.signals[key]then self.signals[key]=signal()end;return self.signals[key]
end
function Methods:SetAttribute(k,v)self.attributes[k]=v end
function Methods:GetAttribute(k)return self.attributes[k]end
function Methods:Destroy()self.Destroying:Fire();self.Parent=nil;self.destroyed=true end
function Methods:GetPivot()return if self.PrimaryPart then self.PrimaryPart.CFrame else CFrame.identity end
function Methods:PivotTo(cf)
 local delta=cf*self:GetPivot():Inverse()
 for _,p in ipairs(self:GetDescendants())do if p:IsA('BasePart')then p.CFrame=delta*p.CFrame end end
end
function Methods:GetBoundingBox()
 local lo,hi={math.huge,math.huge,math.huge},{-math.huge,-math.huge,-math.huge}
 for _,p in ipairs(self:GetDescendants())do if p:IsA('BasePart')then
  local m=p.CFrame.m;local c=p.CFrame.Position;local pos={c.X,c.Y,c.Z};local s={p.Size.X,p.Size.Y,p.Size.Z}
  for a=1,3 do
   local e=0;for b=1,3 do e+=math.abs(m[(a-1)*3+b])*s[b]/2 end
   lo[a]=math.min(lo[a],pos[a]-e);hi[a]=math.max(hi[a],pos[a]+e)
  end
 end end
 return CFrame.new((lo[1]+hi[1])/2,(lo[2]+hi[2])/2,(lo[3]+hi[3])/2),Vector3.new(hi[1]-lo[1],hi[2]-lo[2],hi[3]-lo[3])
end
local tweens={}
local TweenService={Create=function(_,object,info,goal)
 local completed={}
 function completed:Connect(fn)self.callback=fn end
 local tween={object=object,goal=goal,Completed=completed}
 function tween:Play()table.insert(tweens,self)end
 function tween:Cancel()self.cancelled=true end
 return tween
end}
local importLookups=0
local ReplicatedStorage={FindFirstChild=function()
 importLookups+=1
 return nil
end}
local game={GetService=function(_,name)return if name=='TweenService' then TweenService else ReplicatedStorage end}
