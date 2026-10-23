# Matterloom Construction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Construir la primera etapa: parcela y descomponedor colocable, girable, movible y retirable.
**Architecture:** Reglas y estado Luau puros; adaptador Roblox autoritativo en servidor; cliente con selección, previsualización y botones. Modelos de piezas creados por código, sin dependencias de assets.
**Tech Stack:** Roblox Luau, CLI Luau 0.744, Rojo 7.6.1.
**Spec:** docs/superpowers/specs/2026-10-23-construction-design.md

## Global Constraints

- Parcela de 48 × 48 casillas de 4 studs; máquina de 2 × 2 casillas.
- Giros de 90°, máximo 64 máquinas y ocho parcelas por servidor.
- Validación autoritativa, sin compras, guardado, producción o logística funcional.
- Botones en español, PC y táctil; estado de prueba por sesión.
- Usar el checkout aislado existente; no crear worktrees.

## Review Focus

- Órdenes malformadas o pertenencia incorrecta: rechazar sin modificar estado.
- Mover hacia un solapamiento o fuera del borde: conservar posición e ID originales.
- Rotación: conectores, límites de huella y modelo deben compartir convención.
- Interfaz: clic/tap en UI no debe colocar ni seleccionar objetos del mundo.
- Ciclo de vida: respuesta tardía, respawn y salida de jugador no dejan objetos huérfanos.

### Task 1: Reglas autoritativas de construcción

**Files:** src/shared/Construction.luau; tests/construction.spec.luau; scripts/check.sh.
**Interfaces:** Construction.newState(ownerId), snapshot(state), apply(state, actorId, command)
→ boolean, code; canPlace(state,x,z,rotation,ignoreId) → boolean, code;
worldToCell(worldX,worldZ,originX,originZ); ports(x,z,rotation).

- [x] Escribir pruebas de límites, solapamiento, giro de conectores, mover/retirar,
  propietarios, datos malformados, respuestas inmutables y capacidad; observar fallo.
- [x] Implementar módulo puro con validación antes de mutar y sin yields.
- [x] Ejecutar CLI Luau: todos los casos deben pasar; analizar tipos del módulo puro.

### Task 2: Parcela y adaptador Roblox

**Files:** src/shared/MachineVisual.luau; src/server/BuildServer.luau;
src/server/init.server.luau; default.project.json; tests/studio-smoke.server.luau.
**Interfaces:** MachineVisual.create(parent,record,origin,preview) → Model;
MachineVisual.pivot(model,record,origin); BuildServer.start().
Remotes: GetState devuelve snapshot; Command recibe orden y emite respuesta con estado.

- [x] Escribir prueba Studio de creación, rotación, propiedad y eliminación de modelos.
- [x] Integrar reglas del Task 1 con parcelas por jugador, rate limit y render replicado.
- [x] Compilar todos los scripts con luau-compile y empaquetar con Rojo; inspeccionar
  el árbol de salida. Documentar que la prueba de motor espera ejecución en Studio.

### Task 3: Controles de construcción y entrega

**Files:** src/client/BuildController.luau; src/client/BuildUI.luau;
src/client/init.client.luau; README.md.
**Interfaces:** BuildUI.new(callbacks) → interfaz con setMode, setStatus, setCount;
BuildController.start() conecta estado, raycast, vista previa y comandos.

- [x] Conectar botones y teclas a colocar/girar/mover/retirar/cancelar, con una sola
  orden en vuelo, mensajes de rechazo y vista previa local sin autoridad.
- [x] Verificar toda la suite Luau, sintaxis de scripts y Rojo; documentar prueba
  manual PC/táctil, multijugador y respawn en Studio.
- [x] Pedir revisión de código; corregir hallazgos importantes, volver a comprobar.
- [x] Entregar archivo .rbxlx, instrucciones y limitaciones verificadas.

## Registro

- Alcance aprobado por el usuario: empezar por el principio, no hacer todo.
- Ejecución directa en este checkout; rama feat/matterloom-construction.
- Interfaz compartida revisada: cliente usa snapshots, servidor usa estado autoritativo;
  ambos consumen las mismas coordenadas (x,z), orientación (0..3) e IDs.

- Task 1: complete — 18 pruebas iniciales observadas fallar antes de implementar;
  luego 18/18, análisis estricto correcto.
- Task 2: complete — integración y artefacto compilados. Prueba de motor escrita
  y con sintaxis verificada, pendiente de ejecutar en Studio (no disponible aquí).
- Task 3: complete — controles y documentación implementados; revisión independiente
  realizada, comprobaciones completas con scripts/check.sh correctas.
- Revisión final: formato de red con huecos corregido mediante array denso y
  reconstrucción por ID. Regresión observada fallar y pasar; suite 19/19.
- Revisión final: conversión de puntero corregida con ScreenPointToRay tras restar
  inset. Test del adaptador observado fallar y pasar (dos casos).
- Revisión final: Escape cancela mediante MenuOpened incluso si Roblox consume la
  tecla. Verificación del evento y de la interfaz pendiente de Studio.
- Validación final: 19 pruebas de construcción y dos casos de puntero; análisis de
  módulos puros, compilación de sintaxis Luau y estructura de ocho scripts en el
  archivo .rbxlx. No se afirma ejecución de Roblox Studio ni prueba visual.
- Fuera de alcance, de acuerdo con la petición: producción, logística, economía,
  guardado, más máquinas, gamepad y pruebas de carga para publicación.
