"""Low industrial scenery for the west/east service strips; gameplay stays in plots."""
import math
from .scene import Scene,prop
from .canyon import yaw

STEEL=(41,55,62); METAL=(104,118,120); CONCRETE=(107,106,96)
CYAN=(68,190,202); AMBER=(191,139,57); DARK=(27,38,43)

def generate():
    s=Scene();root=s.world
    root.set('class','Folder');root.find("Properties/string[@name='Name']").text='SideDistricts'
    paths=s.item(root,'Folder','ServiceWalkways')
    def part(parent,name,size,at,color=STEEL,material='Metal',**kwargs):
        return s.part(parent,name,size,at,color,material,**kwargs)
    def tube(parent,name,a,b,d,color=METAL,material='Metal',collide=True):
        return s.tube(parent,name,a,b,d,color,material,collide)
    def plaque(parent,side,z,title):
        # Mounted on the retaining wall, facing the campus; no floating labels.
        panel=part(parent,'WallIdentity',(1,12,60),(side*538,22,z),DARK)
        s.label(panel,title,0 if side<0 else 3,color=(207,219,215))
        for end in (-31,31):
            part(parent,'PanelFrame',(1.2,15,1.5),(side*537.8,22,z+end),METAL)
        part(parent,'PanelAccent',(.35,.35,54),(side*537.3,29,z),CYAN,'Neon',collide=False)
    def pad(parent,side,z):
        part(parent,'ServiceFoundation',(56,1,154),(side*502,-.4,z),CONCRETE,'Concrete')
        for offset in (-76,76):
            part(parent,'PadEdge',(54,.12,.45),(side*502,.18,z+offset),AMBER,collide=False)
        for offset in (-68,68):
            part(parent,'SafetyBollard',(1.5,3,1.5),(side*474,1.6,z+offset),AMBER)
            part(parent,'BollardCap',(1.7,.2,1.7),(side*474,3.2,z+offset),DARK)
    def cabinet(parent,side,z):
        part(parent,'ControlCabinet',(12,8,10),(side*484,4.1,z),METAL)
        part(parent,'CabinetScreen',(.2,2,5),(side*477.9,5,z),DARK,collide=False)
        part(parent,'StatusLamp',(.25,.4,1.3),(side*477.7,6.4,z-1.4),CYAN,'Neon',collide=False)
        for offset in (-2,0,2):
            part(parent,'CabinetVent',(.15,.35,5),(side*477.8,2.5+offset*.35,z),DARK,collide=False)
    for side in (-1,1):
        for lo,hi in ((-448,-45),(45,448)):
            part(paths,'ServiceWalk',(10,.4,hi-lo),(side*459,-.05,(lo+hi)/2),CONCRETE,'Concrete')
            part(paths,'WalkEdge',(.25,.04,hi-lo),(side*454.4,.19,(lo+hi)/2),(177,174,153),'SmoothPlastic',collide=False)
        for z in (-400,-190,-60,60,190,400):
            part(paths,'StreetConnection',(32,.3,8),(side*459,-.07,z),CONCRETE,'Concrete')

    power=s.item(root,'Model','WestEnergy');pad(power,-1,-190);plaque(power,-1,-190,'ENERGÍA   /   01')
    for z in (-230,-190,-150):
        part(power,'TransformerFoot',(22,1.4,28),(-516,.8,z),DARK)
        part(power,'TransformerBody',(16,10,22),(-516,6.5,z),(88,105,111))
        for rib in range(-8,9,4):
            part(power,'CoolingFin',(20,7,.7),(-516,6,z+rib),METAL)
        part(power,'TopPlate',(19,1,25),(-516,12,z),STEEL)
        for offset in (-6,6):
            tube(power,'Insulator',(-516,12.5,z+offset),(-516,18,z+offset),2.2,AMBER)
            for y in (14,15.5,17):tube(power,'InsulatorRing',(-516,y,z+offset),(-516,y+.5,z+offset),3.2,STEEL)
        tube(power,'ConduitConnection',(-500,9,z),(-506,9,z),1.5,AMBER)
    for z in (-242,-138):cabinet(power,-1,z)

    cooling=s.item(root,'Model','WestCooling');pad(cooling,-1,190);plaque(cooling,-1,190,'REFRIGERACIÓN   /   02')
    for z in (150,190,230):
        tube(cooling,'FanHousing',(-516,.1,z),(-516,12,z),22,METAL)
        tube(cooling,'FanRim',(-516,12,z),(-516,13,z),23,STEEL)
        tube(cooling,'FanWell',(-516,13.01,z),(-516,13.1,z),19,DARK,collide=False)
        tube(cooling,'FanHub',(-516,13.1,z),(-516,13.8,z),3.4,METAL,collide=False)
        for angle in (0,math.pi/2,math.pi,math.pi*1.5):
            part(cooling,'FanBlade',(6,.3,2.5),(-516+math.cos(angle)*4.3,13.4,z+math.sin(angle)*4.3),
                 (142,151,147),rotation=yaw(-angle),collide=False)
        tube(cooling,'CoolingConnection',(-500,8,z),(-505,8,z),1.5,CYAN)
    cabinet(cooling,-1,120)
    for z in (137,243):
        tube(cooling,'PressureVessel',(-483,.1,z),(-483,10,z),8,(121,137,139))
        tube(cooling,'VesselBand',(-483,6,z),(-483,6.6,z),8.6,STEEL)

    cargo=s.item(root,'Model','EastLogistics');pad(cargo,1,-190);plaque(cargo,1,-190,'LOGÍSTICA   /   03')
    for z,length,color in ((-204,58,(148,104,63)),(-144,36,(74,99,108))):
        part(cargo,'FreightContainer',(22,16,length),(516,8.1,z),color)
        part(cargo,'ContainerRoof',(23,1,length+1),(516,16.6,z),STEEL)
        for offset in range(-int(length/2)+4,int(length/2),6):
            part(cargo,'ContainerRib',(.5,14,.6),(504.7,8.3,z+offset),METAL)
        for end in (-1,1):
            part(cargo,'ContainerCorner',(24,1.1,1),(516,.65,z+end*length/2),STEEL)
        for offset in (-3,3):
            part(cargo,'DoorLatch',(.7,11,.45),(504.2,7,z+offset),DARK)
    for z in (-245,-182,-134):
        part(cargo,'Pallet',(14,.8,14),(483,.5,z),(116,91,60),'Wood')
        for offset in (-3.2,3.2):
            part(cargo,'CargoCrate',(5.8,6,11),(483+offset,3.9,z),(153,133,94))
            for stripe in (-3,3):
                part(cargo,'CrateStrap',(6,.4,.5),(483+offset,7.05,z+stripe),STEEL,collide=False)
    # A short loading gantry supplies a distinct silhouette below terrace height.
    for x in (472,528):
        part(cargo,'GantryColumn',(2.5,25,3),(x,12.5,-220),AMBER)
        part(cargo,'GantryFoot',(5,1,6),(x,.6,-220),STEEL)
    part(cargo,'GantryBeam',(59,2.5,5),(500,25,-220),AMBER)
    part(cargo,'HoistMotor',(8,3,7),(484,27.2,-220),STEEL)
    tube(cargo,'HoistCable',(484,24,-220),(484,16,-220),.28,STEEL,collide=False)
    part(cargo,'HoistHook',(2,1.7,.6),(484,15.5,-220),METAL,collide=False)

    shop=s.item(root,'Model','EastMaintenance');pad(shop,1,190);plaque(shop,1,190,'MANTENIMIENTO   /   04')
    part(shop,'WorkshopBody',(20,14,74),(484,7.1,190),(91,103,108),'Concrete')
    part(shop,'WorkshopRoof',(25,1.2,80),(483,14.7,190),STEEL)
    part(shop,'ShutterDoor',(.4,10,24),(473.7,5.5,190),DARK)
    for y in range(2,11,2):part(shop,'ShutterSlat',(.2,.3,23),(473.4,y,190),METAL,collide=False)
    for z in (176,204):part(shop,'DoorJamb',(.8,12,1.2),(473.3,6,z),AMBER)
    part(shop,'WorkshopWindow',(.3,4,12),(473.6,8,216),(52,111,122),'Glass')
    tube(shop,'ExtractionDuct',(490,15,216),(490,24,216),3,METAL)
    tube(shop,'DuctCap',(490,24,216),(490,25,216),5,STEEL)
    part(shop,'ToolRack',(16,6,28),(518,3.1,190),STEEL)
    for z in (180,190,200):
        part(shop,'ToolChest',(12,3.5,7),(518,5,z),AMBER)
        part(shop,'ChestHandle',(.3,.5,4),(511.8,5,z),METAL,collide=False)
    for z in (240,251):
        tube(shop,'ServiceDrum',(516,.1,z),(516,6,z),7,(113,131,132))
        for y in (1,5):tube(shop,'DrumBand',(516,y,z),(516,y+.5,z),7.4,STEEL)

    for item in root.iter('Item'):item.set('referent',item.get('referent').replace('RBX_CANYON_','RBX_SIDES816_'))
    return root
