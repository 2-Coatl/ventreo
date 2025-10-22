# Catálogo de Casos de Uso - Modelo Financiero Ventreo v3.3 RBAC

Este documento actúa como índice maestro. Cada caso de uso está descrito en un artefacto independiente siguiendo el formato de la guía proporcionada por el equipo (información general, precondiciones, flujos, reglas de negocio, etc.).

| Código | Nombre | Dominio | Actores clave | Artefacto |
| --- | --- | --- | --- | --- |
| UC-001 | Validar acceso RBAC y preparar entorno | Seguridad | Super Admin, CFO, CEO, Contador | [docs/use_cases/UC-001-validar-acceso-rbac.md](use_cases/UC-001-validar-acceso-rbac.md) |
| UC-002 | Gestionar propuesta de inversión CapEx/Opex | Finanzas corporativas | Controller, CFO, CEO | [docs/use_cases/UC-002-gestionar-inversion.md](use_cases/UC-002-gestionar-inversion.md) |
| UC-003 | Ajustar presupuesto operativo por área | Control presupuestal | Gerente, Controller, CFO, CEO | [docs/use_cases/UC-003-ajustar-presupuesto-operativo.md](use_cases/UC-003-ajustar-presupuesto-operativo.md) |
| UC-004 | Actualizar modelo de ingresos y precios | Revenue Management | CFO, CEO, Analista | [docs/use_cases/UC-004-actualizar-modelo-ingresos.md](use_cases/UC-004-actualizar-modelo-ingresos.md) |
| UC-005 | Monitorear flujo de efectivo y alertas | Liquidez | CFO, Controller, CEO | [docs/use_cases/UC-005-monitorear-cashflow-alertas.md](use_cases/UC-005-monitorear-cashflow-alertas.md) |
| UC-006 | Cumplir obligaciones fiscales y cierre contable | Compliance | Contador, CFO, CEO, Auditor | [docs/use_cases/UC-006-cumplir-obligaciones-fiscales.md](use_cases/UC-006-cumplir-obligaciones-fiscales.md) |
| UC-007 | Gestionar escenarios y simulaciones | Planeación estratégica | Analista, CFO, CEO | [docs/use_cases/UC-007-gestionar-escenarios.md](use_cases/UC-007-gestionar-escenarios.md) |
| UC-008 | Consultar dashboards personalizados por persona | Business Intelligence | CEO, CFO, Contador, Gerente | [docs/use_cases/UC-008-consultar-dashboards-persona.md](use_cases/UC-008-consultar-dashboards-persona.md) |
| UC-009 | Configurar parámetros maestros del modelo | Configuración inicial | CFO, Controller, Contador | [docs/use_cases/UC-009-configurar-parametros-maestros.md](use_cases/UC-009-configurar-parametros-maestros.md) |
| UC-010 | Seleccionar bundle de roles según tamaño de empresa | Identidades | Super Admin, CEO | [docs/use_cases/UC-010-seleccionar-bundle-roles.md](use_cases/UC-010-seleccionar-bundle-roles.md) |
| UC-011 | Revisar matriz de permisos por hoja | Access Control | Super Admin, Controller, Auditor | [docs/use_cases/UC-011-revisar-matriz-permisos.md](use_cases/UC-011-revisar-matriz-permisos.md) |
| UC-012 | Consultar fases del pipeline financiero | Finanzas / Documentación | Analista, CFO, Auditor | [docs/use_cases/UC-012-consultar-fases-pipeline.md](use_cases/UC-012-consultar-fases-pipeline.md) |
| UC-013 | Supervisar reglas de alerta RBAC | Notificaciones | CFO, Controller, Super Admin | [docs/use_cases/UC-013-supervisar-reglas-alerta.md](use_cases/UC-013-supervisar-reglas-alerta.md) |
| UC-014 | Configurar canales de alerta | Infraestructura de notificaciones | Super Admin, IT | [docs/use_cases/UC-014-configurar-canales-alerta.md](use_cases/UC-014-configurar-canales-alerta.md) |
| UC-015 | Monitorear bitácora de auditoría | Auditoría y cumplimiento | Auditor, Super Admin, CFO | [docs/use_cases/UC-015-monitorear-bitacora-auditoria.md](use_cases/UC-015-monitorear-bitacora-auditoria.md) |
| UC-016 | Catalogar roles jerárquicos del RBAC | Identidades | Super Admin, Equipo de Seguridad | [docs/use_cases/UC-016-catalogar-roles-rbac.md](use_cases/UC-016-catalogar-roles-rbac.md) |
| UC-017 | Consolidar roles multifuente | Identidades | Administrador de Identidad, Mesa de Soporte | [docs/use_cases/UC-017-consolidar-roles-multifuente.md](use_cases/UC-017-consolidar-roles-multifuente.md) |
| UC-018 | Identificar el rol de mayor privilegio | Compliance | Auditor Interno, Super Admin | [docs/use_cases/UC-018-identificar-rol-maximo.md](use_cases/UC-018-identificar-rol-maximo.md) |
| UC-019 | Calcular permisos efectivos sobre una hoja | Control de accesos | Controller, Super Admin, Auditor | [docs/use_cases/UC-019-calcular-permisos-hoja.md](use_cases/UC-019-calcular-permisos-hoja.md) |
| UC-020 | Derivar destinatarios por severidad de alerta | Notificaciones | CFO, Controller, IT Ops | [docs/use_cases/UC-020-derivar-destinatarios-alertas.md](use_cases/UC-020-derivar-destinatarios-alertas.md) |
| UC-021 | Auditar reglas de alerta por rol | Notificaciones | Auditor, Super Admin, CFO | [docs/use_cases/UC-021-auditar-reglas-por-rol.md](use_cases/UC-021-auditar-reglas-por-rol.md) |
| UC-022 | Operar bitácora en memoria para respuestas rápidas | Auditoría operativa | Equipo de Incidentes, Auditor | [docs/use_cases/UC-022-operar-bitacora-in-memory.md](use_cases/UC-022-operar-bitacora-in-memory.md) |

## Cobertura del pipeline

- **Fase 0:** Seguridad y autenticación (`UC-001`).
- **Fase 1:** Configuración maestra (`UC-009`).
- **Fase 2:** Registro de inversiones (`UC-002`).
- **Fase 3:** Control de costos (`UC-003`).
- **Fase 4:** Modelo de ingresos (`UC-004`).
- **Fase 5:** Flujo de efectivo y alertas (`UC-005`, `UC-013`, `UC-014`).
- **Fase 6:** Cumplimiento fiscal (`UC-006`).
- **Fase 7:** Planeación de escenarios (`UC-007`).
- **Fase 8:** Documentación del pipeline y auditorías (`UC-012`, `UC-015`).
- **Fase 9:** Dashboards por rol (`UC-008`).
- **Capa transversal de identidad y permisos:** (`UC-010`, `UC-011`).
- **Inventario y gobernanza de roles:** (`UC-016`, `UC-017`, `UC-018`).
- **Evaluación granular de permisos y auditoría operativa:** (`UC-019`, `UC-022`).
- **Cobertura avanzada de notificaciones:** (`UC-020`, `UC-021`).

Cada artefacto referencia directamente las constantes y servicios descritos en `finance/domain.py`, `access_control`, `dashboards` y `notifications`, garantizando que la arquitectura modular comunique intención y responsabilidades según los principios de Clean Architecture.
