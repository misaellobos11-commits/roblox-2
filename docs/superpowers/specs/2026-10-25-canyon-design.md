# Matterloom 8.12 — complejo del cañón

El usuario pidió mejorar el terreno y aportó la imagen de referencia con
«así quiero que quede»: complejo industrial de roca arena, vegetación seca,
ocho parcelas alrededor de una plaza con núcleo cian, avenidas y terrazas.
La imagen fija la dirección visual; los valores siguientes son decisiones de
implementación para adaptarla a Roblox y a la versión 8.11 que ya funciona.

Ocho parcelas de 192 × 192 studs conservan las 48 × 48 casillas, la elección
manual, la propiedad y toda la lógica de máquinas/transporte. Centros en las ocho
posiciones exteriores de una cuadrícula con separación de 280 studs. Entradas
hacia el interior. Calles de 32 studs, aceras, plaza circular y reactor decorativo.
Paisaje de aproximadamente 1.800 studs, acantilados escalonados color arenisca,
edificios de servicio, tuberías, rampas y árboles de copa plana dispersos.
Iluminación cálida con luces cian moderadas. Geometría editable propia con Parts;
la captura es referencia artística, no garantía de fotorrealismo dentro de Roblox.

## Enfoque

Se consideró ampliar el generador que se ejecuta en Play o incluir el escenario
en el archivo. Se adopta el segundo: permite inspeccionarlo y editarlo en Studio.
El generador Python comparte las coordenadas con MapConfig. Los pisos de muestra
se sustituyen por las parcelas del servidor al iniciar, conservando su contrato.
El mapa estático permanece; el cargador no duplica geometría ni spawn.

Solo se modifican el mapa, su configuración, la presentación/entrada de parcelas
y el rótulo de versión. Se conservan máquinas, HUD de construcción, economía,
simulación y corrección de ascensores. El trabajo industrial anterior sin terminar
en src/ queda separado de esta entrega.

## Verificación

Comprobar ocho huellas libres de decoración, entradas conectadas a las calles,
spawn accesible, continuidad de rampas, presupuesto de piezas/luces, referencias XML
únicas, determinismo y conservación de los scripts ajenos al terreno. Ejecutar
la creación real de parcelas y el cargador con adaptadores y todas las regresiones
8.11. Una vista auxiliar de la geometría sirve para revisar proporciones; el
aspecto, navegación, rendimiento y multijugador reales se prueban en Studio.
