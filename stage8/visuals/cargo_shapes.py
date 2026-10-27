"""Small original resource silhouettes. All coordinates are relative to the belt deck."""
import json

def piece(name,size,pos,color,material='Metal',kind='Part',shape='Block',rot=(0,0,0)):
    return dict(name=name,size=size,pos=pos,color=color,material=material,kind=kind,shape=shape,rot=rot)

def chunk(name,size,pos,color,rot):
    return piece(name,size,pos,color,'Slate','Part','Ball',rot=rot)

SHAPES={
'RawMatter':[
    chunk('Matriz',(.92,.58,.72),(0,.30,0),(146,168,178),(0,25,0)),
    chunk('Fragmento',(.56,.72,.52),(-.27,.37,.12),(190,204,203),(0,-35,0)),
    chunk('Inclusión',(.52,.44,.48),(.38,.23,-.12),(112,135,148),(0,110,0))],
'Carbon':[
    chunk('CarbonGrande',(.82,.62,.72),(-.16,.32,0),(64,72,83),(0,28,0)),
    chunk('CarbonPequeno',(.62,.43,.58),(.33,.23,.1),(91,99,108),(0,-50,0)),
    chunk('Arista',(.42,.38,.36),(-.31,.57,.05),(114,121,128),(0,105,0))],
'Oxygen':[
    piece('Deposito',(.72,.58,.58),(0,.43,0),(103,187,215),'Metal',shape='Cylinder',rot=(0,0,90)),
    piece('Banda',(.17,.62,.62),(0,.35,0),(216,226,226),'Metal',shape='Cylinder',rot=(0,0,90)),
    piece('Cuello',(.14,.24,.24),(0,.86,0),(105,117,126),'Metal',shape='Cylinder',rot=(0,0,90)),
    piece('Valvula',(.38,.08,.12),(0,.97,0),(231,207,120))],
'Hydrogen':[
    piece('Soporte',(.92,.12,.59),(0,.06,0),(86,102,115)),
    piece('BotellaA',(.70,.34,.34),(-.23,.47,0),(217,227,236),shape='Cylinder',rot=(0,0,90)),
    piece('BotellaB',(.70,.34,.34),(.23,.47,0),(217,227,236),shape='Cylinder',rot=(0,0,90)),
    piece('CierreA',(.12,.24,.24),(-.23,.87,0),(203,169,76),shape='Cylinder',rot=(0,0,90)),
    piece('CierreB',(.12,.24,.24),(.23,.87,0),(203,169,76),shape='Cylinder',rot=(0,0,90)),
    piece('Abrazadera',(.96,.12,.42),(0,.40,0),(105,126,142))],
'Silicon':[
    piece('ObleaInferior',(.9,.14,.9),(0,.07,0),(93,104,139),rot=(0,25,0)),
    piece('ObleaMedia',(.9,.14,.9),(0,.24,0),(134,147,183),rot=(0,25,0)),
    piece('ObleaSuperior',(.9,.14,.9),(0,.41,0),(170,180,211),rot=(0,25,0)),
    piece('Pista',(.65,.025,.06),(0,.493,0),(215,221,234),rot=(0,25,0))],
'Iron':[
    piece('NucleoHierro',(.64,.46,.71),(0,.23,0),(119,134,150)),
    chunk('HierroIzq',(.42,.50,.67),(-.39,.25,0),(145,157,169),(0,90,0)),
    chunk('Oxido',(.45,.40,.55),(.36,.20,0),(137,102,79),(0,-90,0))],
'Copper':[
    piece('BarraA',(1.1,.23,.23),(0,.14,-.18),(195,113,68),shape='Cylinder'),
    piece('BarraB',(1.1,.23,.23),(0,.14,.18),(225,149,92),shape='Cylinder'),
    piece('BarraC',(1.1,.23,.23),(0,.34,0),(236,166,108),shape='Cylinder'),
    piece('Fleje',(.13,.39,.58),(0,.24,0),(113,98,86))],
'CarbonCompound':[
    piece('BloqueCompuesto',(1.1,.49,.75),(0,.245,0),(75,87,103),'Slate'),
    piece('BandaClara',(.2,.51,.77),(-.27,.255,0),(189,186,157)),
    piece('BandaClara2',(.2,.51,.77),(.27,.255,0),(189,186,157))],
'Silicate':[
    chunk('Laja',(.95,.27,.80),(0,.14,0),(168,145,109),(0,15,0)),
    chunk('Cuarzo',(.56,.69,.53),(-.17,.36,.04),(220,203,168),(0,-18,0)),
    chunk('CuarzoSecundario',(.45,.44,.46),(.30,.23,-.1),(195,176,140),(0,75,0))],
'BaseMetal':[
    piece('Aleacion',(1.05,.37,.70),(0,.185,0),(141,145,162)),
    piece('PlacaAleada',(.80,.13,.55),(-.06,.435,0),(190,179,160)),
    piece('Union',(.17,.52,.73),(.21,.26,0),(104,118,134))],
'ConductiveMix':[
    piece('Bobina',(.68,.64,.64),(0,.39,0),(222,142,76),shape='Cylinder'),
    piece('DiscoIzq',(.12,.82,.82),(-.40,.42,0),(88,105,120),shape='Cylinder'),
    piece('DiscoDer',(.12,.82,.82),(.40,.42,0),(88,105,120),shape='Cylinder'),
    piece('Eje',(.96,.19,.19),(0,.42,0),(205,214,219),shape='Cylinder'),
    piece('VueltaCentral',(.06,.67,.67),(0,.39,0),(178,98,54),shape='Cylinder')],
'BasicCrystal':[],
'SyntheticOre':[
    chunk('RocaSintetica',(.95,.65,.82),(0,.33,0),(107,127,147),(0,20,0)),
    chunk('CaraMetalica',(.55,.78,.55),(-.23,.40,0),(153,173,191),(0,-40,0)),
    piece('Veta',(.09,.49,.10),(.22,.39,.26),(104,206,208),'SmoothPlastic',rot=(0,0,-24)),
    piece('VetaSuperior',(.44,.07,.10),(-.12,.70,0),(104,206,208),'SmoothPlastic',rot=(0,20,0))],
'Ingot':[
    piece('Lingote',(1.02,.43,.72),(0,.215,0),(195,208,216)),
    piece('ExtremoIzq',(.72,.43,.25),(-.635,.215,0),(168,187,201),'Metal','WedgePart',rot=(0,90,0)),
    piece('ExtremoDer',(.72,.43,.25),(.635,.215,0),(222,230,233),'Metal','WedgePart',rot=(0,-90,0)),
    piece('Sello',(.26,.018,.26),(0,.439,0),(126,153,170),rot=(0,45,0))],
}
for x,z,w,h,angle,color in ((-.15,0,.36,1.02,20,(100,194,218)),(.28,.12,.28,.64,-20,(148,220,231)),(-.38,-.18,.24,.45,55,(80,160,193))):
    shaft=h*.62;tip=h-shaft
    SHAPES['BasicCrystal'].append(piece('CuerpoCristal',(w,shaft,w),(x,shaft/2,z),color,'Glass',rot=(0,angle,0)))
    SHAPES['BasicCrystal'].append(piece('PuntaCristal',(w,tip,w),(x,shaft+tip/2,z),color,'Glass','WedgePart',rot=(0,angle,0)))

