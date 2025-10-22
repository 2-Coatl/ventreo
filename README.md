# ventreo

## Entorno de desarrollo en contenedor

Este repositorio incluye configuración para [Dev Containers](https://containers.dev/) en `.devcontainer/`. Los pasos automatizados tras crear el contenedor se pueden ejecutar manualmente con:

```bash
bash .devcontainer/post-create.sh
```

El script deja un registro detallado en `.devcontainer/post-create.log` con el resultado de cada intento de instalación y actualización. Durante la verificación en este entorno sin acceso a los repositorios APT ni al índice público de Python, se observaron intentos fallidos de actualización mediante `apt-get` y `pip`. Estos fallos quedan documentados en el log, mientras que el flujo continúa hasta completarse. Esto permite revisar rápidamente los comandos ejecutados y su resultado al configurar el contenedor.
