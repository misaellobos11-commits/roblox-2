"""Connected sandstone escarpment, with broad strata instead of scattered boulders."""
import math
from .scene import Scene,prop
from .refine_814 import triangle


def generate():
    s=Scene();root=s.world
    root.set('class','Folder');root.find("Properties/string[@name='Name']").text='StratifiedCanyon'
    colors=((137,108,81),(158,125,91),(181,145,104))
    tops=(174,174,151,151,199,199,164,148,182,182,161,174)
    for side,(dx,dz) in enumerate(((1,0),(0,1),(-1,0),(0,-1))):
        group=s.item(root,'Model',f'Escarpment_{side+1}')
        def at(u,y,r):return (dz*u+dx*r,y,-dx*u+dz*r)
        def quad(points,color):
            triangle(s,group,[points[0],points[1],points[2]],color)
            triangle(s,group,[points[0],points[2],points[3]],color)
        # Buried foot joins every segment and adjacent sides, before the terrace ends.
        size=(228,66,1536) if dx else (1536,66,228)
        s.part(group,'BedrockFoot',size,at(0,32,746),colors[0],'Sandstone')
        profiles=[]
        for j in range(12):
            u=-704+j*128
            wave=math.sin(j*1.7+side*.9)
            profiles.append([(u,-1,628+3*math.sin(j+side)),
                (u,77+5*wave,644+14*math.sin(j*.8+side)),
                (u,123+7*wave,680+20*math.sin(j+side*.7)),
                (u,tops[(j+side*2)%12]+side*3,728+24*math.sin(j*.8+side))])
        for j in range(11):
            a,b=profiles[j],profiles[j+1]
            for layer in range(3):
                quad([at(*a[layer]),at(*b[layer]),at(*b[layer+1]),at(*a[layer+1])],colors[layer])
            # Broad mesa crown, varied skyline; continues behind the escarpment.
            quad([at(*a[3]),at(*b[3]),at(b[3][0],b[3][1],870),at(a[3][0],a[3][1],870)],(187,154,113))
            for layer in (1,2):
                x,y,r=a[layer];xx,yy,rr=b[layer]
                quad([at(x,y-.8,r-.35),at(xx,yy-.8,rr-.35),
                      at(xx,yy+1.4,rr+.4),at(x,y+1.4,r+.4)],(121,96,75))
        # Eroded spurs grow out of the cliff, breaking the long horizontal bands.
        # Tapered faces remain attached to the wall rather than becoming loose boulders.
        for u in (-480,-120,330):
            levels=((-1,632,72),(84,635,62),(151+side*4,681,36))
            for layer in range(2):
                y0,r0,w0=levels[layer];y1,r1,w1=levels[layer+1]
                quad([at(u-w0/2,y0,r0),at(u+w0/2,y0,r0),
                      at(u+w1/2,y1,r1),at(u-w1/2,y1,r1)],colors[layer])
                for sign in (-1,1):
                    quad([at(u+sign*w0/2,y0,r0),at(u+sign*w0/2,y0,r0+55),
                          at(u+sign*w1/2,y1,r1+55),at(u+sign*w1/2,y1,r1)],colors[layer])
            y,r,w=levels[-1]
            quad([at(u-w/2,y,r),at(u+w/2,y,r),at(u+w/2,y,r+55),at(u-w/2,y,r+55)],colors[2])
        # Backstop behind the scenery: no void falls even if a player reaches a mesa top.
        size=(8,700,1784) if dx else (1784,700,8)
        barrier=s.part(group,'OuterSafetyBoundary',size,at(0,250,884),(90,90,90),'SmoothPlastic')
        prop(barrier,'float','Transparency',1)
        barrier.find("Properties/bool[@name='CanQuery']").text='false'
        prop(barrier,'bool','CastShadow',False)
    for item in root.iter('Item'):
        if item.findtext("Properties/string[@name='Name']")=='RockFacet':
            item.find("Properties/string[@name='Name']").text='StratumFace'
            # The visible rock skin is solid; the outer boundary is only a final backstop.
            item.find("Properties/bool[@name='CanCollide']").text='true'
            item.find("Properties/bool[@name='CanQuery']").text='true'
        item.set('referent',item.get('referent').replace('RBX_CANYON_','RBX_HORIZON819_'))
    return root
