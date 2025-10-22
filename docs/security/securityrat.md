# Guía de Integración SecurityRAT - Modelo Financiero Ventreo

Esta guía complementa la documentación de pipeline (`docs/data_flow_pipeline.md`) y el catálogo de casos de uso (`docs/use_cases.md`) explicando cómo operacionalizar OWASP SecurityRAT dentro del contexto del monolito modular de Ventreo.

---

## 1. Objetivo

- **Centralizar requisitos ASVS** asociados a cada flujo de negocio documentado (UC-001 – UC-022).
- **Automatizar el seguimiento** de controles de seguridad y cumplimiento vinculados al modelo financiero RBAC.
- **Facilitar auditorías** proporcionando evidencia exportable desde SecurityRAT hacia `docs/security/`.

---

## 2. Preparación del entorno

1. **Seleccionar modalidad de despliegue**
   - Docker: `docker run -p 8080:8080 securityrat/securityrat:latest`
   - JDK 11: descargar `securityrat.war` y ejecutar `java -jar securityrat.war`
2. **Crear proyecto `ventreo-rbac`**
   - Configurar atributos personalizados: tamaño de empresa, bundle de roles, severidad de alertas.
   - Importar slugs desde `identity/models.py` y `notifications/models.py`.
3. **Habilitar integración con repositorio**
   - Definir carpeta `docs/security/securityrat_exports/` para evidencias.
   - Versionar los reportes exportados (`json`, `xlsx`) por liberación.

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

---

## 5. Flujo operativo recomendado

1. **Planificación:** al crear una nueva funcionalidad, asignar requisitos SecurityRAT en base al caso de uso afectado.
2. **Ejecución:** actualizar el estado del requisito (To Do → In Progress → Done) conforme se implementa y prueba.
3. **Verificación:** exportar el tablero de requisitos y adjuntarlo en el PR junto con referencias a `docs/use_cases/`.
4. **Auditoría:** en cada liberación, ejecutar `make securityrat-export` (script sugerido) para guardar evidencias en `docs/security/securityrat_exports/YYMMDD/`.

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
