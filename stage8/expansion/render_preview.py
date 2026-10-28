"""Blender adapter for the auxiliary gallery, not a Roblox engine screenshot."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from expansion.content import MACHINES
source=(Path(__file__).resolve().parents[1]/'world'/'render_preview.py').read_text()
start=source.index("elif view=='cargo':")
end=source.index("cam.type='PERSP'",start)
source=source[:start]+'''elif view=='expansion':
    obj.location=(43,-79,92);target=Vector((0,0,1.8))
    obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
    for index,label in enumerate(LABELS):
        font=bpy.data.curves.new('MachineLabel','FONT');font.body=label;font.align_x='CENTER';font.size=.5
        text=bpy.data.objects.new(label,font);bpy.context.collection.objects.link(text)
        text.location=((index%4-1.5)*12,-(index//4-2)*13-5.2,.02)
        mat=bpy.data.materials.new('LabelInk');mat.diffuse_color=(.8,.9,.95,1);font.materials.append(mat)
'''+source[end:]
source=source.replace('resolution_x=1500','resolution_x=2000').replace('resolution_y=1000','resolution_y=1600').replace('cam.lens=42','cam.lens=48').replace('scene.cycles.samples=48','scene.cycles.samples=24')
exec(compile(source,'auxiliary-gallery','exec'),{'LABELS':[m['name'] for m in MACHINES]})