def lua_source():
    def lua(v):
        if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
        if isinstance(v,(list,tuple)):return '{'+','.join(lua(x) for x in v)+'}'
        if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
        return str(v)
    return 'local cargoShapes='+lua(SHAPES)+'\n'+'''
-- Keep the existing animated Part as a carrier, with small anchored visual pieces.
-- Definitions can grow with Catalog.items without changing transport or recipes.
local function createCargo(model,name,item)
    local data=Catalog.items[item]
    local carrier=block(model,name,Vector3.new(.1,.1,.1),Vector3.zero,data.color,Enum.Material.SmoothPlastic)
    carrier.Transparency=1;carrier.CanCollide=false;carrier.CanTouch=false;carrier.CanQuery=false;carrier.CastShadow=false
    carrier:SetAttribute('ItemType',item)
    local shapes=cargoShapes[item]
    if not shapes then
        shapes={{name='Contenedor',size={1,.65,.8},pos={0,.325,0},color={150,169,182},material='Metal',kind='Part',shape='Block',rot={0,0,0}}}
    end
    local baseY=if model:GetAttribute('MachineType')=='Belt' then -.50 else -.22
    local pieces={}
    for _,spec in ipairs(shapes) do
        local part=Instance.new(spec.kind)
        part.Name=spec.name;part.Size=Vector3.new(unpack(spec.size))
        part.Color=Color3.fromRGB(unpack(spec.color));part.Material=Enum.Material[spec.material]
        if spec.kind=='Part' then part.Shape=Enum.PartType[spec.shape] end
        part.Anchored=true;part.CanCollide=false;part.CanTouch=false;part.CanQuery=false;part.CastShadow=false
        part.TopSurface=Enum.SurfaceType.Smooth;part.BottomSurface=Enum.SurfaceType.Smooth
        local pos=spec.pos;local rot=spec.rot
        local offset=CFrame.new(pos[1],pos[2]+baseY,pos[3])*CFrame.Angles(math.rad(rot[1]),math.rad(rot[2]),math.rad(rot[3]))
        part.CFrame=carrier.CFrame*offset;part.Parent=carrier
        table.insert(pieces,{part=part,offset=offset})
    end
    local moving=carrier:GetPropertyChangedSignal('CFrame'):Connect(function()
        for _,entry in ipairs(pieces) do entry.part.CFrame=carrier.CFrame*entry.offset end
    end)
    carrier.Destroying:Connect(function() moving:Disconnect() end)
    return carrier
end
'''
