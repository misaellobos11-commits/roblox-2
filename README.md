# Matterloom — primera etapa

Prototipo de construcción basado en `Matterloom_Diseno_Conceptual_Roblox.docx`.
Esta entrega se limita al primer paso: **terreno y construcción de una máquina**.

## Abrir en Roblox Studio

1. Abre `build/Matterloom.rbxlx` con **File → Open from File** en Roblox Studio.
2. Pulsa **Play** (no Run) para crear tu jugador y su parcela.
3. Pulsa **Nueva**, apunta a tu terreno y haz clic para colocar un descomponedor.
4. Gira la vista previa con **R** o **Girar**. La entrada `IN` y la salida `OUT`
   permiten distinguir la orientación aunque la máquina ocupe siempre 2 × 2 casillas.
5. Haz clic en una máquina para seleccionarla; usa **Mover** o **Retirar**.
   **Cancelar** descarta la vista previa. Abrir el menú con Escape también cancela.

En pantalla táctil, toca el terreno para fijar la vista previa y confirma con
**Colocar**. Un toque en una máquina la selecciona. Los botones están disponibles
para girar, mover, retirar y cancelar; la zona inferior queda para desplazamiento.

La construcción es gratuita en esta prueba y **no se guarda al salir**. La máquina
es una maqueta de construcción: todavía no transforma materia ni usa energía.

## Qué incluye

- Parcela por jugador: 48 × 48 casillas de 4 studs, con líneas visibles.
- Un tipo de máquina (descomponedor 2 × 2), con conectores señalizados.
- Previsualización verde/roja con explicación en texto.
- Colocación, giro de 90°, selección, traslado y retirada.
- Servidor que valida propiedad, límites, ocupación y órdenes malformadas.
- Máximo de 64 máquinas por parcela y ocho parcelas por servidor.
- Al reaparecer, el jugador conserva su parcela durante esa sesión.

La siguiente etapa será el primer transporte de materia. Cintas, producción,
energía, ventas, contratos, investigación y persistencia no pertenecen a esta entrega.

## Herramientas en la nube

Se usan Rojo **7.6.1** y la CLI de Luau **0.744**. El instalador para Linux x86_64
verifica el SHA-256 publicado de ambas descargas oficiales:

```bash
cd /workspace/roblox-2
bash scripts/install-tools.sh
bash scripts/check.sh
```

Las herramientas quedan en `/workspace/tools`; puedes cambiar esa ubicación con
`MATTERLOOM_TOOLS`. Se requieren Bash, curl, unzip, Python 3, sha256sum y ripgrep.
Los scripts no requieren credenciales de Roblox.

`check.sh` ejecuta 19 pruebas de construcción y dos casos de coordenadas de puntero,
analiza los módulos independientes, compila la sintaxis de todos los scripts Luau,
genera el lugar y verifica que sus scripts estén en las rutas correctas.
**Estas comprobaciones no ejecutan el motor de Roblox ni validan la interfaz visual.**

## Desarrollo con Rojo

Desde la raíz del repositorio:

```bash
/workspace/tools/bin/rojo serve default.project.json
```

En un equipo Windows/macOS con Studio, instala Rojo 7.6.1 y su plugin. Clona el
repositorio y ejecuta `rojo serve` en ese equipo para sincronizar con el plugin.
El servidor de la nube se usa para comprobaciones internas y no tiene una conexión
externa de Studio configurada.

Para generar el archivo sin arrancar el servidor:

```bash
mkdir -p build
/workspace/tools/bin/rojo build default.project.json -o build/Matterloom.rbxlx
```

## Comprobación en Studio (pendiente de ejecutar en el motor)

- En Play, colocar en las cuatro esquinas; la última posición válida es (46,46).
  Un descomponedor que sobresale o se solapa debe mostrar un rechazo.
- Girar cuatro veces, comprobar las etiquetas IN/OUT y colocar otra máquina junto
  a la primera, sin dejar un hueco entre sus huellas.
- Mover una máquina sobre otra y fuera de la parcela: la original debe permanecer.
  Cancelar el traslado, incluyendo abrir el menú de Roblox, tampoco la mueve.
- Colocar tres, retirar la segunda y seleccionar/mover la tercera; retirar las
  tres y volver a construir. Los IDs estables no deben confundirse.
- En **Test → Server & Clients**, usar dos jugadores: ambos tienen parcela propia,
  no pueden cambiar las máquinas del otro y pueden construir en paralelo.
- Reaparecer, salir y volver a entrar: reaparecer conserva la sesión; salir la
  termina. Comprueba que se libera la parcela al desconectarse.
- En el emulador de dispositivos, comprobar teléfono vertical y horizontal:
  tocar UI no coloca máquinas, la vista previa sigue el punto tocado, los botones
  se leen y no bloquean los controles normales de caminar/saltar.
- En una copia de pruebas del lugar, añadir un Script temporal en ServerScriptService
  con el contenido de `tests/studio-smoke.server.luau` y ejecutar. Debe imprimir
  `Matterloom Studio model smoke: PASS`; comprueba el giro real de conectores y
  las propiedades del modelo. El script no se incluye en el lugar de entrega.

## Código

- `src/shared/Construction.luau`: cuadrícula, estado, validaciones y formato de red.
- `src/shared/MachineVisual.luau`: modelo del descomponedor y sus conectores.
- `src/server/BuildServer.luau`: parcelas, acciones autoritativas y ciclo de jugadores.
- `src/client/BuildController.luau`: selección, vista previa y órdenes.
- `src/client/BuildUI.luau`: panel y controles en español.
- `src/client/PointerRay.luau`: adaptación de coordenadas de pantalla a la cámara.

Diseño acotado: `docs/superpowers/specs/2026-10-23-construction-design.md`.
