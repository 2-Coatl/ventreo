# Flujo de datos y pipeline del monolito modular

Este documento resume cómo circula la información entre los módulos del monolito y qué artefactos participan en cada etapa del pipeline financiero.

## Visión general

El flujo parte de la autenticación y resolución de permisos, continúa con el registro de operaciones financieras, alimenta dashboards y termina en alertas y auditoría. Todos los módulos se despliegan dentro del mismo proyecto Django pero se organizan como dominios independientes que exponen APIs de sólo lectura.

```
Identidad → Control de acceso → Finanzas → Dashboards → Notificaciones
             ↓                        ↓             ↓
          Auditoría ─────────────────→──────────────┘
```

## Etapas del pipeline financiero

| Fase | Propósito | Artefactos clave |
| --- | --- | --- |
| Acceso inicial | Validar identidad y obtener roles para habilitar pestañas del libro. | `finance.domain.ACCESS_PHASES`, `identity.models.Role`, `access_control.models.SheetPermission`. |
| Inversión (FASE 2) | Registrar gastos de capital y operar el flujo de aprobaciones. | `finance.domain.INVESTMENT_WORKFLOW`, `finance.models.Workflow`. |
| Costos operativos (FASE 3) | Consolidar costos fijos, variables y nómina para el control presupuestal. | `finance.domain.COST_STRUCTURE`, `finance.models.Workflow`. |
| Ingresos (FASE 4) | Proyectar ventas, cohortes y métricas recurrentes. | `finance.domain.REVENUE_MODEL`, dashboards de métricas comerciales. |
| Flujo de efectivo (FASE 5) | Calcular liquidez, runway y generar tableros ejecutivos. | `finance.domain.CASH_FLOW`, `dashboards.models.Dashboard`. |
| Cumplimiento fiscal (FASE 6) | Gestionar impuestos, depreciaciones y recordatorios. | `finance.domain.TAX_COMPLIANCE`, `notifications.models.AlertRule`. |
| Planeación de escenarios (FASE 7) | Evaluar escenarios y simulaciones Monte Carlo. | `finance.domain.SCENARIO_PLANNING`, `dashboards.configs.DASHBOARD_LAYOUTS`. |
| Dashboards por persona (FASE 9) | Entregar indicadores y acciones rápidas según el rol. | `finance.domain.DASHBOARD_VIEWS`, `dashboards.models.DashboardKPI`. |

## Flujo detallado de datos

1. **Autenticación y roles.** Un usuario se autentica y la capa de identidad entrega los roles activos (`identity.models.Role`, `identity.services.RoleAssignment`).
2. **Resolución de permisos.** Con los roles, `access_control.services.resolve_sheet_permissions` determina qué pestañas y acciones están habilitadas. Este resultado desbloquea las fases correspondientes del pipeline (`finance.models.Phase`).
3. **Registro de operaciones.** Los equipos de finanzas alimentan las hojas descritas en `finance.domain`: inversiones, costos, ingresos y simulaciones. Cada workflow define dependencias de hojas y roles aprobadores (`finance.models.Workflow`).
4. **Cálculo y tableros.** Los resultados se consolidan en `finance.domain.CASH_FLOW` y se proyectan en dashboards configurados en `dashboards.models` y `dashboards.configs`. Cada dashboard filtra métricas y acciones para la audiencia definida.
5. **Alertas.** Las condiciones críticas del flujo de efectivo o del calendario fiscal generan reglas en `notifications.models.AlertRule`; los canales configurados en `AlertChannel` envían la señal al rol correspondiente.
6. **Auditoría.** Toda interacción relevante se registra como `audit.models.AuditEvent` o en el log in-memory de `audit.services.AuditLog`. Esto permite rastrear qué usuario consultó, editó o aprobó cada hoja.

## Relaciones entre módulos

- **Identidad ↔ Control de acceso:** Los modelos de permisos referencian roles por clave primaria, garantizando consistencia en la matriz RBAC (`SheetPermission.role`).
- **Control de acceso ↔ Finanzas:** Cada fase del pipeline referencia las hojas protegidas por la matriz de permisos, asegurando que sólo los roles autorizados puedan operar.
- **Finanzas ↔ Dashboards:** Los dashboards consumen métricas calculadas en las hojas de flujo de efectivo, ingresos y escenarios.
- **Finanzas ↔ Notificaciones:** Las reglas de alerta monitorizan condiciones de cashflow e impuestos declaradas en las hojas financieras.
- **Todos ↔ Auditoría:** Cada acción relevante genera eventos que pueden consultarse vía API para auditorías internas o externas.

## Consideraciones para la documentación de infraestructura

- El proyecto es un **monolito modular**: todas las apps se ejecutan en un único despliegue Django, pero cada módulo encapsula su dominio y expone sólo APIs de consulta.
- Los frameworks (Django REST Framework, ORM) se utilizan directamente en los módulos externos; una futura capa de casos de uso permitiría desacoplarlos y hacer que el framework funcione como plugin.
- Las dependencias apuntan hacia la identidad y la definición de dominio (`finance.domain`), que operan como contrato compartido para poblar la base de datos o generar documentación.
