# Ventreo

## Badges

![Estado del proyecto](https://img.shields.io/badge/estado-en%20desarrollo-blue.svg)
![Versión](https://img.shields.io/badge/version-0.1.0-orange.svg)
![Licencia](https://img.shields.io/badge/licencia-MIT-green.svg)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-organizacion/ventreo.git
   cd ventreo
   ```
2. Crea y activa tu entorno virtual preferido (opcional pero recomendado).
3. Instala las dependencias declaradas para el entorno de ejecución:
   ```bash
   pip install -r requirements.txt
   ```
   > Si aún no existe un `requirements.txt`, crea uno acorde a las necesidades del proyecto antes de continuar.

## Desarrollo

- Revisa la guía oficial en [`docs/GUIA_DESARROLLO_PROFESIONAL.md`](docs/GUIA_DESARROLLO_PROFESIONAL.md) para conocer estándares, prácticas y checklist de entregables.
- Ejecuta las pruebas automatizadas localmente con:
  ```bash
  pytest
  ```
  El directorio [`tests/`](tests/) queda reservado para las suites de pruebas unitarias y de integración.
- Utiliza ramas descriptivas y commits atómicos siguiendo la convención `tipo/scope-descripcion`.

## CI/CD

- Configura pipelines en tu herramienta preferida (por ejemplo, GitHub Actions o GitLab CI) que incluyan pasos de linting, pruebas y despliegue.
- Cada push a `main` debe disparar la verificación automática del pipeline y bloquear el merge si alguna verificación falla.
- Define entornos diferenciados para `staging` y `producción`, automatizando despliegues continuos cuando sea viable.

## Reglas de la guía

La guía profesional establece las siguientes reglas principales:

1. **Calidad antes que velocidad.** Ningún código se fusiona sin revisión y pruebas.
2. **Documentación continua.** Toda funcionalidad debe ir acompañada de notas en la guía o en la documentación técnica.
3. **Comunicación transparente.** Los cambios relevantes deben anunciarse en los canales del equipo junto con sus impactos.
4. **Mentoría activa.** Quien lidera un esfuerzo se responsabiliza de acompañar a quienes se sumen.

Consulta la guía completa para profundizar en cada punto y en los procesos asociados.

## Troubleshooting

- **Faltan dependencias:** asegúrate de haber ejecutado `pip install -r requirements.txt` y de que el entorno virtual esté activo.
- **Errores en pruebas:** revisa la salida de `pytest -vv` y corrige los casos reportados antes de abrir un pull request.
- **Problemas de formato:** integra herramientas como `black`, `flake8` o `ruff` y ejecuta `pre-commit run --all-files`.
- **Configuraciones locales inconsistentes:** elimina archivos temporales y reinstala dependencias con `pip install --force-reinstall -r requirements.txt`.

## Roadmap

1. Definir alcance funcional inicial y arquitectura de referencia.
2. Implementar pipeline CI/CD mínimo viable con lint y pruebas.
3. Construir módulo de autenticación y autorización.
4. Publicar documentación de API y patrones de integración.
5. Planificar versión 1.0 con criterios de aceptación y métricas de adopción.

---

> Este README se actualizará conforme avance el proyecto y se integren nuevos aprendizajes del equipo.
