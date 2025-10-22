# Guía de Integración SecurityRAT - Modelo Financiero Ventreo

Esta guía complementa la documentación de pipeline (`docs/data_flow_pipeline.md`) y el catálogo de casos de uso (`docs/use_cases.md`) explicando cómo operacionalizar OWASP SecurityRAT dentro del contexto del monolito modular de Ventreo.

---

## 1. Objetivo

- **Centralizar requisitos ASVS** asociados a cada flujo de negocio documentado (UC-001 – UC-022).
- **Automatizar el seguimiento** de controles de seguridad y cumplimiento vinculados al modelo financiero RBAC.
- **Facilitar auditorías** proporcionando evidencia exportable desde SecurityRAT hacia `docs/security/`.

---

## 2. Preparación del entorno

1. **Provisionar SecurityRAT con Vagrant + Docker Compose**
   - Ejecutar `make securityrat-up` para crear una VM Ubuntu, instalar Docker Engine y levantar el stack definido en `docs/security/securityrat/docker-compose.yml`.
   - Validar disponibilidad en `http://localhost:8080` y revisar logs con `make securityrat-logs` en caso de incidentes.
   - Detener la VM con `make securityrat-halt` o destruirla usando `make securityrat-destroy` cuando se requiera un entorno limpio.
2. **(Opcional) Alternativas manuales**
   - Docker directo en el host (si está disponible): `docker run -p 8080:8080 securityrat/securityrat:latest`.
   - JDK 11: descargar `securityrat.war` y ejecutar `java -jar securityrat.war`.
3. **Crear proyecto `ventreo-rbac`**
   - Configurar atributos personalizados: tamaño de empresa, bundle de roles, severidad de alertas.
   - Importar slugs desde `identity/models.py` y `notifications/models.py`.
4. **Habilitar integración con repositorio**
   - Definir carpeta `docs/security/securityrat_exports/` para evidencias (volumen compartido con el contenedor).
   - Versionar los reportes exportados (`json`, `xlsx`) por liberación utilizando `make securityrat-export` cuando se requiera copiar artefactos desde el contenedor.

> **Tip:** tanto la imagen (`SECURITYRAT_IMAGE`) como los `JAVA_OPTS` (`SECURITYRAT_JAVA_OPTS`) pueden sobreescribirse al ejecutar `make securityrat-up`, por ejemplo: `SECURITYRAT_IMAGE=securityrat/securityrat:2.12 make securityrat-up`.

---

## 3. Generar requisitos iniciales

| Parámetro SecurityRAT | Valor recomendado | Justificación |
| --- | --- | --- |
| Capítulo ASVS | V1–V14 (según flujo) | Cobertura total del modelo financiero |
| Nivel ASVS | L2 | El modelo procesa datos sensibles y requiere segregación de funciones |
| Autenticación SSO | Sí, cuando se integra con la plataforma corporativa | Mantener consistencia con UC-001 |

