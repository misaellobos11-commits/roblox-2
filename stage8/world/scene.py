"""Small deterministic Roblox XML scene writer for the stage-8 canyon."""
import math
import xml.etree.ElementTree as ET
MATERIAL = {'SmoothPlastic':272,'Neon':288,'Slate':800,'Concrete':816,
            'Rock':896,'DiamondPlate':1056,'Metal':1088,'Sand':1296,'Asphalt':1376,'Glass':1568,'Wood':512,'Sandstone':912}
CYAN=(78,211,221)
AMBER=(221,166,61)
STEEL=(63,76,86)
CONCRETE=(104,107,107)
IDENTITY=(1,0,0,0,1,0,0,0,1)


def number(value):
    return format(value,'.9g')


def prop(item, kind, name, value):
    properties=item.find('Properties')
    node=ET.SubElement(properties,kind,{'name':name})
    if kind=='Vector3':
        for axis,coordinate in zip(('X','Y','Z'),value): ET.SubElement(node,axis).text=number(coordinate)
    elif kind=='CoordinateFrame':
        for axis,coordinate in zip(('X','Y','Z','R00','R01','R02','R10','R11','R12','R20','R21','R22'),value):
            ET.SubElement(node,axis).text=number(coordinate)
    elif kind=='Color3':
        for axis,coordinate in zip(('R','G','B'),value): ET.SubElement(node,axis).text=number(coordinate/255)
    elif kind=='UDim2':
        for axis,coordinate in zip(('XS','XO','YS','YO'),value): ET.SubElement(node,axis).text=number(coordinate)
    elif kind=='Vector2':
        for axis,coordinate in zip(('X','Y'),value): ET.SubElement(node,axis).text=number(coordinate)
    else:
        node.text=str(value).lower() if isinstance(value,bool) else str(value)
    return node


class Scene:
    def __init__(self):
        self.root=ET.Element('roblox',{'version':'4'})
        self.sequence=0
        self.world=self.item(self.root,'Model','MatterloomWorld')

    def item(self,parent,kind,name):
        self.sequence+=1
        item=ET.SubElement(parent,'Item',{'class':kind,'referent':f'RBX_CANYON_{self.sequence}'})
        ET.SubElement(item,'Properties')
        prop(item,'string','Name',name)
        return item

    def part(self,parent,name,size,position,color=CONCRETE,material='Concrete',
             rotation=IDENTITY,collide=True,shape=1,kind='Part'):
        item=self.item(parent,kind,name)
        prop(item,'Vector3','size',size)
        prop(item,'CoordinateFrame','CFrame',(*position,*rotation))
        prop(item,'bool','Anchored',True)
        prop(item,'bool','CanCollide',collide)
        prop(item,'bool','CanTouch',False)
        prop(item,'bool','CanQuery',collide)
        prop(item,'Color3uint8','Color3uint8',color[0]*65536+color[1]*256+color[2])
        prop(item,'token','Material',MATERIAL[material])
        prop(item,'token','TopSurface',0)
        prop(item,'token','BottomSurface',0)
        if kind=='Part': prop(item,'token','shape',shape)
        return item

    def tube(self,parent,name,a,b,diameter,color=STEEL,material='Metal',collide=True):
        delta=tuple(v-u for u,v in zip(a,b))
        length=math.sqrt(sum(v*v for v in delta))
        x=tuple(v/length for v in delta)
        guide=(0,0,1) if abs(x[1])>0.9 else (0,1,0)
        def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
        z=cross(x,guide); scale=math.sqrt(sum(v*v for v in z)); z=tuple(v/scale for v in z)
        y=cross(z,x)
        rotation=(x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2])
        return self.part(parent,name,(length,diameter,diameter),tuple((u+v)/2 for u,v in zip(a,b)),
                         color,material,rotation,collide,2)

    def label(self,part,text,face=5,name='Label',color=(215,227,230)):
        surface=self.item(part,'SurfaceGui','SurfaceGui')
        prop(surface,'token','Face',face)
        prop(surface,'Vector2','CanvasSize',(800,240))
        prop(surface,'float','LightInfluence',0.2)
        label=self.item(surface,'TextLabel',name)
        prop(label,'UDim2','Size',(1,0,1,0))
        prop(label,'float','BackgroundTransparency',1)
        prop(label,'string','Text',text)
        prop(label,'Color3','TextColor3',color)
        prop(label,'token','Font',19)
        prop(label,'bool','TextScaled',True)
        prop(label,'bool','TextWrapped',True)
        return label
