# Matterloom 8.22 — acabado visual de las máquinas

**Solicitud:** mejorar un poco el diseño de la maquinaria nueva de 8.21.
**Alcance:** los 20 modelos nuevos y sus miniaturas automáticas. Mantener
máquinas importadas, recursos transportados, recetas, puertos, economía,
mapa, HUD y simulación. El usuario solicita ejecución; se aplica un acabado
industrial coherente con los modelos originales sin abrir otra ronda de diseño.

**Diseño:** plataformas escalonadas y biseladas, carcasas con paneles de acceso,
protecciones, uniones de tubería y detalles específicos del mecanismo.
Grafito y metal con acentos de familia contenidos. Sin luces adicionales,
física ni scripts de animación. Menos de 100 partes visibles por máquina,
huella dentro de las dos casillas y bocas generadas por el catálogo existente.

## Ejecución

- [ ] Añadir `stage8/expansion/polish_822.py`: decoración y acabados de los
  modelos existentes, sin modificar el registro de 8.21.
- [ ] Añadir `stage8/build_822.py`: sustituir exclusivamente la sección de
  modelos de expansión de MachineVisual y la etiqueta de versión.
- [ ] Crear galería de modelos y revisar render auxiliar, incluidos primeros
  planos de máquinas pequeñas y dos entradas laterales.
- [ ] Ejecutar regresiones existentes de modelos, miniaturas, cargas, recetas
  y cintas; comprobar límites de huella y presupuesto de partes.
- [ ] Revisar el cambio, empaquetar .rbxlx/guía/vista previa y comprobar la
  descarga pública exacta. No fusionar main.

**Límite de validación:** CLI y Blender no sustituyen Roblox Studio para render,
rendimiento o interacción real. Usar la demo de 20 máquinas para la prueba manual.
