# Matterloom 8.21 — expansión industrial

El usuario pide ejecutar una ampliación grande de maquinaria y combinaciones.
Se implementan 20 máquinas, 40 recetas y 40 recursos adicionales sobre 8.20.
Conservar las máquinas importadas, transporte corregido, mapa y ciclo día/noche.

## Decisiones de implementación

Se elige una expansión de familias interconectadas: metalurgia, química,
cristales, electrónica, componentes y materia avanzada. Frente a añadir sólo
variantes de velocidad o una única rama larga, permite repartir ingredientes
entre productos distintos. Cada máquina ofrece dos recetas y una silueta propia.
Los nuevos recursos tienen modelos pequeños reconocibles según su función.

Se mantienen compras con créditos y ventas; no se introduce inventario de
construcción, energía obligatoria ni consumo de piezas para mejoras. Niveles
1–5 preservados; niveles 6/7/8 a $10.000/$25.000/$60.000 acumulados. Precios y
tiempos iniciales requieren prueba de ritmo en Studio. Recetas ficticias de juego.
Todas tienen como máximo dos ingredientes distintos, cantidades de 1–2 y una
salida: compatibles con las capacidades actuales. Dos entradas laterales para
mezcladoras y una trasera para transformadoras; salida siempre +Z local.

## Entrega y criterios

Archivo .rbxlx, guía española y catálogo de recetas en ZIP descargable. Todos
los recursos seleccionables en filtros, catálogo con miniaturas y descripción
derecha, recetas mediante G. Conservar demos anteriores y añadir una prueba de
expansión claramente identificada, sólo disponible bajo las mismas condiciones
que las demos actuales, sin alterar la economía de la partida normal.

Pruebas ejecutan módulos Luau reales: alcance de recetas, consumo y bloqueo,
venta, compras y desbloqueos, conexiones en cuatro rotaciones, modelos de carga,
catálogo. Comparación XML debe preservar geometría y scripts ajenos. No se
afirma validación de render, física o rendimiento de Roblox Studio desde CLI.
