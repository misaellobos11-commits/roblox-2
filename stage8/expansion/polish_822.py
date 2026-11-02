"""8.22 art pass. Existing 8.21 geometry stays reproducible and ports stay logical."""
import copy
import math
from .models import MODELS as ORIGINAL, DARK, BODY, STEEL, GOLD
from .content import MACHINES, COLORS, lua
from visuals.cargo_shapes import piece

EDGE=(91,113,123)
RUBBER=(26,36,42)
PAINT=(66,86,94)

class Kit:
    def __init__(self,parts):self.parts=parts
    def box(self,name,size,pos,color=BODY,material='Metal',rot=(0,0,0),kind='Part',alpha=0):
        spec=piece(name,size,pos,color,material,kind=kind,rot=rot)
        if alpha:spec['transparency']=alpha
        self.parts.append(spec)
        return spec
    def cylinder(self,name,pos,length,diameter,color=STEEL,axis='Y'):
        spec=piece(name,(length,diameter,diameter),pos,color,shape='Cylinder',rot={'X':(0,0,0),'Y':(0,0,90),'Z':(0,90,0)}[axis])
        self.parts.append(spec)
        return spec
    def pipe(self,name,a,b,width=.16,color=STEEL):
        # Axis-aligned pipe runs keep geometry cheap, readable and easy to author.
        delta=[abs(b[i]-a[i]) for i in range(3)]
        assert sum(v>1e-6 for v in delta)==1
        axis=max(range(3),key=lambda i:delta[i])
        self.cylinder(name,tuple((a[i]+b[i])/2 for i in range(3)),delta[axis],width,color,'XYZ'[axis])
    def ring(self,name,pos,radius,width=.15,color=GOLD):
        for i in range(8):
            angle=i*math.tau/8
            self.box(name,(width,width,2*radius*math.tan(math.pi/8)),
                (pos[0]+radius*math.cos(angle),pos[1],pos[2]+radius*math.sin(angle)),color,
                rot=(0,-math.degrees(angle),0))
    def find(self,name):return [p for p in self.parts if p['name']==name]
    def remove(self,*names):self.parts[:]=[p for p in self.parts if p['name'] not in names]

