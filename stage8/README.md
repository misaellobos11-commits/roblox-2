# Matterloom — pruebas de conexiones y cintas

## Revisión del árbol de producción de 8.20

El usuario aprobó auditar las recetas y preparar el árbol antes de expandir la
maquinaria. No se genera una nueva versión del juego en esta revisión.

- `production/ANALISIS.md`: hallazgos, progresión y propuestas futuras separadas.
- `production/RECETAS_ACTUALES.md`: 13 recetas con entradas, salidas, tiempos y valores.
- `production/ABRIR_Arbol_Produccion.html`: visor sin dependencias externas.
- `production/Arbol_Produccion.svg`: diagrama exportable.
- `production/catalogo_8_20.json`: datos extraídos ejecutando el Luau del archivo.

Regenerar: `python stage8/production/audit.py`, después
`python stage8/production/build_tree.py` y `node stage8/production/check_viewer.js`.
La extracción confirma 14 recursos alcanzables y 5 productos sin receta posterior.
La recomendación es ampliar filtros, medir cadenas completas y después introducir
una rama química que aproveche hidrógeno y compuesto de carbono. Las propuestas
no se mezclan con el árbol de recetas vigentes.

## 8.20: identidad visual de los recursos transportados

`bash stage8/check_820.sh` genera `build/Matterloom_8_20_Recursos_Transportables.rbxlx`.
Entrega: `downloads/Matterloom_8_20_Recursos_Transportables.zip`, con guía y vista
auxiliar de los recursos. El usuario eligió formas propias por recurso.

`visuals/cargo_shapes.py` define 14 modelos originales de 3 a 6 piezas: mineral,
carbono, botellas de gas, láminas, barras, compuestos, bobina, cristales y lingote.
El registro está separado de recetas, precios y puertos; una nueva materia puede
recibir su forma sin modificar la lógica de transporte. Hay un contenedor de
respaldo para recursos futuros que aún no tengan modelo.

El Part animado existente se conserva como portador invisible. Sus piezas siguen
su CFrame mediante una conexión que se desconecta al destruirlo. Todas están
ancladas, sin colisiones, eventos de contacto, consultas ni sombras individuales.
El apoyo se ajusta a la misma altura de banda para cintas, divisores y ascensores.
No se añaden luces. Se reemplazan tanto Producto como ProductoSalida.

La comparación XML permite solo MachineVisual y la etiqueta de versión.
Las pruebas cubren 14 recursos en 5 transportes, rotaciones, geometría y limpieza,
las animaciones de curvas/bloqueo existentes y rutas de divisores/ascensores.
Los adaptadores no reproducen replicación, señales diferidas ni renderizado de
Roblox. Se debe probar suavidad y rendimiento en Studio con muchas cargas,
pues cada paquete ahora mueve varias piezas. La vista auxiliar usa las mismas
definiciones y no reproduce la iluminación del motor Roblox.

## 8.19: desfiladero conectado y cielo

`bash stage8/check_819.sh` genera `build/Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx`.
Entrega: `downloads/Matterloom_8_19_Canon_Estratificado_y_Cielo.zip` con guía.

`world/horizon_819.py` sustituye únicamente `CanyonRockFormations`: un anillo de
arenisca estratificada, salientes unidos a la pared y coronas de altura variable.
Hay 1388 piezas nuevas frente a las 1804 del fondo anterior. Las caras visibles
son sólidas, cuatro bases conectan las esquinas y cuatro límites invisibles,
situados detrás del paisaje en |x|/|z|=884, impiden caídas fuera del suelo del mapa.
La geometría se mantiene fuera de los edificios existentes (hasta radio 622).

El cielo usa las texturas incluidas en Roblox, ajusta orientación, sol, luna y
estrellas. Las nubes nativas de Terrain ganan cobertura y cambian con el reloj;
GlobalWind mueve las nubes. No se recupera la niebla. Se conservan las 136 luces,
el ciclo de 20 minutos y toda la producción, maquinaria, parcelas y HUD.

