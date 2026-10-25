# Matterloom — pruebas de conexiones y cintas

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
