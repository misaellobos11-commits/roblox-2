"""Original industrial machine geometry shared by runtime and auxiliary previews."""
from visuals.cargo_shapes import piece
from .content import MACHINES,COLORS,lua

DARK=(35,52,61);BODY=(53,74,83);STEEL=(151,171,179);GOLD=(188,149,76)

def machine_parts(machine):
    result=[];accent=COLORS[machine['family']];profile=machine['profile']
    def box(name,size,pos,color=BODY,material='Metal',rot=(0,0,0)):
        result.append(piece(name,size,pos,color,material,rot=rot))
    def cyl(name,pos,length,diameter,color=STEEL,axis='Y'):
        rot={'X':(0,0,0),'Y':(0,0,90),'Z':(0,90,0)}[axis]
        result.append(piece(name,(length,diameter,diameter),pos,color,shape='Cylinder',rot=rot))
    def ball(name,pos,size,color=accent):result.append(piece(name,(size,size,size),pos,color,'Glass',shape='Ball'))
    # Open low belt tunnel. Decoration never blocks authoritative mouths at y=.9.
    box('Zocalo',(7.45,.4,7.45),(0,.48,0),DARK)
    box('Bancada',(6.5,.55,5.7),(0,1.85,0))
    for x in (-2.9,2.9):
        for z in (-2.4,2.4):
            box('Pata',(.5,1,.5),(x,1.1,z),DARK)
            box('Perno',(.22,.12,.22),(x,2.18,z),GOLD)
    # Small front control panel sits above the +Z output, making orientation explicit.
    box('Consola',(1.55,.68,.22),(1.85,2.25,2.91),DARK)
    box('Pantalla',(1.02,.26,.04),(1.7,2.35,3.04),accent,'SmoothPlastic')
    box('Estado',(.18,.16,.06),(2.42,2.17,3.04),accent,'Neon')
    if profile=='rollers':
        for x in (-2.7,2.7):box('SoporteLaminadora',(.5,2.8,3.9),(x,3.35,0))
        for z in (-1.35,1.35):
            for y in (2.65,3.9):cyl('RodilloLaminador',(0,y,z),4.9,1.03,STEEL,'X')
        box('PlacaEnProceso',(3.8,.13,5.2),(0,3.25,0),accent)
    elif profile=='drawbench':
        for z in (-1.5,1.4):
            cyl('TamborTrefilado',(0,3.35,z),2.7,1.7,accent,'X')
            for x in (-1.5,1.5):cyl('DiscoTambor',(x,3.35,z),.2,2.15,STEEL,'X')
        for x in (-.65,0,.65):box('GuiaCable',(.09,.09,4.8),(x,4.1,0),GOLD)
    elif profile=='press':
        for x in (-2.35,2.35):box('ColumnaPrensa',(.65,4.1,1.2),(x,4.1,0),STEEL)
        box('TravesanoPrensa',(5.4,.65,2.2),(0,6.15,0))
        cyl('PistonPrensa',(0,4.9,0),1.9,.85)
        box('Troquel',(3.1,.8,2.7),(0,3.8,0),accent)
        cyl('MatrizEngranaje',(0,2.48,0),.4,2.5,GOLD)
    elif profile=='extruder':
        cyl('CamaraExtrusion',(0,3.3,-.4),4.4,2.1,BODY,'Z')
        for z in (-2.5,1.8):cyl('BridaExtrusion',(0,3.3,z),.25,2.7,STEEL,'Z')
        for x in (-.48,.48):cyl('TuboEnProceso',(x,3.3,2.35),1.1,.5,accent,'Z')
        box('MotorExtrusion',(2.1,1.3,1.4),(-1.8,3.1,-1.9),DARK)
    elif profile=='reactor':
        cyl('DepositoReactor',(0,3.9,0),3.4,3.2,accent)
        for y in (2.4,4,5.5):cyl('AroReactor',(0,y,0),.2,3.6,STEEL)
        ball('CupulaReactor',(0,5.55,0),2.6)
        for x in (-2.4,2.4):cyl('ColumnaReactivo',(x,3.1,-1.6),1.6,.85)
    elif profile=='mixer':
        cyl('CubaMezcladora',(0,3.35,0),2.4,4.1,accent)
        cyl('TapaMezcla',(0,4.65,0),.25,4.4,STEEL)
        box('MotorAgitador',(1.3,1.2,1.3),(0,5.35,0),DARK)
        for z in (-1,1):box('SoporteCuba',(5.5,.4,.45),(0,2.3,z))
    elif profile=='furnace':
        box('CamaraAleacion',(4.9,3.5,4.0),(0,3.9,0),DARK)
        box('PuertaHorno',(3.2,2.3,.2),(0,3.7,2.1),STEEL)
        box('VentanaCalor',(2.4,1.3,.12),(0,3.9,2.24),(238,137,70),'Neon')
        for x in (-1.8,1.8):cyl('Chimenea',(x,5.7,-1.2),2,.65)
    elif profile=='kiln':
        box('HornoTunel',(4.7,2.7,4.6),(0,3.55,0),(160,132,104))
        for z in (-2.35,2.35):
            box('MarcoCeramico',(3.5,1.8,.2),(0,3.15,z),DARK)
            box('RanuraHorno',(2.5,.35,.22),(0,2.65,z),(234,167,91),'Neon')
        for x in (-1.5,0,1.5):box('AletaTermica',(.3,.8,3.9),(x,5.25,0),STEEL)
    elif profile=='purifier':
        for x in (-1.65,1.65):
            cyl('TorrePurificacion',(x,3.75,0),3.1,1.75,STEEL)
            cyl('BandaPurificacion',(x,3.6,0),1.4,1.78,accent)
            cyl('TapaTorre',(x,5.4,0),.25,2.0,DARK)
        box('PuentePurificador',(3.9,.4,.6),(0,5.5,-.6),GOLD)
    elif profile=='cutter':
        box('MesaOptica',(5.4,.5,4.3),(0,2.5,0),STEEL)
        for x in (-2.4,2.4):box('GuiaCorte',(.35,2.8,.4),(x,3.8,-.8))
        box('PuenteLaser',(5.2,.6,.8),(0,5.25,-.8))
        cyl('CabezalLaser',(0,4.6,-.8),1,.6,accent)
        cyl('LenteEnMesa',(0,2.95,.5),.3,1.8,accent)
    elif profile=='winder':
        for x in (-2.4,2.4):box('CaballeteBobinado',(.6,2.6,2.2),(x,3.4,0))
        cyl('EjeBobinadora',(0,3.5,0),5.1,.5,STEEL,'X')
        cyl('CobreBobinado',(0,3.5,0),3.2,2.4,(201,124,67),'X')
        for x in (-1.7,1.7):cyl('CarreteBobinadora',(x,3.5,0),.25,3,STEEL,'X')
        box('GuiaBobinadora',(4,.3,.3),(0,4.65,1.8),GOLD)
    elif profile=='circuit':
        box('PlacaEnsamblado',(4.6,.2,3.8),(0,2.3,0),(53,127,105))
        for x in (-2.55,2.55):box('RailEnsambladora',(.4,2.5,.5),(x,3.5,-1.3),STEEL)
        box('CarroEnsambladora',(5.4,.5,.8),(0,4.8,-1.3))
        for x in (-1.2,0,1.2):cyl('InyectorCircuito',(x,3.9,-1.3),1.4,.28,GOLD)
        for x in (-1,1):box('ComponenteCircuito',(.8,.35,1),(x,2.55,.5),DARK)
    elif profile=='chip':
        box('CabinaLimpia',(5.0,3.7,4.6),(0,4.05,0),STEEL)
        box('VentanaLitografia',(3.9,2,.2),(0,4.25,2.4),(51,76,96),'Glass')
        box('LaserLitografia',(2,.45,.25),(0,4.9,2.55),accent,'Neon')
        for x in (-1.4,1.4):cyl('ExtractorLimpio',(x,6.05,-.5),.4,1.5,DARK)
    elif profile=='motor':
        for x in (-2.5,2.5):box('SoporteMotor',(.5,2.4,1.5),(x,3.3,0),STEEL)
        cyl('RotorEnsamblado',(0,3.65,0),3.7,2.1,accent,'X')
        for x in (-1.9,1.9):cyl('MordazaMotor',(x,3.65,0),.4,2.6,DARK,'X')
        box('BrazoMontaje',(2.8,.45,.6),(.3,5.15,-1.5),STEEL)
        box('PinzaMontaje',(.5,1.3,.5),(1.4,4.65,-1.5),GOLD)
    elif profile=='cell':
        for x in (-1.5,0,1.5):
            cyl('CeldaEnCarga',(x,3.5,0),2.5,.9,accent)
            cyl('TerminalCelda',(x,4.85,0),.2,.5,GOLD)
        for z in (-1.5,1.5):box('BancoCeldas',(5.3,.55,.65),(0,2.4,z))
        box('PuenteElectrico',(5.3,.4,.6),(0,5.3,-1.5),STEEL)
        for x in (-1.5,0,1.5):box('ContactoCelda',(.15,.6,1.5),(x,5,-.75),GOLD)
    elif profile=='sensor':
        box('BancoCalibracion',(5.5,.6,4.4),(0,2.5,0),STEEL)
        for x in (-1.7,1.7):
            cyl('OpticaCalibracion',(x,3.8,0),1.6,1.5,DARK,'Z')
            cyl('CristalCalibracion',(x,3.8,1),.2,1.2,accent,'Z')
        box('PantallaCalibracion',(2.5,1.4,.3),(0,5,-1.7),DARK)
        box('DisplayCalibracion',(2,.8,.07),(0,5,-1.5),accent,'SmoothPlastic')
    elif profile=='frame':
        for x in (-2.1,2.1):box('VigaEstructural',(.6,3.4,.6),(x,3.9,0),STEEL)
        for y in (2.5,5.5):box('TravesanoEstructural',(4.8,.6,.6),(0,y,0),STEEL)
        for x in (-2.7,2.7):box('MordazaEstructural',(.55,.65,2.4),(x,2.5,0),accent)
        box('DiagonalEstructural',(.35,4.7,.35),(0,4,0),GOLD,rot=(0,0,-49))
    elif profile=='robot':
        cyl('BaseRobot',(-1.5,2.5,0),.65,2.0,DARK)
        box('BrazoRobot',(.85,2.8,.85),(-1.5,4.1,0),accent,rot=(0,0,-15))
        cyl('ArticulacionRobot',(-1.1,5.4,0),1.1,1.2,STEEL,'Z')
        box('AntebrazoRobot',(2.7,.65,.7),(.3,5.3,0),accent,rot=(0,0,-12))
        for z in (-.45,.45):box('PinzaRobot',(.3,1.2,.25),(1.7,4.6,z),STEEL)
        box('MesaRobot',(2.1,.4,2.6),(1.6,2.65,0),DARK)
    elif profile=='compressor':
        cyl('CamaraCompresion',(0,3.65,0),2.7,2.8,DARK)
        for x in (-2.1,2.1):
            cyl('PistonCompresion',(x,3.65,0),1.5,1.3,STEEL,'X')
            box('BancadaCompresion',(.6,3.7,2.4),(x,4,0),accent)
        for y in (2.3,5):cyl('AnilloCompresion',(0,y,0),.3,3.2,accent)
    elif profile=='core':
        cyl('BaseContencion',(0,2.6,0),.7,3.9,DARK)
        ball('NucleoSuspendido',(0,4.2,0),2.3)
        for x in (-2,2):
            box('TorreContencion',(.65,3.9,.8),(x,4.2,0),STEEL)
            box('BobinaContencion',(.25,2.3,1),(x*.84,4.2,0),accent,'Neon')
        cyl('CoronaContencion',(0,6.15,0),.3,4.4,STEEL)
    else:raise ValueError(profile)
    return result

MODELS={m['id']:machine_parts(m) for m in MACHINES}

def source():
    return '\nlocal expansionModels='+lua(MODELS)+'''
local function styleExpansion(model,rec)
 for _,spec in ipairs(expansionModels[rec.machineType]) do
  local part=detail(model,spec.name,Vector3.new(unpack(spec.size)),Vector3.new(unpack(spec.pos)),Color3.fromRGB(unpack(spec.color)),Enum.Material[spec.material])
  part.Shape=Enum.PartType[spec.shape]
  part.CFrame=part.CFrame*CFrame.Angles(math.rad(spec.rot[1]),math.rad(spec.rot[2]),math.rad(spec.rot[3]))
 end
 model:SetAttribute('ExpansionModel',rec.machineType)
 makePorts(model,rec)
end
'''
