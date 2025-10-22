# Casos de uso del monolito modular Ventreo

Este inventario describe todos los casos de uso expuestos por el monolito modular. Cada caso señala el objetivo, los actores y los artefactos del repositorio que lo habilitan.

## Identidad y roles

- **Catalogar roles de la organización.** Permite listar y consultar cada rol con su jerarquía para cimentar las políticas RBAC. Implementado mediante `identity.models.Role`, el `RoleViewSet` y sus serializadores. 
- **Recomendar paquetes de roles por etapa de la empresa.** Expone combinaciones predefinidas de roles para acelerar la configuración inicial; usa `identity.models.RoleBundle` y el `RoleBundleViewSet`. 
- **Calcular el rol de mayor privilegio.** Dado un conjunto de slugs, determina la jerarquía más alta para decisiones sensibles. Resuelto por `identity.services.highest_privilege_role`. 
- **Aplanar asignaciones de roles.** Consolida varias asignaciones individuales en un set único para alimentar motores de permisos. Resuelto por `identity.services.flatten_role_assignments`. 

## Autenticación y control de acceso

- **Evaluar permisos por hoja de cálculo.** Consulta en qué pestañas puede operar un rol o persona, expuesto por el `SheetViewSet` y respaldado por `Sheet`/`SheetPermission`. 
- **Combinar banderas de permiso entre roles.** Determina los accesos efectivos cuando un usuario posee múltiples roles mediante `resolve_sheet_permissions` y `PermissionSet`. 
- **Aplicar reglas de permiso genéricas a endpoints.** Permite exponer catálogos de manera pública y restringir operaciones críticas, implementado con `authentication.permissions.CallCenterPermission`. 

## Finanzas operativas

- **Describir fases del pipeline financiero.** Lista el flujo maestro de trabajo y sus artefactos por fase utilizando los modelos `Phase`, `Workflow` y `PhaseOutput`, expuestos mediante el `PhaseViewSet`. 
- **Documentar el pipeline financiero de referencia.** Captura las fases, workflows y dashboards esperados en `finance.domain`, fuente de la semilla funcional del monolito. 

## Auditoría y monitoreo

- **Registrar actividades relevantes en el libro financiero.** Modela eventos como inicio de sesión, aprobaciones o exportaciones mediante `AuditEvent`. 
- **Exponer el historial de auditoría.** Entrega eventos para monitoreo y cumplimiento vía `AuditEventViewSet`. 
- **Gestionar un log in-memory para pruebas o integraciones ligeras.** Permite registrar, consultar, filtrar y obtener el último evento con `AuditLog`/`AuditEntry`. 

## Dashboards ejecutivos

- **Administrar dashboards por persona.** Modela dashboards, KPIs y acciones rápidas mediante `Dashboard`, `DashboardKPI` y `DashboardAction`, expuestos por `DashboardViewSet`. 
- **Definir la configuración declarativa de dashboards.** Asocia métricas, audiencias y acciones en `dashboards.configs.DASHBOARD_LAYOUTS` para guiar la generación de vistas. 

## Alertas y notificaciones

- **Orquestar reglas de alerta financieras.** Describe condiciones, severidad y destinatarios con `notifications.models.AlertRule`, publicado mediante `AlertRuleViewSet`. 
- **Configurar canales de entrega de alertas.** Gestiona e integra medios como email, Slack o webhooks usando `AlertChannel` y el `AlertChannelViewSet`. 

## Infraestructura cruzada

- **Documentar fases, workflows y dashboards para análisis externo.** Los dataclasses en `finance.domain` funcionan como contrato compartido entre módulos y documentos. 
- **Centralizar catálogos de métricas y acciones.** `dashboards.configs` complementa el pipeline al detallar qué indicadores consume cada persona. 
