"""Wall-scale utility bays fill the bare strips without touching plots or central ramps."""
import math
from .scene import Scene,prop

STEEL=(43,58,65); PALE=(133,142,137); SAND=(151,130,100)
DARK=(28,40,46); AMBER=(187,139,58); CYAN=(68,190,202)

def generate():
    s=Scene();root=s.world
    root.set('class','Folder');root.find("Properties/string[@name='Name']").text='PerimeterUtilities'
    for dx,dz,title in ((0,-1,'NORTE'),(0,1,'SUR'),(-1,0,'OESTE'),(1,0,'ESTE')):
        group=s.item(root,'Model','Wall'+title)
        tx,tz=dz,-dx
        rotation=(tx,0,dx,0,1,0,tz,0,dz)
        def at(u,y,r):return (tx*u+dx*r,y,tz*u+dz*r)
        def block(name,size,u,y,r,color=STEEL,material='Metal',collide=True):
            return s.part(group,name,size,at(u,y,r),color,material,rotation=rotation,collide=collide)
        def tube(name,a,b,width,color=PALE):
            return s.tube(group,name,at(*a),at(*b),width,color,'Metal',True)
        # West/east already contain energy, cooling, logistics, workshop and reservoirs.
        # Their new bays sit BEHIND that equipment, safely beyond the main pipe at r=500.
        centers=(-350,350) if dx else (-350,-170,170,350)
        if not dx:
            for lo,hi in ((-448,-45),(45,448)):
                block('ServiceWalk',(hi-lo,.4,10),(lo+hi)/2,-.05,459,PALE,'Concrete')
            for u in (-350,-170,-60,60,170,350):
                block('StreetConnection',(8,.3,32),u,-.07,459,PALE,'Concrete')
        for index,u in enumerate(centers):
            narrow=bool(dx);width=94 if narrow else 128
            front=513 if narrow else 474
            block('UtilityPad',(width,1,538-front),u,-.4,(538+front)/2,(110,110,101),'Concrete')
            block('WallCladding',(width-4,30,1.2),u,18,538.8,(83,93,96))
            for offset in (-width/2+1,width/2-1):
                block('WallPier',(3,38,5),u+offset,18.4,537.4,SAND,'Concrete')
                block('PierFoot',(6,2,8),u+offset,.5,535.8,STEEL)
            block('WallCornice',(width,2,5),u,36.4,537,PALE)
            block('CableTrunk',(width-8,1.5,2),u,32.5,536.5,AMBER)
            for offset in (-width/2+13,width/2-13):
                tube('ServiceRiser',(u+offset,1,535),(u+offset,31,535),1.6)
            # Broad wall-mounted louvers provide readable detail from the player's plot.
            vent_u=u-20 if not narrow else u
            block('VentHousing',(40,18,3),vent_u,20,535,STEEL)
            block('VentInset',(36,14,1),vent_u,20,533,DARK)
            for y in (14,17,20,23,26):block('VentSlat',(36,.8,1.5),vent_u,y,532.2,PALE)
            if narrow:
                block('UtilityCabinet',(26,9,12),u,4.6,522.5,PALE)
                block('CabinetDoor',(23,7,.4),u,4.7,516.3,DARK)
                for shift in (-7,7):block('Handle',(1,2,.5),u+shift,5,515.8,AMBER)
            elif dz<0:
                # Pump station with two vertical vessels and a short ground-level manifold.
                for shift in (-23,23):
                    tube('PumpVessel',(u+shift,.1,493),(u+shift,21,493),17,PALE)
                    for y in (2,18):tube('VesselCollar',(u+shift,y,493),(u+shift,y+1,493),18,STEEL)
                    tube('ValveNeck',(u+shift,8,493),(u+shift,8,480),2,AMBER)
                tube('PumpManifold',(u-23,4,493),(u+23,4,493),2.5,AMBER)
            else:
                # Service hatch and ground-level air handling unit; clearly decorative.
                block('ServiceHatch',(28,22,2),u+30,11.1,536.5,DARK)
                for y in range(3,22,3):block('HatchSlat',(26,.6,1),u+30,y,535.2,PALE)
                block('AirHandlingUnit',(40,10,22),u-18,5.1,492,(106,120,121))
                for shift in (-11,11):
                    tube('BlowerRim',(u-18+shift,10.1,492),(u-18+shift,12,492),16,STEEL)
                    tube('BlowerWell',(u-18+shift,12.01,492),(u-18+shift,12.15,492),13,DARK)
                    block('BlowerCross',(12,.3,1),u-18+shift,12.4,492,PALE,collide=False)
                    block('BlowerCross',(1,.3,12),u-18+shift,12.4,492,PALE,collide=False)
            sign=block('SectorPlate',(23,4,.4),u,29,532.8,DARK,collide=False)
            s.label(sign,f'{title} / {index+1:02d}',face=5,color=(210,220,215))
            fixture=block('WallLamp',(8,.8,2),u,34,534,(246,203,135),'Neon',False)
            light=s.item(fixture,'PointLight','PerimeterLight')
            prop(light,'Color3','Color',(255,216,165));prop(light,'float','Brightness',.65)
            prop(light,'float','Range',42);prop(light,'bool','Shadows',False)
            # Short cyan markers, not an outline around the whole wall.
            block('StatusStrip',(3,.5,.4),u+16,29,532.8,CYAN,'Neon',False)
    for item in root.iter('Item'):
        item.set('referent',item.get('referent').replace('RBX_CANYON_','RBX_PERIM817_'))
    return root
