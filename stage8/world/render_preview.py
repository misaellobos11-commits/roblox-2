"""Auxiliary render of actual XML geometry; this is not a Roblox Studio screenshot.
Run: blender -b --python stage8/world/render_preview.py -- world.rbxmx output.png
"""
import sys
import math
import xml.etree.ElementTree as ET
import bpy
from mathutils import Vector

args=sys.argv[sys.argv.index('--')+1:]
source,output=args[:2]
view=args[2] if len(args)>2 else 'overview'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
groups={}
def vector(p,name):return tuple(float(p.findtext(f"*[@name='{name}']/{a}")) for a in ('X','Y','Z'))
for item in ET.parse(source).iter('Item'):
    if item.get('class') not in ('Part','WedgePart','SpawnLocation'):continue
    if float(item.findtext("Properties/float[@name='Transparency']",'0'))>=1:continue
    p=item.find('Properties');size=vector(p,'size');pos=vector(p,'CFrame')
    matrix=[float(p.findtext(f"*[@name='CFrame']/R{r}{c}")) for r in range(3) for c in range(3)]
    color=int(p.findtext("*[@name='Color3uint8']"));material=int(p.findtext("*[@name='Material']"))
    verts,faces=groups.setdefault((color,material),([],[]));offset=len(verts)
    shape=p.findtext("*[@name='shape']",'1')
    if item.get('class')=='WedgePart':
        points=[(-.5,-.5,-.5),(.5,-.5,-.5),(.5,-.5,.5),(-.5,-.5,.5),(-.5,.5,.5),(.5,.5,.5)]
        polygons=[(0,3,2,1),(3,4,5,2),(0,1,5,4),(0,4,3),(1,2,5)]
    elif shape=='2':
        n=16;points=[(x,.5*math.cos(i*math.tau/n),.5*math.sin(i*math.tau/n)) for x in (-.5,.5) for i in range(n)]
        polygons=[tuple(reversed(range(n))),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    elif shape=='0':
        n=12;m=6
        points=[(.5*math.sin(j*math.pi/m)*math.cos(i*math.tau/n),.5*math.cos(j*math.pi/m),.5*math.sin(j*math.pi/m)*math.sin(i*math.tau/n)) for j in range(m+1) for i in range(n)]
        polygons=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(m) for i in range(n)]
    else:
        points=[(x,y,z) for x in (-.5,.5) for y in (-.5,.5) for z in (-.5,.5)]
        polygons=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
    for v in points:
        local=[v[i]*size[i] for i in range(3)]
        xyz=[pos[r]+sum(matrix[r*3+c]*local[c] for c in range(3)) for r in range(3)]
        verts.append((xyz[0],-xyz[2],xyz[1]))
    faces.extend(tuple(offset+i for i in f) for f in polygons)

for (color,kind),(verts,faces) in groups.items():
    mesh=bpy.data.meshes.new('CampusGeometry');mesh.from_pydata(verts,[],faces);mesh.update()
    ob=bpy.data.objects.new('Campus',mesh);bpy.context.collection.objects.link(ob)
    mat=bpy.data.materials.new(str((color,kind)));mat.use_nodes=True
    node=mat.node_tree.nodes.get('Principled BSDF')
    rgb=tuple(((color>>s)&255)/255 for s in (16,8,0))
    # Convert authored sRGB colors to linear for Blender's shading.
    rgb=tuple(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb)
    node.inputs['Base Color'].default_value=(*rgb,1)
    node.inputs['Roughness'].default_value=.75 if kind!=1088 else .38
    node.inputs['Metallic'].default_value=.45 if kind==1088 else 0
    if kind==288:
        node.inputs['Emission Color'].default_value=(*rgb,1);node.inputs['Emission Strength'].default_value=2.5
    ob.data.materials.append(mat)

world=bpy.data.worlds.new('Daylight');bpy.context.scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.48,.63,.82,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.6
sun=bpy.data.lights.new('Late afternoon','SUN');sun.energy=3;sun.angle=math.radians(10);sun.color=(1,.82,.60)
light=bpy.data.objects.new('Sun',sun);bpy.context.collection.objects.link(light)
light.rotation_euler=(math.radians(28),math.radians(-35),math.radians(-25))
cam=bpy.data.cameras.new('Overview');obj=bpy.data.objects.new('Overview',cam);bpy.context.collection.objects.link(obj)
obj.location=(830,-1030,810);target=Vector((0,0,0));obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
if view in ('west','east'):
    side=-1 if view=='west' else 1
    obj.location=(side*130,-260,200);target=Vector((side*510,0,12))
    obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
elif view in ('north','south'):
    side=-1 if view=='north' else 1
    obj.location=(260,-side*130,150);target=Vector((0,-side*510,14))
    obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
cam.type='PERSP';cam.lens=42;cam.clip_end=5000
scene=bpy.context.scene;scene.camera=obj
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False
scene.render.resolution_x=1500;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG';scene.render.filepath=output
bpy.ops.render.render(write_still=True)
