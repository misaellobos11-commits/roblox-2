# Dirección de producción y expansión

Actualizado el 28 de octubre de 2026 a partir de la indicación del usuario:
quiere incorporar más maquinaria y combinar más cosas en futuras etapas.

## Objetivo confirmado

La fábrica debe admitir más máquinas, materiales y combinaciones con el tiempo.
La primera cadena de producción es una introducción al sistema, no su límite.
El usuario aprobó revisar las recetas y dibujar el árbol sobre la versión 8.20.
El resultado histórico de 8.20 está en `production/ANALISIS.md` y en su visor.
Después el usuario pidió una expansión mucho mayor y ejecutarla directamente.
8.21 añade 20 máquinas, 40 recetas y 40 recursos; véase `expansion/content.py`,
`expansion/RECETAS_8_21.md` y `GUIA_PRUEBA_8_21.txt`. No añade tutoriales ni costes
de construcción con piezas. Compras con créditos y venta se conservan.

## Criterio para la siguiente etapa

Antes de añadir contenido, revisar cómo representan los módulos actuales el
catálogo, los materiales, las recetas y los puertos. Ampliar esas estructuras
para que una nueva máquina o receta no exija parches específicos en las cintas.
Conservar una convención única de orientación/entrada/salida en modelos,
previsualizaciones, colocación y simulación, tras las correcciones anteriores.

Diseñar la primera experiencia como una cadena pequeña y comprobable:
recibir materia, transportarla, venderla y aprender a procesarla para aumentar
su valor. Explicar por qué añadir un procesador y probar precios y tiempos.
La auditoría inicial está completada. La expansión añade tres niveles posteriores
sin modificar los requisitos de los cinco anteriores; falta medir el ritmo de
partida en Studio antes de cambiar los precios iniciales o introducir hitos.

Preparar la ampliación para recetas con múltiples ingredientes y productos,
máquinas con varios puertos, bifurcaciones y progresión por desbloqueos.
No suponer que todas las máquinas tendrán el mismo tamaño o una única salida.
Antes de cambiar el formato de datos, revisar compatibilidad de partidas y
ofrecer migración si fuera necesaria. Evitar una reescritura anticipada:
validar estas necesidades con una combinación real cuando toque implementar.

## Criterios de revisión futura

- Añadir una máquina debería consistir principalmente en registrar datos,
  recetas, puertos y su modelo visual.
- Ninguna máquina nueva debe invertir el sentido de las cintas ni perder la
  compatibilidad con divisores, filtros, ascensores o alturas automáticas.
- El catálogo debe mostrar nuevas máquinas con sus iconos y descripciones.
- La progresión debe dejar espacio para ramificaciones y nuevas combinaciones,
  sin fijar todavía una lista definitiva de máquinas o materiales.
