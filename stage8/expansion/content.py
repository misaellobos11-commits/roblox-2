"""One source of truth for the 8.21 industrial extension (fictional recipes)."""
import json
import math

COLORS={
    'Metalurgia':(193,159,99),'Química':(116,191,140),'Cristales':(112,211,227),
    'Electrónica':(112,165,220),'Componentes':(225,158,92),'Avanzada':(174,137,228),
}
# Recipe tuple: output ID, Spanish name, input quantities, seconds, cargo silhouette.
MACHINES=[
 dict(id='RollingMill',name='Laminadora',family='Metalurgia',tier=5,price=850,profile='rollers',recipes=[
  ('MetalPlate','Placa metálica',{'Ingot':1},4,'plates'),('CopperSheet','Lámina de cobre',{'Copper':2},3.6,'plates')]),
 dict(id='WireDrawer',name='Trefiladora',family='Metalurgia',tier=4,price=380,profile='drawbench',recipes=[
  ('CopperWire','Cable de cobre',{'Copper':1},3,'spool'),('ConductiveWire','Cable conductor',{'ConductiveMix':1},3.6,'spool')]),
 dict(id='GearPress',name='Prensa de engranajes',family='Metalurgia',tier=5,price=950,profile='press',recipes=[
  ('Gear','Engranaje',{'Ingot':1},4.2,'gear'),('ReinforcedGear','Engranaje reforzado',{'MetalPlate':1,'BaseMetal':1},4.8,'gear')]),
 dict(id='TubeExtruder',name='Extrusora de tubos',family='Metalurgia',tier=5,price=820,profile='extruder',recipes=[
  ('MetalTube','Tubo metálico',{'Ingot':1},4,'tubes'),('CopperTube','Tubo de cobre',{'Copper':2},3.6,'tubes')]),
 dict(id='ChemicalReactor',name='Reactor químico',family='Química',tier=3,price=520,profile='reactor',recipes=[
  ('Polymer','Polímero',{'Hydrogen':1,'CarbonCompound':1},3.6,'pellets'),('Resin','Resina',{'CarbonCompound':1,'Oxygen':1},3.6,'canister')]),
 dict(id='IndustrialMixer',name='Mezcladora industrial',family='Química',tier=4,price=650,profile='mixer',recipes=[
  ('Insulator','Aislante',{'Polymer':1,'Silicate':1},4.2,'plates'),('Composite','Compuesto reforzado',{'Resin':1,'Carbon':1},4.2,'plates')]),
 dict(id='AlloyFurnace',name='Horno de aleaciones',family='Metalurgia',tier=5,price=1200,profile='furnace',recipes=[
  ('Steel','Acero',{'Ingot':1,'Carbon':1},4.8,'bar'),('ConductiveAlloy','Aleación conductiva',{'Ingot':1,'ConductiveMix':1},5.4,'bar')]),
 dict(id='CeramicKiln',name='Horno cerámico',family='Química',tier=5,price=900,profile='kiln',recipes=[
  ('Ceramic','Cerámica técnica',{'Silicate':1,'Carbon':1},4.2,'tiles'),('HeatShield','Escudo térmico',{'Ceramic':1,'MetalPlate':1},4.8,'shield')]),
 dict(id='CrystalPurifier',name='Purificadora de cristales',family='Cristales',tier=5,price=1050,profile='purifier',recipes=[
  ('PureCrystal','Cristal puro',{'BasicCrystal':1,'Oxygen':1},4.8,'crystal'),('ResonantCrystal','Cristal resonante',{'PureCrystal':1,'ConductiveMix':1},5.4,'crystal')]),
 dict(id='LensCutter',name='Cortadora óptica',family='Cristales',tier=5,price=1100,profile='cutter',recipes=[
  ('Lens','Lente óptica',{'PureCrystal':1},4.2,'lens'),('CrystalPrism','Prisma cristalino',{'ResonantCrystal':1},4.8,'prism')]),
 dict(id='CoilWinder',name='Bobinadora',family='Componentes',tier=5,price=1000,profile='winder',recipes=[
  ('Coil','Bobina',{'CopperWire':1,'Iron':1},4.2,'coil'),('MagneticCoil','Bobina magnética',{'ConductiveWire':1,'Steel':1},4.8,'coil')]),
 dict(id='CircuitAssembler',name='Ensambladora electrónica',family='Electrónica',tier=5,price=1250,profile='circuit',recipes=[
  ('Circuit','Circuito',{'ConductiveMix':1,'BasicCrystal':1},4.8,'circuit'),('AdvancedCircuit','Circuito avanzado',{'Circuit':1,'Polymer':1},5.4,'circuit')]),
 dict(id='ChipFabricator',name='Fabricadora de microchips',family='Electrónica',tier=6,price=1900,profile='chip',recipes=[
  ('Microchip','Microchip',{'Silicon':1,'Circuit':1},5.4,'chip'),('ControlChip','Procesador de control',{'Microchip':1,'PureCrystal':1},6,'chip')]),
 dict(id='MotorAssembler',name='Ensambladora de motores',family='Componentes',tier=6,price=2100,profile='motor',recipes=[
  ('Motor','Motor eléctrico',{'Coil':1,'Gear':1},5.4,'motor'),('PrecisionMotor','Motor de precisión',{'MagneticCoil':1,'ReinforcedGear':1},6,'motor')]),
 dict(id='CellFabricator',name='Fabricadora de celdas',family='Electrónica',tier=6,price=2200,profile='cell',recipes=[
  ('EnergyCell','Celda energética',{'Hydrogen':1,'ConductiveAlloy':1},5.4,'cell'),('Battery','Batería industrial',{'EnergyCell':1,'Insulator':1},6,'battery')]),
 dict(id='SensorAssembler',name='Ensambladora de sensores',family='Electrónica',tier=6,price=2000,profile='sensor',recipes=[
  ('Sensor','Sensor',{'Lens':1,'Circuit':1},5.4,'sensor'),('OpticalSensor','Sensor óptico',{'CrystalPrism':1,'AdvancedCircuit':1},6,'sensor')]),
 dict(id='FrameAssembler',name='Ensambladora estructural',family='Componentes',tier=6,price=1800,profile='frame',recipes=[
  ('Frame','Bastidor industrial',{'MetalTube':1,'MetalPlate':1},4.8,'frame'),('ReinforcedFrame','Bastidor reforzado',{'Steel':1,'Composite':1},5.4,'frame')]),
 dict(id='RoboticsAssembler',name='Ensambladora robótica',family='Avanzada',tier=7,price=3500,profile='robot',recipes=[
  ('Actuator','Actuador',{'Motor':1,'Frame':1},6,'actuator'),('RoboticArm','Brazo robótico',{'PrecisionMotor':1,'ControlChip':1},7.2,'robot')]),
 dict(id='MatterCompressor',name='Compresora de materia',family='Avanzada',tier=7,price=3800,profile='compressor',recipes=[
  ('DenseMatter','Materia densa',{'ResonantCrystal':1,'Composite':1},6.6,'core'),('Stabilizer','Estabilizador',{'DenseMatter':1,'MagneticCoil':1},7.2,'stabilizer')]),
 dict(id='CoreAssembler',name='Ensambladora de núcleos',family='Avanzada',tier=8,price=6000,profile='core',recipes=[
  ('MatterCore','Núcleo de materia',{'Stabilizer':1,'Battery':1},7.8,'core'),('QuantumCore','Núcleo cuántico',{'MatterCore':1,'OpticalSensor':1},9,'core')]),
]

