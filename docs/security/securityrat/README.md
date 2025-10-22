# SecurityRAT local helper

Este directorio encapsula el entorno automatizado para ejecutar SecurityRAT mediante Vagrant, Docker y Docker Compose **sin depender de que el host tenga Docker instalado**.

## Componentes

- `Vagrantfile`: levanta una VM Ubuntu, instala Docker Engine + plugin `docker compose` y ejecuta el stack definido en `docker-compose.yml`.
- `docker-compose.yml`: construye la imagen local usando el `Dockerfile`, publica el puerto 8080 y comparte `../securityrat_exports` para persistir evidencias.
- `Dockerfile`: permite fijar la etiqueta de SecurityRAT a través del argumento `SECURITYRAT_IMAGE` (ver variables en `docker-compose.yml`).

Los comandos `make securityrat-*` descritos en `../securityrat.md` delegan en este directorio.
