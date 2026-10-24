# Matterloom 8.5 — test de conexiones y selección

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