def lua(value):
    if isinstance(value,str):return json.dumps(value,ensure_ascii=False)
    if isinstance(value,bool):return 'true' if value else 'false'
    if isinstance(value,(tuple,list)):return '{'+','.join(lua(v) for v in value)+'}'
    if isinstance(value,dict):return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in value.items())+'}'
    return str(value)

def expanded_items():
    values=dict(RawMatter=1,Carbon=8,Oxygen=10,Silicon=12,Iron=12,Copper=14,Hydrogen=11,CarbonCompound=24,Silicate=26,BaseMetal=30,ConductiveMix=34,BasicCrystal=55,SyntheticOre=62,Ingot=95)
    result={}
    for machine in MACHINES:
        for index,(key,name,inputs,seconds,shape) in enumerate(machine['recipes']):
            value=math.ceil(sum(values[i]*n for i,n in inputs.items())*1.25/5)*5
            values[key]=value
            color=COLORS[machine['family']]
            if 'Copper' in key:color=(211,138,82)
            elif index:color=tuple(min(245,c+25) for c in color)
            result[key]=dict(name=name,value=value,color=color,shape=shape)
    return result

def catalog_source():
    machines=[]
    for m in MACHINES:
        recipes=[dict(id='expand_'+r[0],name=r[1],inputs=r[2],outputs={r[0]:1},seconds=r[3]) for r in m['recipes']]
        machines.append(dict(id=m['id'],name=m['name'],family=m['family'],color=COLORS[m['family']],profile=m['profile'],dual=any(len(r[2])>1 for r in m['recipes']),recipes=recipes))
    return '\nlocal expansion='+lua(machines)+'\nlocal expansionItems='+lua(expanded_items())+'''
C.expansionOrder={}
for item,data in pairs(expansionItems) do
 data.color=rgb(unpack(data.color));C.items[item]=data
end
for _,entry in ipairs(expansion) do
 C.types[entry.id]={name=entry.name,size=2,color=rgb(unpack(entry.color)),group=entry.family,
  expansion=true,profile=entry.profile,inputTags=if entry.dual then {'left_in','right_in'} else {'back'},
  description=entry.name..': '..entry.recipes[1].name..' o '..entry.recipes[2].name..'.'}
 table.insert(C.order,entry.id);table.insert(C.expansionOrder,entry.id)
 C.recipeOrder[entry.id]={}
 for _,recipe in ipairs(entry.recipes) do
  C.recipes[recipe.id]=recipe;table.insert(C.recipeOrder[entry.id],recipe.id)
 end
end
-- Preserve the familiar starting choices, then include every registered material.
local extra={}
for item in pairs(C.items) do if not table.find(C.filterOrder,item) then table.insert(extra,item) end end
table.sort(extra,function(a,b)return C.items[a].name<C.items[b].name end)
for _,item in ipairs(extra) do table.insert(C.filterOrder,item) end
'''

def details_source():
    return '''
-- Recipe data is authoritative for descriptions, including future machines.
for typ,list in pairs(C.recipeOrder) do
 local recipe=C.recipes[list[1]]
 C.details[typ]={inputs=C.recipeLines(recipe,'inputs'),outputs=C.recipeLines(recipe,'outputs'),
  cycle=tostring(recipe.seconds)..' s',notes=if #list>1 then 'G cambia la receta. Comprueba las entradas antes de producir.' else 'Producción fija.'}
end
'''

def economy_source():
    return '\nlocal expansionEconomy='+lua({m['id']:dict(price=m['price'],tier=m['tier']) for m in MACHINES})+'''
for typ,entry in pairs(expansionEconomy) do E.prices[typ]=entry.price;E.tiers[typ]=entry.tier end
E.unlockThresholds={0,180,650,1800,4000,10000,25000,60000}
E.levelNames={'Inicio','Procesamiento','Síntesis','Industria','Tecnología avanzada','Automatización','Robótica','Materia avanzada'}
'''
