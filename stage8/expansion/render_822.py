"""Render the model geometry for art review; never presented as Studio rendering."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from expansion.content import MACHINES
from expansion.preview_822 import CLOSE
args=sys.argv[sys.argv.index('--')+1:]
close=len(args)>2 and args[2]=='close'
source=(Path(__file__).resolve().parents[1]/'world'/'render_preview.py').read_text()
start=source.index("elif view=='cargo':");end=source.index("cam.type='PERSP'",start)
source=source[:start]+'''elif view in ('polish','close'):
    obj.location=(45,-68,95);target=Vector((0,0,2.4))
    obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler()
    rows=math.ceil(len(LABELS)/COLUMNS)
    for index,label in enumerate(LABELS):
        font=bpy.data.curves.new('MachineLabel','FONT');font.body=label;font.align_x='CENTER';font.size=.46
        text=bpy.data.objects.new(label,font);bpy.context.collection.objects.link(text)
        text.location=((index%COLUMNS-(COLUMNS-1)/2)*12,-(index//COLUMNS-(rows-1)/2)*13-5.2,.02)
        mat=bpy.data.materials.new('LabelInk');mat.diffuse_color=(.8,.9,.95,1);font.materials.append(mat)
'''+source[end:]
source=source.replace("cam.type='PERSP';cam.lens=42", "cam.type='ORTHO';cam.ortho_scale="+('44' if close else '95')+";cam.lens=48")
source=source.replace('resolution_x=1500','resolution_x=2000').replace('resolution_y=1000','resolution_y=1700').replace('scene.cycles.samples=48','scene.cycles.samples=32')
exec(compile(source,'polished-machine-gallery','exec'),{'LABELS':[m['name'] for m in (CLOSE if close else MACHINES)],'COLUMNS':3 if close else 4})
