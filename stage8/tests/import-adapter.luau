-- Rigid transforms about Y, with real translation/rotation composition.
-- Only engine calls are adapted; installBlenderAsset itself is extracted unchanged.
local V={}
V.__index=V
local Vector3={new=function(x,y,z)return setmetatable({X=x,Y=y,Z=z},V)end}
V.__add=function(a,b)return Vector3.new(a.X+b.X,a.Y+b.Y,a.Z+b.Z)end
V.__sub=function(a,b)return Vector3.new(a.X-b.X,a.Y-b.Y,a.Z-b.Z)end
V.__mul=function(a,n)return Vector3.new(a.X*n,a.Y*n,a.Z*n)end
local F={};F.__index=F
local function frame(x,y,z,yaw)return setmetatable({Position=Vector3.new(x,y,z),yaw=yaw or 0},F)end
function F:VectorToWorldSpace(v)
 local c,s=math.cos(self.yaw),math.sin(self.yaw)
 return Vector3.new(c*v.X+s*v.Z,v.Y,-s*v.X+c*v.Z)
end
function F:PointToWorldSpace(v)return self.Position+self:VectorToWorldSpace(v)end
F.__mul=function(a,b)
 local p=a:PointToWorldSpace(b.Position)
 return frame(p.X,p.Y,p.Z,a.yaw+b.yaw)
end
local CFrame={new=function(x,y,z)return frame(x,y,z)end,Angles=function(_,y,_)return frame(0,0,0,y)end,identity=frame(0,0,0)}
local Color3={fromRGB=function(...)return {...}end}
local Construction={CELL_SIZE=4}
local missingKey=nil
local cloned=nil
local assetScale=1
local folder={}
function folder:FindFirstChild(key)
 if key==missingKey then return nil end
 local template={}
 function template:IsA(class)return class=='Model'end
 function template:Clone()
  local model={key=key,pivot=frame(90,15,-30,math.pi),scale=1}
  model.part={IsA=function(_,class)return class=='BasePart'end}
  function model:GetDescendants()return {self.part}end
  function model:PivotTo(cf)self.pivot=cf end
  function model:GetPivot()return self.pivot end
  function model:ScaleTo(scale)self.scale=scale end
  function model:GetBoundingBox()
   -- Fixtures are centered horizontally, bottom at authored pivot, like the XML.
   return self.pivot*CFrame.new(0,3*self.scale,0),Vector3.new(7.9*self.scale,6*self.scale,7.9*self.scale)
  end
  function model:Destroy()self.destroyed=true end
  cloned=model
  return model
 end
 return template
end
local ReplicatedStorage={FindFirstChild=function()return folder end}
local function wrapper(typ,rotation)
 local object={attributes={MachineType=typ},PrimaryPart={CFrame=frame(100,8,200,-rotation*math.pi/2)}}
 function object:GetAttribute(k)return self.attributes[k]end
 function object:SetAttribute(k,v)self.attributes[k]=v end
 return object
end
local function near(a,b)return math.abs(a-b)<1e-4 end
local function vectorMatches(a,b)return near(a.X,b.X) and near(a.Y,b.Y) and near(a.Z,b.Z)end
