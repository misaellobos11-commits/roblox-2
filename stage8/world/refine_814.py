"""Replace box cliffs with original faceted rock geometry and calm the vacant plots."""
import math
import random
from .scene import prop

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,n):return tuple(x*n for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):return scale(a,1/math.sqrt(dot(a,a)))

def triangle(scene,parent,vertices,color):
    # Split along the altitude to the longest edge into two right triangular prisms.
    a,b,c=vertices
    if dot(sub(c,b),sub(c,b))>dot(sub(b,a),sub(b,a)):a,b,c=b,c,a
    if dot(sub(a,c),sub(a,c))>dot(sub(b,a),sub(b,a)):a,b,c=c,a,b
    axis=unit(sub(b,a));foot=add(a,scale(axis,dot(sub(c,a),axis)))
    height=math.sqrt(dot(sub(c,foot),sub(c,foot)));up=unit(sub(c,foot))
    for endpoint in (a,b):
        base=math.sqrt(dot(sub(foot,endpoint),sub(foot,endpoint)))
        if base<1e-5:continue
        forward=unit(sub(foot,endpoint));right=cross(up,forward)
        rotation=tuple(v for i in range(3) for v in (right[i],up[i],forward[i]))
        scene.part(parent,'RockFacet',(.18,height,base),scale(add(endpoint,c),.5),color,
                   'Sandstone',rotation,False,kind='WedgePart')

def rock(scene,parent,center,size,rng,coarse=False):
    phi=(1+math.sqrt(5))/2
    if coarse:
        vertices=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
        faces=[(0,2,4),(4,2,1),(1,2,5),(5,2,0),(0,4,3),(4,1,3),(1,5,3),(5,0,3)]
    else:
        vertices=[(-1,phi,0),(1,phi,0),(-1,-phi,0),(1,-phi,0),(0,-1,phi),(0,1,phi),
                  (0,-1,-phi),(0,1,-phi),(phi,0,-1),(phi,0,1),(-phi,0,-1),(-phi,0,1)]
        faces=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),
               (11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),
               (4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    angle=rng.uniform(-math.pi,math.pi);cs,sn=math.cos(angle),math.sin(angle)
    transformed=[]
    for v in vertices:
        v=scale(unit(v),rng.uniform(.88,1.12))
        x,y,z=(v[i]*size[i]/2 for i in range(3))
        transformed.append(add(center,(x*cs+z*sn,y,-x*sn+z*cs)))
    base=rng.choice(((167,111,70),(184,130,82),(155,104,68),(197,143,92)))
    for face in faces:
        tint=rng.uniform(.92,1.07)
        triangle(scene,parent,[transformed[i] for i in face],tuple(min(255,round(v*tint)) for v in base))
    hull=scene.part(parent,'RockCollision',tuple(v*.69 for v in size),center,base,'Rock',shape=0)
    prop(hull,'float','Transparency',1)
    # Collision remains available at the distant perimeter; selection rays ignore it.
    hull.find("Properties/bool[@name='CanQuery']").text='false'

def refine(scene):
    world=scene.world
    def name(i):return i.findtext("Properties/string[@name='Name']")
    landscape=next(i for i in world if i.tag=='Item' and name(i)=='Landscape')
    for item in list(landscape):
        if item.tag=='Item' and name(item) in ('SandstoneMesa','CliffButtress','TerraceOutcrop'):landscape.remove(item)
    rng=random.Random(814)
    mountains=scene.item(landscape,'Folder','CanyonRockFormations')
    for side in range(4):
        for along in range(-700,701,140):
            along+=rng.uniform(-34,34);depth=rng.uniform(748,815);h=rng.uniform(120,240)
            x,z=((along,depth),(depth,along),(along,-depth),(-depth,along))[side]
            rock(scene,mountains,(x,h*.37-8,z),(rng.uniform(155,220),h,rng.uniform(135,205)),rng)
    # Low irregular talus, with broad gaps around ramps and below the upper walkway.
    for dx,dz in ((1,0),(-1,0),(0,1),(0,-1)):
        for along in range(-490,491,90):
            if abs(along)<50:continue
            along+=rng.uniform(-12,12);h=rng.uniform(23,38)
            rock(scene,mountains,(dx*532+dz*along,h*.35-1,dz*532+dx*along),
                 (rng.uniform(30,49),h,rng.uniform(31,48)),rng,True)
    # Keep editor preview floors, but remove their fine grids and dim unclaimed edges.
    preview=next(i for i in world if i.tag=='Item' and name(i)=='PreviewPlots')
    for plot in preview.findall('Item'):
        for p in list(plot):
            if p.tag!='Item':continue
            if name(p)=='Grid':plot.remove(p)
            elif name(p)=='Border':
                p.find("Properties/token[@name='Material']").text='1088'
                p.find("Properties/Color3uint8[@name='Color3uint8']").text=str(48*65536+97*256+102)
    return scene