La comparación XML permite solo esos cambios y la etiqueta de versión. Las
pruebas cubren todos los lados/esquinas del límite, las propiedades de Sky y
Clouds mediante Rojo y la actualización nocturna con adaptadores de servicios.
La revisión auxiliar de geometría no renderiza el cielo Roblox; es necesario
comprobar colisiones del personaje, cielo y rendimiento en Studio.

## 8.18: niebla eliminada e iluminación de las farolas

`bash stage8/check_818.sh` genera `build/Matterloom_8_18_Noche_Clara_y_Focos.rbxlx`.
ZIP: `downloads/Matterloom_8_18_Noche_Clara_y_Focos.zip`, con guía de inspección.

La captura nocturna del usuario mostró niebla sobre el fondo y parcelas negras.
El archivo conservaba `Atmosphere.Haze=0.6` y el ciclo volvía a establecer una
densidad positiva cada actualización. Además, 116 de las 124 farolas solo tenían
un cuerpo de neón y carecían de una fuente de luz. Las pruebas de regresión
fallan con esos síntomas sobre la versión 8.17.

La corrección anula Density/Haze/Glare en el archivo y durante el ciclo, y aleja
la niebla clásica fuera del mapa. Las farolas existentes reciben PointLights
sin sombras (rango 48); hay 136 luces contando las 12 del perímetro. Se apagan
de día y aumentan al oscurecer. La paleta nocturna refuerza la luz ambiental y
reduce el contraste; la paleta diurna se conserva. No se añade geometría.

La comparación XML protege todo el contenido anterior ajeno a estos cambios.
Las pruebas ejecutan un ciclo completo, entrada tardía y luz dinámica con
adaptadores, y comprueban también propiedades de luces al pasar por Rojo.
No hay motor de Roblox disponible: aspecto y coste de renderizado quedan
pendientes de validar en Studio, especialmente en equipos modestos.

Dirección futura confirmada por el usuario: ampliar maquinaria y combinaciones.
Ver [DIRECCION_PRODUCCION.md](DIRECCION_PRODUCCION.md) antes de tocar producción,
recetas, puertos o progresión. La 8.18 no incorpora nuevas máquinas.

## 8.17: completar el perímetro y ciclo de día/noche

`bash stage8/check_817.sh` genera `build/Matterloom_8_17_Perimetro_Dia_Noche.rbxlx`.
Entrega: `downloads/Matterloom_8_17_Perimetro_Dia_Noche.zip`, con guía de prueba.

Doce módulos completan los cuatro muros, con estaciones de bombeo, ventilación,
conductos y paneles; `world/perimeter_817.py` añade 376 piezas y 12 luces sin
sombras (20 en total). Se conserva la decoración de 8.16, con pasos libres.
Se eligieron módulos industriales de escala visible desde la parcela para
integrar los muros al complejo y evitar pequeñas piezas de relleno.

`environment/DayNight.server.luau` publica una época común por servidor.
`DayNight.client.luau` calcula la hora desde `GetServerTimeNow()` y aplica una
paleta suave, sin replicar cambios cada fotograma. El módulo `DayNight.luau`
contiene el reloj y las transiciones. Por defecto son 1200 segundos por ciclo,
iniciando a las 16:12. El atributo numérico de Workspace `DayNightCycleSeconds`
permite ajustarlo (mínimo 60; por debajo se usa el valor predeterminado).
Este ajuste es una decisión inicial de implementación, no hora real del usuario.
El cliente controla solo las luces del entorno, no las de las máquinas.

Las pruebas cubren vuelta de medianoche, sesiones largas, entrada tardía,
pausas de fotogramas, duración configurable y alta/baja de luces. Se ejecutan
los scripts que contiene el archivo entregable con adaptadores de servicios;
no sustituyen una prueba en Studio. La comparación XML completa protege el
contenido anterior; Rojo verifica geometría y propiedades. La visibilidad de
noche y el rendimiento quedan pendientes de comprobar en Roblox Studio.