**Procedimiento:**
1. Iniciar sesión en la demo o instancia local (credenciales en [OWASP SecurityRAT](https://owasp.org/www-project-securityrat/)).
2. Seleccionar capítulos relevantes (por ejemplo V4 para UC-019, V7 para UC-022).
3. Generar el artefacto de requisitos y guardarlo como `ventreo-rbac-L2.json`.

---

## 4. Mapeo con casos de uso

| Caso de uso | Capítulos ASVS sugeridos | Etiquetas SecurityRAT |
| --- | --- | --- |
| UC-001 Validar acceso | V1, V4, V7 | `rbac`, `login`, `auditoria` |
| UC-002 Gestionar inversión | V6, V11 | `workflow`, `aprobaciones` |
| UC-003 Ajustar presupuesto | V4, V8 | `costos`, `controller` |
| UC-004 Actualizar ingresos | V4, V11 | `pricing`, `cfo` |
| UC-005 Monitorear cashflow | V8, V9 | `alertas`, `cashflow` |
| UC-006 Cumplir obligaciones fiscales | V6, V7, V9 | `fiscal`, `contador` |
| UC-007 Gestionar escenarios | V1, V4 | `escenarios`, `analista` |
| UC-008 Dashboards por persona | V1, V4, V8 | `dashboards`, `persona` |
| UC-009 Configurar parámetros | V1, V4 | `setup`, `parametros` |
| UC-010 Seleccionar bundle de roles | V4 | `identidades`, `bundles` |
| UC-011 Revisar matriz de permisos | V4, V7 | `permisos`, `auditoria` |
| UC-012 Consultar fases pipeline | V1, V11 | `pipeline`, `documentacion` |
| UC-013 Supervisar reglas alerta | V7, V9 | `alert_rules`, `governance` |
| UC-014 Configurar canales alerta | V9 | `alert_channels`, `infra` |
| UC-015 Monitorear bitácora | V7 | `audit_log`, `compliance` |
| UC-016 Catalogar roles | V4 | `roles_catalog`, `seguridad` |
| UC-017 Consolidar roles | V4 | `role_assignment`, `onboarding` |
| UC-018 Identificar rol máximo | V4 | `privilege`, `risk` |
| UC-019 Calcular permisos hoja | V4 | `sheet_permissions`, `control` |
| UC-020 Derivar destinatarios | V7, V9 | `alert_recipients`, `notificaciones` |
| UC-021 Auditar reglas por rol | V7, V11 | `alert_rules_audit`, `governance` |
| UC-022 Bitácora en memoria | V7 | `auditlog_temporal`, `incidentes` |

> **Sugerencia:** crear un atributo personalizado `use_case` en SecurityRAT y asociarlo al código correspondiente (`UC-0XX`).

### 4.1 Implementación operativa de los casos de uso

1. **Crear un requerimiento base** en SecurityRAT por cada caso de uso documentado en `docs/use_cases/`. Para acelerar el proceso:
   - Utiliza la plantilla `ventreo-rbac-L2.json` generada en la sección 3 y duplica la fila correspondiente.
   - Completa los metadatos `use_case`, `owner` y `milestone` siguiendo la tabla anterior.
2. **Relacionar controles ASVS específicos** mediante etiquetas adicionales:
   - Para requisitos críticos (por ejemplo UC-019 o UC-022) agrega la etiqueta `critical` y asigna un `Due Date` en el mismo sprint.
   - Cuando un caso de uso involucre integraciones externas (UC-006, UC-020), añade una referencia cruzada al proveedor externo en el campo `External Reference`.
3. **Vincular evidencia de implementación** desde el repositorio:
   - Añade el enlace al archivo del caso de uso (`docs/use_cases/UC-0XX-*.md`) dentro del campo `Description` de SecurityRAT.
   - Registra el PR o commit que satisface el requisito en el campo `Implementation Ticket` para simplificar auditorías.
4. **Automatizar el seguimiento dentro del sprint**:
   - Ejecuta `make securityrat-export` al cerrar cada historia para versionar la evidencia generada en `docs/security/securityrat_exports/<timestamp>/`.
   - Revisa los resultados con `make securityrat-logs` cuando se modifiquen requisitos o etiquetas para validar que el contenedor siga activo.
5. **Sincronizar los estados** antes de liberar:
   - Marca en SecurityRAT los requisitos asociados a los casos de uso completados con estado `Done`.
   - Actualiza el catálogo de casos de uso indicando los controles implantados y referencia el archivo exportado desde SecurityRAT en la sección de auditoría del PR.

---

## 5. Flujo operativo recomendado

1. **Planificación:** al crear una nueva funcionalidad, asignar requisitos SecurityRAT en base al caso de uso afectado.
2. **Ejecución:** actualizar el estado del requisito (To Do → In Progress → Done) conforme se implementa y prueba.
3. **Verificación:** exportar el tablero de requisitos y adjuntarlo en el PR junto con referencias a `docs/use_cases/`.
4. **Auditoría:** en cada liberación, ejecutar `make securityrat-export` para guardar evidencias en `docs/security/securityrat_exports/YYMMDD-HHMMSS/`.

### 5.1 Checklist automatizado con Make

| Tarea | Comando | Resultado esperado |
| --- | --- | --- |
| Provisionar SecurityRAT | `make securityrat-up` | VM con Docker Compose ejecutando `ventreo-securityrat` |
| Revisar logs | `make securityrat-logs` | Últimos eventos de `docker compose logs` dentro de la VM |
| Exportar evidencias | `make securityrat-export` | Copia de `/opt/securityrat/exports` a `docs/security/securityrat_exports/<timestamp>/` |
| Detener servicio temporalmente | `make securityrat-halt` | VM apagada (se conserva el volumen de exportaciones) |
| Limpiar entorno | `make securityrat-destroy` | VM destruida junto con los contenedores |

> **Análisis de tareas:** antes de cada liberación confirmar que (1) el contenedor está activo, (2) los requisitos afectados en SecurityRAT están en estado "Done", (3) los artefactos exportados se almacenaron en el timestamp correcto y (4) los casos de uso vinculados (`UC-0XX`) quedaron documentados en el PR correspondiente. El target `make securityrat-export` ejecuta `docker compose cp` desde la VM, por lo que no es necesario disponer de Docker en el host.

---

## 6. Integración con SecurityCAT (futuro)

- SecurityRAT expone una API para construir pruebas automáticas.
- Mapear reglas críticas (UC-019, UC-020, UC-022) como candidatas a automatización.
- Planificar prototipo de SecurityCAT que valide el cumplimiento del requisito antes de liberar versiones.

---

## 7. Buenas prácticas

- Mantener alineados los catálogos de roles (`UC-016`) y alertas (`UC-021`) con los atributos de SecurityRAT.
- Versionar cualquier cambio en requisitos dentro del repositorio (`docs/security/`).
- Revisar la [documentación oficial](https://securityrat.github.io/) ante actualizaciones del proyecto OWASP.

---

## 8. Recursos adicionales

- [OWASP SecurityRAT](https://owasp.org/www-project-securityrat/)
- [Documentación SecurityRAT](https://securityrat.github.io/)
- [Video OWASP Spotlight](https://youtu.be/ythaa6nRa0Y)
- [SecurityCAT](https://github.com/SecurityRAT/SecurityCAT)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)

---

**Última actualización:** sincronizada con catálogo de casos de uso UC-001–UC-022.
