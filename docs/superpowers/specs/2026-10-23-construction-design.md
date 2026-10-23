# Matterloom — etapa 1: terreno y construcción

Fuente: Matterloom_Diseno_Conceptual_Roblox.docx, fases 01 y primer paso del orden de trabajo.
El usuario eligió empezar por el principio y no implementar todo el juego.

## Entrega

Una parcela por jugador de 48 × 48 casillas de 4 studs (192 × 192 studs).
Un solo tipo de máquina: un descomponedor de prueba de 2 × 2 casillas,
con entrada y salida señalizadas y rotación en incrementos de 90°.
Colocar, seleccionar, mover y retirar. Previsualización transparente válida/inválida
con texto además del color. Las operaciones válidas las decide el servidor.
Interfaz en español, botones para ratón y pantalla táctil; R gira, Escape cancela.
Se permiten hasta 64 máquinas por parcela para probar colisiones y distribución.

## Enfoque

Se considera una maqueta visual sin validación frente a un prototipo integrado con
reglas compartidas y validación autoritativa. Se adopta el prototipo integrado:
permite comprobar el encaje real y rechazar órdenes manipuladas desde esta etapa.
El alcance es el primer paso, más pequeño que el circuito productivo completo
propuesto anteriormente y que el usuario pidió aplazar.

Un módulo Luau puro contiene geometría, estado y validaciones para ejecutarlo tanto
en Roblox como en la CLI de Luau. El cliente muestra la vista previa; el servidor
mantiene las máquinas, crea los modelos y valida pertenencia, límites y ocupación.
Cada máquina usa un ID monotónico por parcela. Mover conserva el ID; una operación
rechazada conserva la construcción original. Los conectores rotan con el modelo.

## Decisiones de implementación

- Cámara y movimiento normales de Roblox; se construye apuntando al suelo propio.
- En móvil, tocar el terreno fija la vista previa y un botón confirma; tocar una
  máquina propia la selecciona. No se confirma automáticamente al tocar el mundo.
- Construcción gratuita de prueba. No se simulan créditos, inventarios ni procesos.
- Estado solamente durante la sesión; salir elimina la parcela. No hay guardado aún.
- Ocho parcelas como máximo por servidor, con separación de 32 studs; rechazo claro
  si la capacidad se agota. Cada jugador reaparece junto a su propia parcela.
- Máquina industrial sencilla hecha con piezas de Roblox; sin assets externos.

## Aceptación

1. Puede colocarse en las esquinas válidas, nunca fuera del terreno ni sobre otra.
2. Giro de 90° cambia entrada/salida; cuatro giros recuperan la orientación inicial.
3. Mover preserva el ID y no pierde la máquina al fallar o cancelar.
4. Retirar libera las casillas; las órdenes repetidas no recrean máquinas.
5. Un jugador no modifica el terreno ajeno, incluso enviando órdenes arbitrarias.
6. Validaciones rechazan tipos incorrectos, NaN, infinitos y coordenadas fraccionarias.
7. Rojo genera un lugar con scripts; pruebas Luau verifican las reglas reales.
8. Play y controles de PC/móvil se comprueban en Studio; la CLI no sustituye al motor.

Quedan fuera: cintas funcionales, materia, producción, energía, economía,
investigación, contratos, persistencia y el resto del catálogo.
