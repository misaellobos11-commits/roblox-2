# Matterloom — pruebas de conexiones y cintas

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