def polish(machine):
    parts=copy.deepcopy(ORIGINAL[machine['id']]);k=Kit(parts)
    accent=COLORS[machine['family']];profile=machine['profile']
    # Layered chassis and sloping shoulders replace the exposed tabletop look.
    k.find('Zocalo')[0]['size']=(7.35,.3,7.35)
    k.find('Zocalo')[0]['color']=EDGE
    k.box('BaseAntivibratoria',(7.5,.16,7.5),(0,.22,0),RUBBER,'SmoothPlastic')
    k.box('FaldonCentral',(5.9,.55,5.2),(0,1.32,0),DARK)
    for side in (-1,1):
        # Side fairings are high enough to leave the inlet mouths clear.
        k.box('HombroBiselado',(5.6,.42,.8),(side*2.96,2.05,0),PAINT,
              rot=(0,side*90,0),kind='WedgePart')
        k.box('PlacaLateral',(.1,.7,2.3),(side*3.27,1.74,-.15),DARK)
        k.box('IdentificadorFamilia',(.12,.15,1.7),(side*3.29,1.93,-.15),accent,'SmoothPlastic')
        for z in (-.65,0,.65):
            k.box('RejillaLateral',(.13,.1,.36),(side*3.29,1.62,z),EDGE)
        # Visible lower edge stops short of the front/back port center.
        k.box('MolduraFrontal',(1.9,.14,.17),(side*2.55,.65,3.45),DARK)
    k.box('MarcoConsola',(1.75,.88,.16),(1.85,2.25,2.91),EDGE)
    k.find('Consola')[0]['pos']=(1.85,2.25,3.00)
    k.find('Pantalla')[0]['pos']=(1.7,2.35,3.14)
    k.find('Estado')[0]['pos']=(2.42,2.17,3.14)
    for x in (1.28,1.55,1.82):k.box('TeclaConsola',(.14,.08,.04),(x,2.1,3.14),STEEL)
    k.box('PanelServicio',(1.7,.6,.18),(-1.85,2.15,2.96),PAINT)
    k.box('CierreServicio',(.4,.08,.09),(-1.85,2.17,3.08),GOLD)
    # Guard stripe outside the center path. The port colors retain their meaning.
    for x in (-2.7,-2.3,-1.9):
        k.box('MarcaPrecaucion',(.19,.035,.45),(x,.665,3.17),GOLD,'SmoothPlastic',rot=(0,-25,0))

    if profile=='rollers':
        for p in k.find('PlacaEnProceso'):p['color']=STEEL
        for x in (-2.7,2.7):
            for z in (-1.35,1.35):
                k.cylinder('CojineteRodillo',(x,3.9,z),.58,.75,DARK,'X')
                k.cylinder('TapaCojinete',(x*1.12,3.9,z),.1,.43,GOLD,'X')
            k.box('ProtectorLaminadora',(.16,.68,2.5),(x*1.06,3.05,0),accent)
        k.box('DeflectorLaminado',(4.4,.18,1.1),(0,2.32,2.4),PAINT)
    elif profile=='drawbench':
        for z in (-1.5,1.4):
            for x in (-.9,0,.9):k.cylinder('EstriaTrefilado',(x,3.35,z),.08,1.74,GOLD,'X')
        k.box('CajaTransmision',(1.1,1.45,3.75),(2.25,3.25,-.05),PAINT)
        for z in (-1.1,0,1.1):k.box('VentilacionTransmision',(.08,.55,.22),(2.83,3.3,z),DARK)
        k.box('GuardaDeHilo',(4.3,.2,.38),(0,3.6,2.45),STEEL)
    elif profile=='press':
        k.box('CapotaPrensa',(5.65,.24,2.65),(0,6.55,0),PAINT)
        for x in (-2.35,2.35):
            k.box('FuellePrensa',(.8,.8,1.35),(x,2.65,0),RUBBER)
            k.box('RotuloPrensa',(.22,1.6,.1),(x,4.5,.66),accent,'SmoothPlastic')
        k.cylinder('CamisaHidraulica',(0,5.5,0),1.0,1.3,DARK)
        k.pipe('ConductoHidraulico',(0,5.75,-.8),(1.65,5.75,-.8),.17,GOLD)
        k.pipe('RetornoHidraulico',(1.65,5.75,-.8),(1.65,3.0,-.8),.17,GOLD)
        for x in (-1,0,1):k.box('RanuraMatriz',(.13,.04,1.7),(x,2.71,0),DARK)
    elif profile=='extruder':
        for z in (-1.9,-1.0,-.1,.8):k.cylinder('BandaCamara',(0,3.3,z),.18,2.2,EDGE,'Z')
        k.cylinder('CabezalExtrusion',(0,3.3,1.95),.45,1.8,DARK,'Z')
        for p in k.find('TuboEnProceso'):p['color']=STEEL
        for y in (2.75,3.0,3.25):k.box('RejillaMotorExtrusion',(1.35,.1,.06),(-1.8,y,-2.64),STEEL)
        k.box('TolvaEntrada',(1.5,.7,1.4),(0,4.65,-1.4),accent)
        k.box('BocaTolva',(1.16,.08,1.05),(0,5.04,-1.4),DARK)
    elif profile=='reactor':
        k.find('DepositoReactor')[0]['color']=PAINT
        k.find('CupulaReactor')[0]['color']=accent
        k.find('CupulaReactor')[0]['size']=(2.6,1.5,2.6)
        k.find('CupulaReactor')[0]['pos']=(0,5.65,0)
        k.cylinder('SombrereteReactor',(0,6.48,0),.2,1.0,STEEL)
        k.box('IndicadorNivel',(.5,1.9,.15),(0,3.9,1.62),DARK)
        k.box('FluidoIndicador',(.22,1.4,.07),(0,3.7,1.73),accent,'SmoothPlastic')
        for x in (-2.4,2.4):
            k.pipe('TuboReactivoVertical',(x,2.3,-1.6),(x,4.5,-1.6),.24,EDGE)
            k.pipe('TuboReactivoSuperior',(x,4.5,-1.6),(0,4.5,-1.6),.24,EDGE)
        k.cylinder('Manometro',(1.95,4.7,.1),.16,.68,STEEL,'Z')
        k.cylinder('EsferaManometro',(1.95,4.7,.21),.05,.52,DARK,'Z')
        k.box('Aguja',(.05,.23,.03),(1.95,4.76,.25),GOLD,rot=(0,0,-30))
    elif profile=='mixer':
        k.find('CubaMezcladora')[0]['color']=PAINT
        for y in (2.3,4.35):k.cylinder('AroCuba',(0,y,0),.16,4.22,STEEL)
        for x in (-1.55,1.55):k.box('AbrazaderaCuba',(.18,1.9,.2),(x,3.35,1.4),GOLD)
        k.cylinder('BocaCarga',(1.05,4.96,0),.5,.92,DARK)
        k.cylinder('TapaCarga',(1.05,5.24,0),.13,1.12,STEEL)
        for z in (-.4,0,.4):k.box('AletaMotorMezcla',(1.4,.12,.11),(0,5.7,z),EDGE)
        k.pipe('DesagueMezcla',(-2.25,3.2,0),(-2.25,2.2,0),.28,GOLD)
    elif profile=='furnace':
        k.find('VentanaCalor')[0]['size']=(2.35,.82,.12)
        for y in (3.5,3.9,4.3):k.box('ProtectorVentana',(2.6,.09,.17),(0,y,2.35),DARK)
        for x in (-2.55,2.55):
            k.box('PanelHorno',(.18,2.5,2.95),(x,3.85,0),PAINT)
            k.box('BiselHorno',(4.0,.42,.45),(x*.94,5.58,0),EDGE,rot=(0,90 if x>0 else -90,0),kind='WedgePart')
        for x in (-1.8,1.8):
            k.cylinder('ChimeneaBase',(x,5.95,-1.2),.22,1.05,DARK)
            k.cylinder('SombrereteHorno',(x,6.8,-1.2),.16,1.05,STEEL)
    elif profile=='kiln':
        k.find('HornoTunel')[0]['color']=(115,111,98)
        for z in (-1.55,0,1.55):
            k.box('JuntaHorno',(4.85,.14,.16),(0,4.9,z),DARK)
        for x in (-2.43,2.43):
            k.box('PlacaCeramica',(.13,1.65,3.5),(x,3.65,0),PAINT)
            k.box('IndicadorCalor',(.15,.11,2.2),(x,4.2,0),accent,'SmoothPlastic')
        k.box('ViseraHorno',(3.65,.24,.7),(0,4.2,2.34),STEEL)
        k.box('CeramicaEnProceso',(1.9,.12,1.0),(0,2.28,2.2),(193,174,140),'Slate')
    elif profile=='purifier':
        for x in (-1.65,1.65):
            for y in (2.35,4.9):k.cylinder('CollarinTorre',(x,y,0),.15,1.98,EDGE)
            k.box('MirillaPurificador',(.45,1.55,.15),(x,3.7,.93),DARK)
            k.box('LecturaPurificador',(.18,1.1,.06),(x,3.6,1.03),accent,'SmoothPlastic')
        k.pipe('RetornoSuperior',(-1.65,5.8,-.3),(1.65,5.8,-.3),.25,STEEL)
        for x in (-1.65,1.65):k.pipe('CodoPurificacion',(x,5.8,-.3),(x,5.25,-.3),.25,STEEL)
    elif profile=='cutter':
        k.box('MesaNegra',(4.7,.1,3.55),(0,2.8,0),DARK)
        for x in (-1.8,-.9,0,.9,1.8):k.box('RanuraMesa',(.045,.03,3.25),(x,2.87,0),EDGE)
        for x in (-2.4,2.4):k.cylinder('GuiaPrecision',(x,3.9,-.8),2.55,.2,STEEL)
        k.box('CarroOptico',(1.3,.9,1.15),(0,5.15,-.8),PAINT)
        k.cylinder('AnilloCabezal',(0,4.2,-.8),.18,.86,STEEL)
        k.box('ProtectorOptico',(4.6,.4,.25),(0,3.2,1.85),accent,'Glass',alpha=.25)
    elif profile=='winder':
        for x in (-1.2,-.6,0,.6,1.2):k.cylinder('EspiraBobinadora',(x,3.5,0),.08,2.44,GOLD,'X')
        for x in (-2.4,2.4):k.cylinder('CojineteBobinadora',(x,3.5,0),.7,.9,STEEL,'X')
        k.box('MotorBobinadora',(1.0,1.0,2.0),(-2.7,2.7,0),DARK)
        k.box('GuardaBobina',(4.2,.28,.65),(0,2.8,2.1),accent)
        k.box('CarroGuiahilo',(.75,.65,.7),(.8,4.65,1.8),PAINT)
    elif profile=='circuit':
        for x in (-1.2,0,1.2):
            k.box('CarroInyector',(.65,.7,1.05),(x,4.7,-1.3),PAINT)
            k.box('PistaCircuito',(.065,.025,2.4),(x,2.42,0),GOLD)
        for x in (-2.4,2.4):
            k.box('CarrilPlaca',(.3,.3,4.1),(x,2.45,0),STEEL)
            k.box('CartuchoComponentes',(.5,.7,1.4),(x,2.9,1.15),accent)
        k.box('PuenteConexion',(4.9,.16,.18),(0,5.15,-1.3),GOLD)
    elif profile=='chip':
        k.find('CabinaLimpia')[0]['color']=PAINT
        for x in (-2.4,2.4):k.box('MarcoCabina',(.25,3.6,.25),(x,4.05,2.4),STEEL)
        k.box('BiselCabina',(4.75,.38,.65),(0,6.0,2.0),EDGE,kind='WedgePart')
        k.box('PanelInferiorChip',(3.65,.75,.14),(0,2.72,2.39),DARK)
        for x in (-1.2,-.4,.4,1.2):k.box('RejillaCabina',(.5,.1,.18),(x,2.7,2.52),EDGE)
        for x in (-1.4,1.4):k.cylinder('FiltroCabina',(x,6.15,-.5),.25,1.15,STEEL)
    elif profile=='motor':
        for x in (-1.3,-.65,0,.65,1.3):k.cylinder('AletaRotor',(x,3.65,0),.11,2.2,EDGE,'X')
        k.cylinder('AcopleRotor',(2.3,3.65,0),.95,.6,GOLD,'X')
        k.box('ColumnaMontaje',(.6,2.9,.6),(-1.0,3.7,-1.5),PAINT)
        k.cylinder('JuntaMontaje',(-1.0,5.1,-1.5),.8,.85,EDGE,'Z')
        for z in (-1.95,-1.05):k.box('PinzaMotor',(.35,.6,.15),(1.4,4.1,z),STEEL)
    elif profile=='cell':
        for x in (-1.5,0,1.5):
            k.cylinder('BaseCelda',(x,2.4,0),.3,1.15,DARK)
            k.cylinder('CollarinCelda',(x,4.5,0),.13,1.06,STEEL)
            k.box('IndicadorCelda',(.18,.8,.07),(x,3.6,.48),STEEL,'SmoothPlastic')
        k.box('BarreraCarga',(5.2,.3,.45),(0,2.9,1.55),accent)
        k.box('UnidadCarga',(1.4,1.15,.65),(0,4.65,-1.65),DARK)
    elif profile=='sensor':
        for x in (-1.7,1.7):
            k.cylinder('AroObjetivo',(x,3.8,.8),.12,1.7,STEEL,'Z')
            k.cylinder('AnilloOptico',(x,3.8,1.12),.1,1.32,DARK,'Z')
            k.find('CristalCalibracion')[0]['color']=accent
            k.box('PieOptica',(.6,.7,1.3),(x,3.1,0),PAINT)
        k.box('MastilCalibracion',(.35,1.7,.35),(0,3.9,-1.7),STEEL)
        k.box('ReticulaHorizontal',(1.5,.04,.04),(0,5,-1.45),STEEL,'SmoothPlastic')
        k.box('ReticulaVertical',(.04,.65,.04),(0,5,-1.44),STEEL,'SmoothPlastic')
    elif profile=='frame':
        for x in (-2.1,2.1):
            for y in (2.6,5.4):k.box('UnionEstructural',(.85,.65,.18),(x,y,.38),PAINT)
            k.box('MordazaSoldadura',(.5,1.2,1.2),(x*.75,3.0,0),DARK)
        k.box('SoldadorAutomatico',(1.1,1.0,.9),(0,5.8,0),accent)
        k.cylinder('PuntaSoldador',(0,5.1,0),.55,.22,GOLD)
        for z in (-1.4,1.4):k.box('GuiaBastidor',(4.8,.2,.15),(0,2.3,z),STEEL)
    elif profile=='robot':
        for p in k.find('BrazoRobot')+k.find('AntebrazoRobot'):p['color']=PAINT
        k.cylinder('RotulaInferior',(-1.5,2.85,0),.9,1.25,STEEL,'Z')
        k.cylinder('TapaRotula',(-1.1,5.4,.62),.12,.8,accent,'Z')
        k.box('CubiertaBrazo',(.14,2.0,.95),(-1.92,4.1,0),accent,rot=(0,0,-15))
        k.box('CubiertaAntebrazo',(1.85,.15,.8),(.3,5.67,0),accent,rot=(0,0,-12))
        k.cylinder('MunecaRobot',(1.7,4.9,0),.8,.6,STEEL,'Z')
        k.box('FuellePinza',(.65,.55,.65),(1.7,4.65,0),DARK)
        for x in (1.0,2.2):k.box('FijacionMesa',(.16,.25,1.7),(x,2.95,0),GOLD)
    elif profile=='compressor':
        for y in (2.8,3.25,3.7,4.15,4.6):k.cylinder('ArmaduraCompresion',(0,y,0),.1,2.92,EDGE)
        for x in (-2.1,2.1):
            k.box('MarcoHidraulico',(.72,.3,2.6),(x,5.3,0),STEEL)
            k.box('IndicadorPresion',(.15,1.7,.09),(x,4,1.28),accent,'SmoothPlastic')
        k.box('ColectorPresion',(2.9,.5,.6),(0,5.6,-1.0),DARK)
        k.pipe('TuberiaPresion',(-1.5,5.6,-1.0),(1.5,5.6,-1.0),.15,GOLD)
    elif profile=='core':
        # A hollow crown keeps the suspended core visible from the build camera.
        k.remove('CoronaContencion')
        k.ring('CoronaAbierta',(0,6.15,0),2.1,.22,STEEL)
        k.ring('BobinadoInferior',(0,3.05,0),1.75,.12,GOLD)
        for x in (-2,2):
            k.box('BlindajeContencion',(.85,2.45,1.2),(x,4.15,0),PAINT)
            k.box('BobinaExterior',(.18,1.8,.12),(x*1.23,4.15,.42),accent,'SmoothPlastic')
        k.find('NucleoSuspendido')[0]['size']=(1.95,1.95,1.95)
    else:raise ValueError(profile)
    return parts

MODELS={m['id']:polish(m) for m in MACHINES}

def source():
    return '\nlocal expansionModels='+lua(MODELS)+'''
local function styleExpansion(model,rec)
 for _,spec in ipairs(expansionModels[rec.machineType]) do
  local part=Instance.new(spec.kind)
  part.Name=spec.name;part.Size=Vector3.new(unpack(spec.size))
  part.Color=Color3.fromRGB(unpack(spec.color));part.Material=Enum.Material[spec.material]
  if spec.kind=='Part' then part.Shape=Enum.PartType[spec.shape] end
  part.Anchored=true;part.CanCollide=false;part.CanTouch=false;part.CanQuery=false;part.CastShadow=false
  part.TopSurface=Enum.SurfaceType.Smooth;part.BottomSurface=Enum.SurfaceType.Smooth
  part.Transparency=spec.transparency or 0
  part.CFrame=CFrame.new(unpack(spec.pos))*CFrame.Angles(math.rad(spec.rot[1]),math.rad(spec.rot[2]),math.rad(spec.rot[3]))
  part.Parent=model
 end
 model:SetAttribute('ExpansionModel',rec.machineType)
 makePorts(model,rec)
end
'''