## 8.16: identidad para los costados izquierdo y derecho

`bash stage8/check_816.sh` genera `build/Matterloom_8_16_Sectores_Laterales.rbxlx`.
ZIP: `downloads/Matterloom_8_16_Sectores_Laterales.zip` con guía de inspección.

Se añaden cuatro conjuntos decorativos fuera de las parcelas: energía y
refrigeración al oeste, logística y mantenimiento al este. Incluyen equipos,
contenedores, grúa baja, taller, senderos, bolardos y rótulos sobre los muros.
`world/side_districts.py` genera 246 piezas ancladas, sin scripts ni luces nuevas.
La geometría queda por debajo de las terrazas y fuera de calles, parcelas y rampas.
Los equipos se distribuyen a ambos lados de la tubería existente sin atravesarla.

El archivo conserva exactamente el contenido de 8.15 salvo la carpeta añadida
`Workspace/MatterloomWorld/SideDistricts` y el rótulo de versión. Los controles
comprueban determinismo, límites, paso peatonal, accesos y separación de tuberías;
Rojo verifica las propiedades geométricas al leer/escribir el XML. Se revisan
ambos laterales con vistas auxiliares de la geometría en Blender; la luz real,
el recorrido y el rendimiento quedan pendientes de comprobar en Studio.

## 8.15: retirar las rocas puntiagudas junto al muro

`bash stage8/check_815.sh` genera `build/Matterloom_8_15_Perimetro_Despejado.rbxlx`.
ZIP: `downloads/Matterloom_8_15_Perimetro_Despejado.zip`.

El usuario señaló las rocas bajas en forma de pirámide. Se retiran las cuarenta
formaciones de esa franja, incluidos sus volúmenes invisibles de colisión: 680
piezas en total. Los afloramientos grandes del fondo se mantienen exactamente.
La opción `include_talus=False` conserva la generación original 8.14 por defecto.
Se compara el XML completo: las únicas diferencias son las piezas retiradas y el
rótulo 8.15 del menú Pruebas. Se valida además la geometría restante con Rojo.
La lógica del juego y los demás ajustes visuales quedan intactos.

## 8.14: respuesta a la captura real del HUD y el cañón

`bash stage8/check_814.sh` genera `build/Matterloom_8_14_Entorno_y_HUD.rbxlx`.
Distribución: `downloads/Matterloom_8_14_Entorno_y_HUD.zip` con guía de comparación.

Se corrigen los cinco puntos aceptados por el usuario: panel inferior contextual,
demos en un menú Pruebas, rocas sin cajas apiladas, iluminación cálida y clara,
cuadrícula local discreta y nombres integrados en placas físicas. La cabecera pasa
a 64 px; el panel de acciones queda oculto en reposo y tiene hasta 620 px de ancho.
Receta/Filtro solo se muestran para una máquina compatible. El catálogo horizontal
y la descripción derecha se conservan; abrirlo oculta la barra de acciones.

El servidor mantiene una carpeta Grid vacía. Cada cliente genera 98 líneas suaves,
sin colisión, consultas ni sombras, exclusivamente para su parcela mientras coloca
o mueve objetos. Sigue la altura automática del transporte y se oculta al cancelar
o abrir el catálogo. Solo el borde de la parcela propia recibe el cian luminoso.
Los carteles son SurfaceGui sobre placas de 14 × 4 studs, mirando hacia el acceso,
con AlwaysOnTop=false y alcance 72, en lugar de BillboardGui de 240 × 78 píxeles.

El archivo conservaba Technology=Voxel y LightingStyle=Soft. Se fijan Future y
Realistic, prioridad de iluminación, hora consistente 16:12, ambiente cálido y menor
dispersión atmosférica. `world/refine_814.py` reemplaza las cajas por poliedros
irregulares propios: cada cara triangular se divide en dos WedgeParts rectos.
Las caras no colisionan ni participan en raycasts; envolventes invisibles aportan
colisión en el perímetro. El escenario contiene 5.005 piezas, ocho luces y un spawn.

