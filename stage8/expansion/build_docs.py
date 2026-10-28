"""Generate a compact offline reference for the exact registered new recipes."""
import html
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from expansion.content import MACHINES,expanded_items
BASE=Path(__file__).parent
old=json.loads((BASE.parent/'production/catalogo_8_20.json').read_text())['items']
items=old|expanded_items()
rows=[];cards=[]
for machine in MACHINES:
    recipes=[]
    for key,name,inputs,seconds,shape in machine['recipes']:
        ingredients=' + '.join(f"{items[item]['name']} ×{n}" for item,n in inputs.items())
        rows.append(f"| {machine['name']} | {machine['family']} | {machine['tier']} | ${machine['price']} | {ingredients} | {name} ×1 | {seconds:g} s | ${items[key]['value']} |")
        recipes.append(f'<li><strong>{html.escape(name)}</strong><p>{html.escape(ingredients)} → {html.escape(name)} ×1</p><small>{seconds:g} s nominales · Venta ${items[key]["value"]}</small></li>')
    cards.append(f'<article><span class="family">{machine["family"]} · NIVEL {machine["tier"]} · ${machine["price"]}</span><h2>{machine["name"]}</h2><ul>{"".join(recipes)}</ul></article>')
(BASE/'RECETAS_8_21.md').write_text('''# Matterloom 8.21 — 40 recetas nuevas

20 máquinas adicionales; el total del juego es de 53 recetas y 54 recursos.
Recetas ficticias, no reacciones químicas reales. Todas las salidas son una unidad.
Los tiempos son intervalos nominales entre producciones, revisados cada 0,6 s.
El valor de venta no mide rentabilidad por minuto ni descuenta la instalación.

| Máquina | Familia | Nivel | Compra | Ingredientes | Producto | Intervalo | Venta |
|---|---|---:|---:|---|---|---:|---:|
'''+ '\n'.join(rows)+'\n')
(BASE/'CATALOGO_8_21.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Matterloom · Maquinaria 8.21</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0e1c25;color:#e5eef1;font:16px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:30px 20px}h1{margin-bottom:6px;color:#6ce0e3}p{margin:8px 0}header p{color:#b9c8cf;max-width:800px}label{display:block;margin-top:24px}input{width:100%;margin:8px 0 22px;padding:14px;border:1px solid #557584;border-radius:8px;background:#1b303c;color:#fff;font:inherit}input:focus{outline:2px solid #6ce0e3}#cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px}article{border:1px solid #345361;border-radius:10px;background:#162a36;padding:20px}article[hidden]{display:none}.family{font-size:12px;color:#6ce0e3}h2{font-size:20px;margin:10px 0 18px}ul{padding:0;list-style:none}li+li{border-top:1px solid #345361;margin-top:16px;padding-top:16px}small{color:#b9c8cf}footer{margin:25px 0;color:#b9c8cf}</style>
<main><header><h1>MATTERLOOM · EXPANSIÓN INDUSTRIAL</h1><p>20 máquinas nuevas · 40 recetas nuevas. Repartir materiales entre líneas permite combinar metalurgia, química, cristales, electrónica y robótica.</p><p>En el juego, selecciona una máquina y pulsa G para alternar sus dos recetas. Entradas naranjas y salida cian. Estos son precios iniciales para probar y equilibrar.</p></header>
<label for="search">Buscar máquina, familia, ingrediente o producto</label><input id="search" type="search" placeholder="Por ejemplo: cobre, polímero, motor…" autocomplete="off"><p id="count" aria-live="polite">20 máquinas</p><section id="cards">'''+''.join(cards)+'''</section><footer>Los tiempos son nominales; la simulación revisa cada 0,6 s. La partida conserva las 13 recetas anteriores. Las compras usan créditos; no requieren fabricar piezas. Archivo de consulta sin conexión.</footer></main>
<script>const input=document.querySelector('#search'),cards=[...document.querySelectorAll('article')];const normalize=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();input.addEventListener('input',()=>{let visible=0;const q=normalize(input.value.trim());for(const card of cards){card.hidden=!normalize(card.textContent).includes(q);if(!card.hidden)visible++;}document.querySelector('#count').textContent=visible+' máquinas';});</script></html>''')
print('Generated 20 machine cards and 40 recipe rows')
