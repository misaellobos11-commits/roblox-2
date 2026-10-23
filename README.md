# roblox-2

Base de un proyecto Roblox generado con Rojo 7.6.1 y scripts Luau.

## Estructura

- `src/server`: scripts del servidor.
- `src/client`: scripts del cliente.
- `src/shared`: módulos compartidos.
- `default.project.json`: distribución de los scripts y plataforma inicial.

## Entorno en la nube

Rojo está instalado en `/workspace/tools/bin/rojo`. Para compilar:

```bash
cd /workspace/roblox-2
export PATH="/workspace/tools/bin:$PATH"
mkdir -p build
rojo build default.project.json -o build/roblox-2.rbxlx
```

El resultado `build/roblox-2.rbxlx` se puede abrir en Roblox Studio.
La compilación comprueba que Rojo puede empaquetar el proyecto; no ejecuta
los scripts ni comprueba la jugabilidad. Esta base aún no incluye pruebas automatizadas.

## Roblox Studio

Roblox Studio requiere Windows o macOS. Instala Rojo 7.6.1 y su plugin en
ese equipo, clona el repositorio y ejecuta desde su carpeta:

```bash
rojo build -o roblox-2.rbxlx
rojo serve
```

Abre el archivo generado en Studio, conecta el plugin Rojo al servidor local
y usa Play para probar los scripts. El servidor en la nube se valida
internamente; no se presupone una conexión desde Studio a este entorno.

Documentación: https://rojo.space/docs/v7/