Validación: controlador completo, HUD en varios tamaños, lifecycle de cuadrícula,
carteles físicos, 128 acoples de transportes, circuito de ascensores, catálogo,
simulación y regresiones anteriores. La prueba de HUD nuevo falla sobre 8.13.
La geometría conserva ocho huellas libres, rampas transitables, IDs únicos y formato
Roblox comprobado con Rojo. La revisión independiente no encontró regresiones.
Se comparan todos los scripts: cambian solo BuildUI, BuildController y BuildServer;
se preservan assets, simulación, catálogo de máquinas y respaldos. En el mundo se
conservan carreteras, plaza, infraestructura, vegetación y alrededores de parcelas.
La vista geométrica de Blender permite revisar siluetas, pero no valida la luz ni
el render real de Roblox. La guía pide comprobar eso y rendimiento en Studio.

## 8.13: selección por defecto y catálogo horizontal

`bash stage8/check_813.sh` genera `build/Matterloom_8_13_Catalogo_Horizontal.rbxlx`.
ZIP: `downloads/Matterloom_8_13_Catalogo_Horizontal.zip` con guía de prueba.

El modo normal permite marcar/desmarcar mediante clic/toque y seleccionar áreas
con arrastre. La selección única mantiene detalles, mover y receta; un grupo
desactiva las acciones de un solo objeto. El borrado usa una sola acción para
cualquier cantidad y conserva la confirmación y bloqueo de solicitudes pendientes.
Se retiran el selector de modo múltiple y el control manual de altura (incluidos
V/T). El ajuste automático de altura se aplica a cintas, divisores, filtros y
desbordes; el arrastre conserva su nivel. Las tres demos permanecen disponibles
por indicación del usuario.

El catálogo aprovecha más ancho, con miniaturas de hasta 100 × 88 píxeles, dos
filas y desplazamiento horizontal cuando falta espacio. A partir de 900 píxeles
caben seis columnas y las once máquinas de Producción sin desplazamiento. Las
descripciones permanecen a la derecha y se desplazan verticalmente cuando hace
falta. El panel de acciones se reduce a nueve botones en tres filas.

Se ejecuta el controlador completo con adaptadores de servicios: clic, arrastre,
toque, cancelación, mover una pieza, protección de acciones de grupo, confirmación
de borrado, respuestas del servidor, demos y eliminación de T/V. El HUD real prueba
distribución, estados y límites en cinco tamaños de pantalla. Los casos nuevos
fallan en 8.12 y pasan en 8.13. Se mantienen las 32 conexiones de ascensores y el
circuito manual que vende 26 paquetes, además de todas las regresiones anteriores.
La revisión detectó que retirar T dejaba a los otros transportes sin cambio de
altura: se extendió la detección al tipo realmente colocado y se verificaron
128 casos de transporte, además de órdenes reales del controlador para colocar
un divisor arriba y un filtro abajo. El caso se observó fallar antes del ajuste.
La comparación XML permite solo BuildController y BuildUI: el cañón y la lógica
del servidor se conservan. Las pruebas no ejecutan la interfaz en Roblox Studio.

## 8.12: complejo industrial en un cañón

`bash stage8/check_812.sh` genera `build/Matterloom_8_12_Canon_Industrial.rbxlx`.
ZIP: `downloads/Matterloom_8_12_Canon_Industrial.zip`, con guía para Studio.

Adapta la referencia del usuario a Parts editables: ocho parcelas alrededor de
una plaza circular con núcleo cian, avenidas, aceras, cuatro rampas, terrazas de
servicio, edificios, depósitos, tuberías, acantilados arena y acacias dispersas.
El mapa y la iluminación están incluidos en el archivo para verse antes de Play.
El generador `world/canyon.py` produce geometría y MapConfig con la misma fuente
de coordenadas. El cargador elimina únicamente PreviewPlots y devuelve el spawn
existente; BuildServer sigue creando las parcelas autoritativas. Sus cambios se
limitan a colores, acceso lateral y orientación del personaje al llegar.

