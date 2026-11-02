# Verificación 8.22

Base: 88bdc41 / entrega 8.21. Arte inicial: 15ea4d4.

`bash stage8/check_822.sh` verifica el archivo generado, no sólo datos auxiliares:

- Sustitución exacta de la sección de modelos de expansión en MachineVisual y
  etiqueta de versión en BuildUI. XML restante idéntico a 8.21.
- Veinte siluetas distintas en ochenta colocaciones; bocas, selección y huella.
- Máximo de 77 partes visibles por máquina. Sin nuevas luces o animaciones.
- Miniaturas y selección del catálogo, 54 modelos de recursos transportados,
  53 recetas y 212 entregas giradas; demo finita de 240 ventas.
- Regresiones de animación de cintas, divisores, filtros y ascensores.
- Compilación de los dos scripts modificados y round-trip de geometría Roblox.

Revisión independiente `review_polish_822`: preservación y flags correctos.
Hallazgo material: el aro de la ensambladora de sensores ocultaba sus lentes.
Prueba de visibilidad falló con el aro original; ambas lentes se adelantaron y
redujeron para dejar visible el borde. Prueba y suite completa pasaron después.

Galería general y detalle de seis máquinas revisados mediante Blender. Los
renders son auxiliares; no se ha ejecutado Roblox Studio. Pendiente allí:
iluminación real, rendimiento con muchas máquinas y valoración estética del usuario.
