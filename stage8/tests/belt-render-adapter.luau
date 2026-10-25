-- Only the Roblox rendering boundary is adapted. Geometry builders run unchanged.
local V={}
V.__index=function(v,k)
 if k=='Magnitude' then return math.sqrt(v.X*v.X+v.Y*v.Y+v.Z*v.Z) end
 if k=='Unit' then return v/v.Magnitude end
 return V[k]
end
local Vector3={new=function(x,y,z) return setmetatable({X=x,Y=y,Z=z},V) end}
Vector3.zero=Vector3.new(0,0,0)
V.__add=function(a,b)return Vector3.new(a.X+b.X,a.Y+b.Y,a.Z+b.Z)end
V.__sub=function(a,b)return Vector3.new(a.X-b.X,a.Y-b.Y,a.Z-b.Z)end
V.__mul=function(a,b)return Vector3.new(a.X*b,a.Y*b,a.Z*b)end
V.__div=function(a,b)return a*(1/b)end
local function frame() return setmetatable({}, {__mul=function()return frame()end}) end
local CFrame={new=frame}
local Color3={fromRGB=function(...)return {...}end}
local Enum={Material={Metal=0,SmoothPlastic=1,Neon=2}}
local parts={}
local function object(name)
 local o={Name=name,children={},attributes={}}
 function o:FindFirstChild(n)
  for _,child in ipairs(self.children) do if child.Name==n and not child.dead then return child end end
 end
 function o:GetAttribute(k)return self.attributes[k]end
 function o:SetAttribute(k,v)self.attributes[k]=v end
 function o:Destroy()self.dead=true end
 return setmetatable(o,{__newindex=function(t,k,v)
  rawset(t,k,v)
  if k=='Parent' and v then table.insert(v.children,t) end
 end})
end
local Instance={new=object}
local function block(parent,name,size,pos,color,material)
 local p=object(name);p.Size=size;p.Position=pos;p.Parent=parent
 table.insert(parts,p);return p
end
local segments={}
local function bendStrip(folder,root,name,a,b,width,thickness,color,material)
 table.insert(segments,{name=name,a=a,b=b})
 return block(folder,name,Vector3.zero,Vector3.zero,color,material)
end
local function installBlenderAsset(model,key)
 local mesh=object('VisualBlender');mesh.Parent=model
end
local Visual={}