Se conservan selección de parcela, 48 × 48 casillas, máquinas originales, economía,
HUD y correcciones de transporte/ascensores. Solo cambian cuatro scripts activos:
MapConfig, MapGenerator, BuildServer y el rótulo de BuildUI. Assets y backups quedan
intactos. El trabajo antiguo sin terminar de src/world no forma parte de esta versión.

Verificación: 3.665 piezas ancladas en edición, ocho luces, un spawn, ocho huellas
sin decoración, entradas transitables, rampas sin muro al final, ausencia de
superficies de carretera/acera superpuestas, IDs únicos y generación determinista.
El cargador, la creación real de parcelas, sus carteles y la orientación de llegada
se ejecutan con adaptadores. Rojo comprueba la lectura/escritura de dimensiones,
transformaciones, materiales y colisiones del XML. Todas las regresiones 8.11 pasan.
La revisión detectó una intersección rampa/terraza: el nuevo caso falló antes y pasó
al terminar la pendiente en el borde interior de la terraza (radio 540, altura 40).

Se revisaron proporciones con un render auxiliar de la geometría XML en Blender,
no una captura de Roblox. `world/render_preview.py` permite reproducir esa vista.
No se afirma igualdad fotorrealista con la referencia ni rendimiento medido en
Studio; la guía cubre esas comprobaciones y el recorrido con dos jugadores.

## 8.11: colocación de cintas junto a ascensores

`bash stage8/check_811.sh` genera
`build/Matterloom_8_11_Conexiones_Ascensores.rbxlx`.
Distribución: `downloads/Matterloom_8_11_Ascensores.zip`, con guía de prueba manual.

Las rutas de ascensores ya funcionaban en las demos, pero el controlador proyectaba
el puntero al suelo, reiniciaba la altura al elegir una cinta y solo atraía piezas
a puertos de máquinas grandes. El atajo T no tenía botón visible.

Para las cintas, el puntero se proyecta al plano de cada puerto y se valida el
acople con Catalog.connected y Construction.canPlace. La vista previa adopta
posición, altura y orientación. Un arrastre iniciado fija su altura; T fija el
nivel explícito y cancela el trazo actual. R conserva la orientación manual para
piezas aisladas. Volver a elegir Transportador reactiva el acople automático.
Los puertos superpuestos en pantalla priorizan el cercano a la cámara; T permite
elegir el nivel inferior. El HUD añade el botón de altura a la cuadrícula existente.

Regresiones: groundAt real en 32 combinaciones de ascensor/puerto/giro/subcuadrícula,
altura de arrastre y selección manual, puertos superpuestos y un circuito de subida,
cintas elevadas y bajada que registra 26 ventas en 60 segundos simulados. El HUD
real comprueba botón, callback, etiquetas y restricciones. Los casos de acople y
botón se observaron fallar sobre 8.10. Pasan también las pruebas anteriores de
lógica, demos, transporte, modelos, animación, catálogo y compilación.
El circuito ejecuta beginStroke/strokeTo/endStroke reales; se verifica también que
el callback T cancele el trazo sin enviar una orden y respete la altura elegida.
Una revisión independiente no encontró defectos dentro del alcance.
La comparación XML limita los cambios a BuildController y BuildUI frente a 8.10.
Los adaptadores no ejecutan el motor de Roblox; la guía cubre la prueba real de
puntero, cámara, arrastre y controles táctiles. El terreno queda para después.

## 8.10: tres cuerpos con la salida trasera

`bash stage8/check_810.sh` genera `build/Matterloom_8_10_Tres_Modelos.rbxlx`.
Distribución: `downloads/Matterloom_8_10_Tres_Modelos.zip`.

