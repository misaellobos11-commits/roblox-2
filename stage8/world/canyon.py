"""Editable sandstone campus inspired by the user's reference; no external assets."""
import math
import random
from .scene import Scene, prop

SLOTS = [(-280,-280,0,1),(0,-280,0,1),(280,-280,0,1),
         (-280,0,1,0),(280,0,-1,0),
         (-280,280,0,-1),(0,280,0,-1),(280,280,0,-1)]
CYAN=(58,221,235); STEEL=(37,55,65); SAND=(172,129,85)
GOLD=(187,139,58); PALE=(204,191,163); ROAD=(49,57,63)


def yaw(a):
    c,s=math.cos(a),math.sin(a)
    return (c,0,s,0,1,0,-s,0,c)


def generate():
    s=Scene(); w=s.world; rng=random.Random(812)
    groups={name:s.item(w,'Folder',name) for name in
            ('Landscape','Roads','Plaza','PlotSurrounds','PreviewPlots','Infrastructure','Vegetation')}
    def block(group,name,size,pos,color=STEEL,material='Metal',**kw):
        return s.part(groups[group],name,size,pos,color,material,**kw)
    def beam(group,name,a,b,width,color=STEEL,material='Metal',collide=False):
        return s.tube(groups[group],name,a,b,width,color,material,collide)
    def disc(group,name,x,y,z,diameter,thickness,color,material='Metal',collide=True):
        return beam(group,name,(x,y-thickness/2,z),(x,y+thickness/2,z),diameter,color,material,collide)
    def ring(group,name,r,y,width,color,material='Metal',segments=64):
        for i in range(segments):
            a=math.tau*i/segments;b=math.tau*(i+1)/segments
            beam(group,name,(r*math.cos(a),y,r*math.sin(a)),
                 (r*math.cos(b),y,r*math.sin(b)),width,color,material)
    def lamp(x,z,height=12,base=0,lit=False):
        block('Infrastructure','LampBase',(2.5,.7,2.5),(x,base+.35,z))
        block('Infrastructure','LampPost',(1,height,1),(x,base+height/2,z))
        bulb=block('Infrastructure','CyanLantern',(1.4,2.5,1.4),(x,base+height-1.2,z),CYAN,'Neon',collide=False)
        block('Infrastructure','LampCap',(2.4,.3,2.4),(x,base+height+.2,z))
        if lit:
            light=s.item(bulb,'PointLight','LampLight')
            prop(light,'Color3','Color',(151,219,228));prop(light,'float','Brightness',.5)
            prop(light,'float','Range',22);prop(light,'bool','Shadows',False)

    block('Landscape','DesertFloor',(1800,12,1800),(0,-6.6,0),SAND,'Sand')
    # Asphalt network encloses all eight building sites; continuous, walkable pavement.
    for coordinate in (-420,-140,140,420):
        for axis in ('X','Z'):
            horizontal=axis=='X'
            def pos(a,y,b):return (a,y,b) if horizontal else (b,y,a)
            def size(a,y,b):return (a,y,b) if horizontal else (b,y,a)
            spans=((-448,-436),(-404,-156),(-124,124),(156,404),(436,448))
            sidewalk_spans=spans if horizontal else ((-448,-443),(-397,-163),(-117,117),(163,397),(443,448))
            for side in (-1,1):
                for low,high in sidewalk_spans:
                    block('Roads','Sidewalk'+axis,size(high-low,.8,7),pos((low+high)/2,-.2,coordinate+side*19.5),PALE,'Concrete')
            road_spans=((-448,448),) if horizontal else ((-448,-436),(-404,-156),(-124,124),(156,404),(436,448))
            for low,high in road_spans:
                block('Roads','Boulevard'+axis,size(high-low,.4,32),pos((low+high)/2,-.2,coordinate),ROAD,'Asphalt')
            for offset in range(-432,433,24):
                if any(abs(offset-c)<25 for c in (-420,-140,140,420)):continue
                block('Roads','LaneDash',size(9,.025,.35),pos(offset,.025,coordinate),PALE,'SmoothPlastic',collide=False)
            for edge in (-14.5,14.5):
                for low,high in spans:
                    block('Roads','EdgeLine',size(high-low,.024,.28),pos((low+high)/2,.024,coordinate+edge),PALE,'SmoothPlastic',collide=False)
            for offset in (-365,-245,-85,85,245,365):
                lamp(*( (offset,coordinate+20) if horizontal else (coordinate-20,offset)))
    for x in (-140,140):
        for z in (-140,140):
            for k in range(-5,6):
                for side in (-1,1):
                    block('Roads','Crosswalk',(1.5,.035,7),(x+k*2.5,.04,z+side*25),PALE,'SmoothPlastic',collide=False)
                    block('Roads','Crosswalk',(7,.035,1.5),(x+side*25,.04,z+k*2.5),PALE,'SmoothPlastic',collide=False)
    # Ring road and paths meet the grid, leaving the middle as a pedestrian plaza.
    disc('Plaza','Roundabout',0,-.25,0,248,.5,ROAD,'Asphalt')
    disc('Plaza','PlazaDeck',0,.05,0,190,.3,PALE,'Concrete')
    disc('Plaza','PlazaInset',0,.24,0,170,.08,(87,101,108),'Slate')
    ring('Plaza','TrafficRing',111,.03,.4,PALE,'SmoothPlastic')
    ring('Plaza','DeckTrim',92,.3,.45,CYAN,'Neon')
    ring('Plaza','InnerInlay',68,.3,.35,(176,163,128),'Metal')
    for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
        block('Roads','HubLink',(56 if dx else 24,.4,56 if dz else 24),(dx*111,-.16,dz*111),ROAD,'Asphalt')
        block('Plaza','RadialWalk',(70 if dx else 18,.3,70 if dz else 18),(dx*58,.22,dz*58),PALE,'Concrete')
        for side in (-1,1):
            lamp(dx*74+dz*side*14,dz*74+dx*side*14,lit=True)
    # Low steps and a tall, open synthesis core establish a readable focal point.
    for diameter,y,thickness in ((76,.45,.4),(64,.8,.3),(52,1.15,.4)):
        disc('Plaza','ReactorStep',0,y,0,diameter,thickness,STEEL)
    ring('Plaza','ReactorHalo',28,1.35,.7,CYAN,'Neon',48)
    disc('Plaza','CoreFoot',0,2.2,0,22,1.8,(75,89,97))
    beam('Plaza','SynthesisCore',(0,3.1,0),(0,54,0),3.6,CYAN,'Neon')
    for a in (0,math.pi/2,math.pi,math.pi*1.5):
        x,z=math.cos(a)*12,math.sin(a)*12
        h=57 if x>1 else 46
        block('Plaza','ReactorFin',(3.5,h,5),(x,h/2+2,z),STEEL,rotation=yaw(-a))
        block('Plaza','FinLight',(1,h-6,5.15),(x,h/2+3,z),CYAN,'Neon',rotation=yaw(-a),collide=False)
        block('Plaza','FinCap',(5,2,7),(x,h+2,z),(119,133,138),rotation=yaw(-a))
    for y,r in ((8,15),(22,10),(37,8)):
        ring('Plaza','CoreCollar',r,y,.8,(122,146,150),segments=32)
    for x,z in ((-48,-48),(48,-48),(-48,48),(48,48)):
        disc('Plaza','Planter',x,.8,z,17,1.2,STEEL)
        disc('Plaza','PlanterSand',x,1.45,z,14,.15,SAND,'Sand')
        for sign in (-1,1):
            block('Plaza','Bench',(12,1.1,3),(x,1,z+sign*13),(121,107,83))
    spawn=s.part(groups['Plaza'],'MatterloomLobbySpawn',(9,.5,9),(0,.55,48),(86,115,125),'Metal',kind='SpawnLocation')
    prop(spawn,'bool','Neutral',True);prop(spawn,'float','Duration',0)
    block('Plaza','ArrivalGuide',(9,.08,.35),(0,.85,52),CYAN,'Neon',collide=False)

    # Preview floors are removed before the server creates its authoritative plots.
    for slot,(x,z,dx,dz) in enumerate(SLOTS,1):
        model=s.item(groups['PreviewPlots'],'Model',f'PlotSlot_{slot}')
        s.part(model,'BuildFloor',(192,1,192),(x,-.5,z),(82,91,99),'Concrete')
        block('PlotSurrounds','PlatformFoundation',(202,1.3,202),(x,-.95,z),(69,78,84),'Concrete')
        for i in range(49):
            offset=-96+i*4
            col=(106,118,123) if i%4==0 else (93,103,110)
            for size,pos in (((.045,.014,192),(x+offset,.014,z)),((192,.014,.045),(x,.014,z+offset))):
                s.part(model,'Grid',size,pos,col,'SmoothPlastic',collide=False)
        for sign in (-1,1):
            s.part(model,'Border',(192,.18,.55),(x,.1,z+sign*96),CYAN,'Neon',collide=False)
            s.part(model,'Border',(.55,.18,192),(x+sign*96,.1,z),CYAN,'Neon',collide=False)
        block('PlotSurrounds','GateWalk',(42 if dx else 28,.6,42 if dz else 28),
              (x+dx*116,-.25,z+dz*116),PALE,'Concrete')
        for tangent in (-17,17):
            bx,bz=x+dx*103+dz*tangent,z+dz*103-dx*tangent
            lamp(bx,bz,7)
        # Corner markers, service box and a banner never enter the 192-stud build floor.
        for ax,az in ((-102,-102),(-102,102),(102,-102),(102,102)):
            block('PlotSurrounds','CornerPedestal',(3,2.5,3),(x+ax,1, z+az))
            block('PlotSurrounds','CornerBeacon',(2,.4,2),(x+ax,2.5,z+az),CYAN,'Neon',collide=False)
        bx,bz=x+dx*108+dz*37,z+dz*108-dx*37
        block('Infrastructure','BannerMast',(1,24,1),(bx,12,bz))
        flag=block('Infrastructure','PlotBanner',(7,12,.45),(bx+3,18,bz),STEEL,collide=False)
        for face in (2,5):s.label(flag,f'{slot:02d}\nM',face,color=CYAN)
        block('Infrastructure','ServiceCabinet',(7,4,4),(bx,2,bz+5),(100,107,106))

    # Four gently sloping ramps connect the street to the raised service terraces.
    for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
        block('Landscape','Terrace',(1100 if dz else 100,42,1100 if dx else 100),
              (dx*590,19,dz*590),(151,116,81),'Sandstone')
        block('Infrastructure','RimWalk',(1100 if dz else 22,1,1100 if dx else 22),
              (dx*558,40,dz*558),PALE,'Concrete')
        # Reach y=40 at the inner terrace face (r=540), before the raised rim walk.
        rise,run=40,100; length=math.hypot(rise,run);mid=490
        # Basis: width tangent to the rim, thickness normal to the slope, length up-slope.
        tangent=(dz,0,-dx); up=(-dx*rise/length,run/length,-dz*rise/length)
        forward=(dx*run/length,rise/length,dz*run/length)
        rot=tuple(v for i in range(3) for v in (tangent[i],up[i],forward[i]))
        block('Infrastructure','AccessRamp',(22,.6,length),(dx*mid,20,dz*mid),ROAD,'Asphalt',rotation=rot)
        for sign in (-1,1):
            a=(dx*440+dz*sign*12,2.3,dz*440-dx*sign*12)
            b=(dx*540+dz*sign*12,42.3,dz*540-dx*sign*12)
            beam('Infrastructure','RampRail',a,b,.5,STEEL,collide=True)
            beam('Infrastructure','RampGuide',(a[0],a[1]-.9,a[2]),(b[0],b[1]-.9,b[2]),.24,CYAN,'Neon')
        for offset in range(-500,501,80):
            lamp(dx*558+dz*offset,dz*558+dx*offset,10,40)
        # Inner railing leaves an opening at the ramp and stands outside the walking strip.
        for low,high in ((-540,-17),(17,540)):
            for height in (41,43):
                beam('Infrastructure','RimRail',(dx*545+dz*low,height,dz*545+dx*low),
                     (dx*545+dz*high,height,dz*545+dx*high),.55,STEEL,collide=True)
        for offset in range(-520,521,40):
            if abs(offset)<17:continue
            beam('Infrastructure','RimPost',(dx*545+dz*offset,40,dz*545+dx*offset),
                 (dx*545+dz*offset,43.4,dz*545+dx*offset),.65,STEEL,collide=True)

    # Faceted layered cliffs: tall enough to frame the campus, with irregular skyline.
    for side in range(4):
        for along in range(-735,736,90):
            depth=rng.uniform(675,735);height=rng.uniform(85,190)
            x,z=((along,depth),(depth,along),(along,-depth),(-depth,along))[side]
            for layer in range(3):
                h=height/3; y=layer*h
                width=rng.uniform(105,155)*(1-layer*.12)
                block('Landscape','SandstoneMesa',(width,h,118-layer*14),(x+layer*3,y+h/2-8,z),
                      ((151,109,76),(178,132,88),(194,151,104))[layer],'Sandstone',rotation=yaw(rng.uniform(-.3,.3)))
            # Staggered buttresses break up the regular block silhouettes.
            block('Landscape','CliffButtress',(rng.uniform(24,40),height*.8,38),(x-30,height*.32,z-25),
                  (146,105,74),'Rock',rotation=yaw(rng.uniform(-.5,.5)),kind='WedgePart')
    # Broken rock shoulders disguise the perfectly straight terrace retaining face.
    for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
        for along in range(-505,506,43):
            if abs(along)<35:continue
            h=rng.uniform(19,36)
            block('Landscape','TerraceOutcrop',(rng.uniform(18,28),h,rng.uniform(22,38)),
                  (dx*537+dz*along,h/2-1,dz*537+dx*along),(149,111,75),'Sandstone',
                  rotation=yaw(rng.uniform(-.6,.6)),kind='WedgePart')
    # Service buildings on the rim, with ribbed facades, bright doors and roof machinery.
    for x,z in ((-350,-590),(350,-590),(-350,590),(350,590)):
        toward=-1 if z>0 else 1
        block('Infrastructure','ServiceHall',(116,34,56),(x,57,z),(75,87,92),'Concrete')
        block('Infrastructure','RoofCornice',(124,2,64),(x,75,z),STEEL)
        for xx in (-50,-25,0,25,50):
            block('Infrastructure','FacadeRib',(3,36,3),(x+xx,58,z+toward*29),(131,140,139))
        block('Infrastructure','MainDoor',(25,24,1),(x,52,z+toward*28.5),STEEL)
        for xx in (-15,15):
            block('Infrastructure','DoorLight',(1.1,23,.5),(x+xx,53,z+toward*30),CYAN,'Neon',collide=False)
        for xx,h in ((-38,45),(36,57)):
            block('Infrastructure','Tower',(14,h,16),(x+xx,76+h/2,z),(113,123,125))
            block('Infrastructure','TowerCap',(17,2,19),(x+xx,76+h,z),STEEL)
            beam('Infrastructure','Antenna',(x+xx,76+h,z),(x+xx,92+h,z),.65)
            block('Infrastructure','TowerInset',(3,h-8,.4),(x+xx,77+h/2,z+toward*8.3),CYAN,'Neon',collide=False)
        for xx in (-18,18):
            disc('Infrastructure','RoofVent',x+xx,78,z,12,4,(119,131,132))
    for sign in (-1,1):
        for z in (-330,330):
            x=sign*485
            block('Infrastructure','TankBase',(35,1,70),(x,0,z),(106,109,105),'Concrete')
            for offset in (-18,18):
                beam('Infrastructure','Reservoir',(x,1,z+offset),(x,25,z+offset),22,(155,160,150),collide=True)
                for y in (3,23):beam('Infrastructure','TankCollar',(x,y,z+offset),(x,y+1,z+offset),23,STEEL)
        # Overhead pipes track the outer edge, outside circulation and build sites.
        beam('Infrastructure','MainPipe',(sign*500,10,-480),(sign*500,10,480),5,(139,120,85),collide=True)
        for z in range(-460,461,40):
            beam('Infrastructure','PipeSleeve',(sign*500,10,z-1),(sign*500,10,z+1),6,STEEL)
            block('Infrastructure','PipeSupport',(8,9,3),(sign*500,4,z),(87,91,85),'Concrete')

    def tree(x,z):
        h=rng.uniform(13,21)
        beam('Vegetation','AcaciaTrunk',(x,-.4,z),(x+1,h*.8,z),1.7,(94,72,47),'Wood',True)
        for a in (0,2.1,4.2):
            bx,bz=x+math.cos(a)*5,z+math.sin(a)*5
            beam('Vegetation','AcaciaBranch',(x,h*.5,z),(bx,h,bz),.8,(94,72,47),'Wood')
            block('Vegetation','DryCanopy',(13,3.2,11),(bx,h,bz),(119,107,47),'SmoothPlastic',shape=0,collide=False)
            block('Vegetation','SunlitCanopy',(9,2.5,9),(bx+1,h+1.3,bz),(157,133,56),'SmoothPlastic',shape=0,collide=False)
    for i,(x,z,dx,dz) in enumerate(SLOTS):
        # Planted strips are outside the build floor and clear of the chosen entrance.
        for side in (-1,1):
            for along in (-78,-54,-30,30,54,78):
                px,pz=x+along,z+side*109
                if dz==side and abs(along)<30:continue
                r=rng.uniform(1.6,3.2)
                block('Vegetation','SandstoneFragment',(r*2,r,r*1.6),(px,r*.2,pz),(137,110,79),'Rock',rotation=yaw(rng.random()*6.28),kind='WedgePart',collide=False)
                for angle in (0,2.1,4.2):
                    block('Vegetation','DryGrass',(.35,2.3,2.8),(px+4,1,pz),GOLD,'SmoothPlastic',rotation=yaw(angle),kind='WedgePart',collide=False)
        tree(x-108,z-108)
        if i%2==0:tree(x+108,z+108)
        for ax,az in ((-111,105),(108,-110)):
            for n in range(3):
                h=rng.uniform(2,5)
                block('Vegetation','CornerRocks',(rng.uniform(4,7),h,rng.uniform(4,7)),
                      (x+ax+n*2,h*.4,z+az+n),(146,117,80),'Rock',
                      rotation=yaw(rng.uniform(0,6)),kind='WedgePart',collide=False)
    return s


def config_source():
    slots=',\n'.join(f'    {{x={x},z={z},dx={dx},dz={dz}}}' for x,z,dx,dz in SLOTS)
    return '''--!strict
-- Generated from stage8/world/canyon.py; plot coordinates and entry direction share one source.
local MapConfig={PLOT_SIZE=192,MAX_PLOTS=8,PLAZA_CENTER=Vector3.new(0,0,0)}
local slots={
'''+slots+'''
}
local function slotInfo(slot: number)
    assert(slot%1==0 and slot>=1 and slot<=#slots,'Parcela fuera de rango')
    return slots[slot]
end
function MapConfig.plotCenter(slot: number): Vector3
    local p=slotInfo(slot);return Vector3.new(p.x,0,p.z)
end
function MapConfig.plotOrigin(slot: number): Vector3
    return MapConfig.plotCenter(slot)-Vector3.new(96,0,96)
end
function MapConfig.entryDirection(slot: number): Vector3
    local p=slotInfo(slot);return Vector3.new(p.dx,0,p.dz)
end
function MapConfig.entryPoint(slot: number): Vector3
    return MapConfig.plotCenter(slot)+MapConfig.entryDirection(slot)*109
end
return MapConfig
'''
