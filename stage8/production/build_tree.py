"""Render a standalone interactive HTML and exportable SVG from the audited catalog."""
from pathlib import Path
import html,json,textwrap
P=Path(__file__).parent
d=json.loads((P/'catalogo_8_20.json').read_text())
positions={'RawMatter':(15,435),'Carbon':(265,80),'Oxygen':(265,225),'Silicon':(265,370),'Iron':(265,515),'Copper':(265,660),'Hydrogen':(265,805),'CarbonCompound':(585,80),'Silicate':(585,340),'BaseMetal':(585,580),'ConductiveMix':(585,805),'BasicCrystal':(895,340),'SyntheticOre':(895,580),'Ingot':(1190,580)}
assert set(positions)==set(d['items'])
w,h=185,90
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 960" role="img" aria-labelledby="treeTitle"><title id="treeTitle">Árbol actual de producción de Matterloom 8.20</title>',
 '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="#75a7b2"/></marker></defs>',
 '<rect width="1400" height="960" fill="#142631"/>']
for x,title in ((15,'MATERIA'),(265,'ELEMENTOS'),(585,'COMBINACIONES'),(895,'REFINADOS'),(1190,'FINAL')):
 svg.append(f'<text x="{x}" y="35" font-family="sans-serif" font-size="15" fill="#91b4c2">{title}</text>')
edges=[]
for recipe in d['recipes'].values():
 for a in recipe['inputs']:
  for b in recipe['outputs']:
   x,y=positions[a];xx,yy=positions[b];sx=x+w;sy=y+h/2;ey=yy+h/2
   svg.append(f'<path class="edge" data-from="{a}" data-to="{b}" d="M{sx} {sy} C{sx+70} {sy},{xx-70} {ey},{xx} {ey}" fill="none" stroke="#75a7b2" stroke-width="2" marker-end="url(#arrow)"/>')
   edges.append((a,b))
for key,(x,y) in positions.items():
 item=d['items'][key];recipe=next((r for r in d['recipes'].values() if key in r['outputs']),None)
 tier=d['machines'][recipe['machines'][0] if recipe else 'Receiver']['tier']
 stroke='#e8bc72' if key in d['terminal_items'] else '#55c7d0'
 svg.append(f'<g class="node" data-id="{key}" tabindex="0" role="button" aria-label="{html.escape(item["name"])}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#233e4b" stroke="{stroke}" stroke-width="2"/>')
 lines=textwrap.wrap(item['name'],width=19)
 for index,line in enumerate(lines):
  svg.append(f'<text x="{x+12}" y="{y+29+index*22}" font-family="sans-serif" font-size="17" fill="#eef7f8">{html.escape(line)}</text>')
 svg.append(f'<text x="{x+12}" y="{y+75}" font-family="sans-serif" font-size="13" fill="#b8d4dc">Venta ${item["value"]} · Nivel {tier}</text></g>')
svg.append('<text x="15" y="940" font-family="sans-serif" font-size="15" fill="#e8bc72">Borde dorado: sin receta posterior. Todos los materiales se pueden vender.</text></svg>')
svg='\n'.join(svg)
(P/'Arbol_Produccion.svg').write_text(svg)
template=(P/'tree_template.html').read_text()
page=template.replace('__SVG__',svg).replace('__DATA__',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
(P/'ABRIR_Arbol_Produccion.html').write_text(page)
assert len(edges)==17
print('PASS production diagram: 14 resource nodes, 17 ingredient links, 13 recipe records; no external assets')
try:
 import cairosvg
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(P/'Arbol_Produccion.png'),output_width=1960,output_height=1344)
 print('Exported PNG')
except ImportError:print('PNG export unavailable; SVG remains directly viewable')