El usuario identificó exclusivamente Receiver, ElementSynthesizer y FusionChamber
como girados después de probar 8.9. Se aplica un yaw local de π a sus tres claves
de importación, antes de centrar/escalar y aplicar el pivot del wrapper. Ninguna
otra clave recibe compensación. El catálogo usa la misma orientación al crear
miniaturas. El único otro cambio es el rótulo de versión en BuildUI.

La regresión ejecuta el instalador real con composición de transforms: 96 casos
(24 tipos × cuatro rotaciones), corrige los tres cuerpos y preserva los demás.
Se observó fallar en 8.9 y pasar en 8.10. También pasan las comprobaciones completas
de lógica, demos, HUD, transporte, animaciones y compilación de 14 scripts.
La comparación XML permite solo MachineVisual y BuildUI frente a 8.9; todas las
plantillas, geometría, lógica y backups del lugar se conservan.
La prueba no inspecciona vértices de mallas externas: el ajuste de 180° sigue
pendiente de comprobación visual en Studio con la guía incluida.

## 8.9: restauración de máquinas, miniaturas y movimiento de cintas

Ejecutar `bash stage8/check_89.sh`. Genera
`build/Matterloom_8_9_Catalogo_y_Animaciones.rbxlx`, distribuido en
`downloads/Matterloom_8_9_Catalogo.zip` con guía y respuestas.

El usuario aclaró que solo quería cambiar el transporte; confirmó explícitamente
recuperar las máquinas grandes y conservar divisores, filtros y ascensores 8.8.
Los 14 tipos de tamaño 2 vuelven a usar las mallas originales con la selección
importada; los nueve tipos de transporte especiales conservan la geometría 8.8.
El catálogo y simulación lógica no cambian. Las plantillas originales se conservan.

Las 24 tarjetas usan ViewportFrame/WorldModel con el mismo Visual.create que la
pieza colocada. Cámara ajustada a dimensiones/aspecto, iluminación propia y precio
debajo; nombres y descripciones permanecen a la derecha. Se evita reconstruir
miniaturas en cada reporte de economía. Los estados de precio, nivel y solicitud
pendiente siguen controlando la compra. La columna derecha usa filas de altura
automática, contenido desplazable y categorías con ancho fijo desplazables.
El diseño usa ScreenGui.AbsoluteSize para respetar los márgenes de Roblox.

Las cintas animan un progreso continuo de 0,58 segundos, casi todo su ancho
(-1,92 a +1,92 studs), a altura 1,52 para evitar hundirse en la banda. Las curvas
usan la misma Bézier cúbica de su trazado, sin la anterior esquina de dos tweens.
La entrega aceptada limpia el cubo anterior, permitiendo reiniciar otro paquete
idéntico. Si está bloqueado, conserva su posición; eliminar la pieza cancela y
limpia el tween y sus conexiones. Se mantiene el tick autoritativo de 0,6 s.

Regresiones observadas fallar antes y pasar después: restauración de las 14 máquinas,
tarjetas con miniatura/descripción/precio, compra pendiente, límites de pantalla y
márgenes, texto adaptable, recorrido completo y curvo, repetición y limpieza.
También pasan las direcciones, las tres demos (317/128/427 ventas), la geometría
del transporte, selección y compilación de 14 scripts. Exactamente dos fuentes
cambian frente a 8.8 (MachineVisual y BuildUI). Una revisión independiente detectó
dos problemas de texto/márgenes; ambos se corrigieron y verificaron antes de entregar.

Los tests de UI ejecutan handlers reales sobre adaptadores; no sustituyen el
renderizado ni mediciones de fluidez/red en Studio. La guía pide comprobar carga
de miniaturas, legibilidad y movimiento real. El sistema sigue animando desde el
servidor; esta entrega mejora el recorrido y continuidad, no cambia la red.

## 8.8: diseño y direcciones desde los puertos reales

Ejecutar `bash stage8/check_88.sh`. Genera
`build/Matterloom_8_8_Diseno_y_Direcciones.rbxlx` y se distribuye en
`downloads/Matterloom_8_8_Diseno.zip` con guía y plantilla de respuestas.

