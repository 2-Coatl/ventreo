# Guía de Desarrollo Profesional v2.0

## 1. Propósito

Esta guía proporciona un marco actualizado para coordinar el trabajo técnico, acelerar el aprendizaje colectivo y garantizar entregables de alta calidad en el proyecto **Ventreo**.

## 2. Principios Rectores

1. **Excelencia técnica sostenible:** prioriza decisiones que faciliten mantenibilidad, seguridad y rendimiento.
2. **Aprendizaje continuo:** cada iteración debe dejar evidencia documentada de lo aprendido.
3. **Colaboración empática:** fomenta un ambiente donde todas las voces sean escuchadas y se privilegie el respeto.
4. **Impacto medible:** toda iniciativa debe vincularse a métricas claras de valor para usuarios y negocio.

## 3. Roles y Responsabilidades

| Rol | Responsabilidades clave |
| --- | --- |
| Dirección técnica | Define arquitectura, revisa roadmap y habilita procesos de revisión de código. |
| Líder/a de módulo | Coordina tareas, valida entregables y gestiona riesgos técnicos en su dominio. |
| Desarrollador/a | Implementa historias, documenta cambios y participa en revisiones cruzadas. |
| QA/Testing | Diseña planes de pruebas, automatiza suites y reporta resultados al equipo. |
| DevOps | Mantiene pipelines CI/CD, monitoreo y estrategias de despliegue. |

## 4. Flujo de Trabajo

1. **Ideación:** registrar propuestas en el backlog con contexto, métricas y criterios de aceptación.
2. **Diseño técnico:** elaborar RFC breves cuando haya decisiones arquitectónicas relevantes.
3. **Implementación:** trabajar en ramas dedicadas, mantener commits atómicos y descriptivos.
4. **Revisión:** solicitar revisiones con checklist de pruebas, documentación y riesgos.
5. **Integración:** fusionar únicamente cuando las pruebas y la verificación de CI estén en verde.
6. **Retrospectiva:** documentar aprendizajes y actualizaciones en esta guía o en el conocimiento compartido.

## 5. Estándares de Código

- Estilo Python: `black`, `isort` y `ruff` como herramientas de referencia.
- Tests: utilizar `pytest` con nomenclatura `test_<funcionalidad>_<escenario>`.
- Cobertura mínima esperada: 85% del módulo modificado.
- Documentación: cada módulo nuevo requiere docstring de módulo y funciones públicas documentadas.
- Internacionalización: strings visibles para usuarios deben centralizarse en archivos de traducción.

## 6. Documentación y Comunicación

- Actualizar `README.md` cuando existan cambios en instalación, uso o arquitectura general.
- Registrar decisiones relevantes en un directorio `docs/decisiones/` con formato RFC.
- Mantener changelog semántico en `CHANGELOG.md` a partir de la versión 0.2.0.
- Utilizar canales asíncronos (por ejemplo, Slack) para anuncios y correo para decisiones formales.

## 7. CI/CD y Entornos

- Pipelines deben incluir linting, pruebas unitarias, integración y análisis de seguridad.
- Deploys a `staging` ocurren tras aprobar el PR; a `producción`, bajo ventana planificada y checklist de rollback.
- Monitorizar servicios con alertas configuradas para errores críticos y degradaciones de rendimiento.

## 8. Seguridad

- Revisar dependencias con herramientas como `pip-audit` o `safety` cada sprint.
- Aplicar políticas de mínimos privilegios en infraestructura y secretos.
- Establecer procesos de divulgación responsable para vulnerabilidades internas o externas.

## 9. Carrera y Crecimiento

- Definir planes individuales de aprendizaje vinculados a objetivos del proyecto.
- Promover rotación de responsabilidades para ampliar experiencia del equipo.
- Ofrecer mentorías cruzadas y sesiones de pairing semanales.

## 10. Checklist de PR

- [ ] Historia/tarea enlazada y contexto descrito.
- [ ] Evidencias de pruebas automatizadas y manuales.
- [ ] Documentación actualizada (README, docs específicos, notas de despliegue).
- [ ] Riesgos identificados y planes de mitigación.
- [ ] Validación de accesibilidad (si aplica).

## 11. Troubleshooting Organizacional

- **Falta de claridad en prioridades:** convocar a revisión de backlog con dirección técnica.
- **Bloqueos recurrentes en CI:** escalar al rol DevOps y documentar causa raíz.
- **Desalineación entre equipos:** programar reunión de sincronización y actualizar acuerdos de trabajo.

## 12. Roadmap Formativo

1. Consolidar onboarding técnico con sesiones grabadas y documentación navegable.
2. Lanzar programa de certificaciones internas en temas clave (seguridad, performance, UX).
3. Implementar métricas de satisfacción del equipo y revisar acciones trimestralmente.
4. Preparar plan de sucesión para roles críticos con documentación de procesos y contactos.

## 13. Actualizaciones de la Guía

- Versionado semántico siguiendo `Mayor.Menor.Parche` (esta versión: 2.0.0).
- Registrar cambios relevantes en la sección "Historial".

## 14. Historial

- **2.0.0 (2024-04-01):** Actualización completa alineada con roadmap y prácticas de CI/CD reforzadas.
- **1.0.0 (2023-09-15):** Publicación inicial del marco profesional.

---

Para sugerencias o aportes, abre un issue en el repositorio con la etiqueta `guia-profesional`.