El usuario confirmó que 8.7 seguía mal. La calibración de mallas de esa entrega
no resolvió el problema. La nueva reproducción además encontró una inversión
lógica: para avance +Z, la izquierda del viajero es +X; `Catalog.port` devolvía -X.
Se corrigen izquierda/derecha y sus entradas laterales. Doce entradas literales
de demos cambian a la variante opuesta para mantener sus circuitos existentes.

La construcción parte de 8.6, conservando sus cintas. Los otros 23 tipos dejan
de depender del frente desconocido de una malla externa: utilizan geometría
industrial controlada, con puertos y cheurones derivados de `Catalog.inputPorts`
y `Catalog.outputs`. Se reutilizan los cuerpos procedurales de producción;
los distribuidores y ascensores tienen un diseño nuevo. Las plantillas GLB
originales permanecen intactas en el archivo. La apariencia de las máquinas cambia.

La simulación avisa al visual solamente después de una transferencia aceptada.
El cubo de un distribuidor espera centrado y su animación de salida sigue esa ruta.
Los ascensores usan las alturas del catálogo, un hueco central abierto y tres
etapas de movimiento. Al entregar se limpia el cubo anterior para reiniciar el
siguiente paquete, aunque contenga el mismo material. La animación de las cintas
no se modifica. La selección usa cajas invisibles sin colisión ni eventos Touch.

Validación observada fallar antes y pasar después:
- izquierda/derecha relativas al avance en las cuatro rotaciones;
- 48 entregas de filtros/divisores/desbordes, prioridades y salidas bloqueadas;
- 60 animaciones de salida aceptada y espera sin falsa salida frontal;
- ascensores en cuatro rotaciones: entrada/salida, alturas, paquetes idénticos;
- 184 combinaciones tipo/rotación/preview con el código visual completo:
  bocas en los puertos reales, puntas de cheurones orientadas, hitboxes y huecos;
- regresiones de cintas/arrastre/demos y compilación de los 14 scripts.

Las demos conservan ventas 317/128/427 en 120 segundos simulados. La comparación
XML permite exactamente seis fuentes cambiadas frente al archivo original,
cinco frente a 8.6. Se conserva todo el resto del lugar, assets y backups.
Los tests ejecutan código real con adaptadores matemáticos de CFrame/Instance;
no sustituyen la ejecución visual, raycasts, replicación ni rendimiento en Studio.

## 8.7: orientación de modelos importados

Ejecutar `bash stage8/check_87.sh`. Genera
`build/Matterloom_8_7_Orientacion_Maquinas.rbxlx` sobre la versión 8.6.
Guía: `GUIA_PRUEBA_8_7.txt`. ZIP: `downloads/Matterloom_8_7_Maquinas.zip`.

El usuario confirmó que las cintas 8.6 funcionan; reportó inversión visual en
divisores, filtros, ascensores y el receptor. El instalador normalizaba todas las
mallas con `PivotTo(CFrame.identity)`, descartando la orientación del template
(los 26 templates del archivo tienen yaw 180° y un atributo de corrección previo).
Las conexiones y las bocas dibujadas en la malla usan convenciones independientes.

Se aplica una calibración visual explícita de 180° a los 23 tipos importados
restantes, antes de centrar, escalar y colocar en el wrapper. Las familias laterales
usan el modelo espejo para conservar el lado de salida después del giro.
La simulación, catálogo, controlador, cintas procedurales y sus rutas no cambian.
Tampoco se cambian los templates ni las copias de seguridad del archivo.

Los tests ejecutan el instalador real con composición de traslación/rotación y
92 casos de tipo/orientación, más fallback y preservación de cintas. Los casos
de calibración fallan en 8.6 y pasan en 8.7. La comparación XML permite exactamente
dos fuentes distintas de 8.6 (MachineVisual y BuildUI); las demos mantienen ventas
317/128/427 en 120 segundos simulados.

Límite importante: las convenciones nativas (-Z frontal, lados -X/+X) son fixtures
de calibración basados en las capturas, no datos extraídos de vértices/texturas.
El entorno no accede a esas mallas externas ni ejecuta Studio. Los tests validan
las transformaciones bajo ese contrato; la guía pide confirmar cada familia,
los lados y alturas en Studio. No se afirma haber inspeccionado visualmente las
23 mallas. La animación sobre distribuidores sigue siendo simplificada y no se
confunde con la ruta efectiva elegida por la simulación.

## 8.6: sentido visual y arrastre

Ejecutar `bash stage8/check_86.sh`. Genera `build/Matterloom_8_6_Cintas.rbxlx`
desde la misma base 8.4, aplicando primero las correcciones 8.5.
Guía: `GUIA_PRUEBA_8_6.txt`. ZIP: `downloads/Matterloom_8_6_Cintas.zip`.

El caso reportado se reproduce con un arrastre contrario a la rotación previa:
el antiguo planificador invertía el recorrido completo. Ahora un trazo de varias
celdas sigue el ratón; R sigue orientando una pieza aislada. Las previsualizaciones
tienen puntas de flecha y respetan el nivel de construcción.

Las rectas importadas contenían sus propias flechas dentro de una malla/textura
externa; las curvas y el movimiento se generaban con ejes locales +Z. No se ha
podido inspeccionar esa textura ni ejecutar Roblox en este entorno. Para eliminar
esa dependencia de orientación, las rectas se generan con el mismo estilo y eje
de las curvas. Las plantillas importadas permanecen intactas en el archivo.
Esta es una corrección visual además de la corrección del planificador, no un
cambio del sentido lógico global ni de la economía.

Validación: casos de arrastre con R y curvas consecutivas, transferencias bloqueadas
entre cintas enfrentadas en cuatro orientaciones, flechas locales, sustitución de
rectas/curvas, previsualización en ambos niveles, selección importada, tres demos,
compilación de los 14 scripts y conservación XML (exactamente cuatro fuentes
activas distintas del original). Los tests nuevos se observaron fallar en 8.5.
La prueba de cintas enfrentadas ya pasaba en 8.5; protege esa regla existente.
Los adaptadores de renderizado comprueban geometría enviada a Roblox, no su
ejecución en el motor. El aspecto, clics reales y movimiento visual requieren Studio.
Una revisión independiente no detectó fallos bloqueantes en el alcance del cambio.

## 8.5: conexiones y selección (conservada)

Esta versión parte del archivo 8.4 adjuntado por el usuario, no de la ampliación
industrial anterior del repositorio. `original-8.4.rbxlx` conserva el archivo recibido.

Ejecutar desde la raíz: `bash stage8/check.sh`.
Requiere Python 3 y Luau CLI en `/workspace/tools/luau-0.744`.
La salida es `build/Matterloom_8_5_Prueba_Conexiones.rbxlx`.

Se cambian exactamente tres scripts activos: MachineCatalog (dirección de flujo),
MachineVisual (superficie seleccionable importada) y BuildUI (identificación 8.5).
Los assets, geometría, demás scripts y respaldos se comprueban sin cambios semánticos.

Pruebas originales observadas fallar y nuevas pasar: dirección de cuatro giros,
20 recorridos por arrastre, tres grafos de demos y 48 casos del contrato de selección.
Las demos venden 317/128/427 productos en 120 segundos virtuales. Los 14 scripts
activos compilan. La ejecución visual real requiere Studio: GUIA_PRUEBA_8_5.txt.

La revisión independiente no encontró problemas importantes en el alcance corregido.
La caja seleccionable cubre la altura del modelo importado, permanece invisible y
no colisiona; su efecto visual y clic real se comprueban con el usuario en Studio.
Los problemas fuera de alcance están enumerados en PLAN.md y la guía; no se afirma
que el prototipo completo esté terminado ni que todas las incidencias estén resueltas.
