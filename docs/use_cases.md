# Casos de uso completos del modelo financiero Ventreo v3.3 RBAC

Este inventario complementa el documento del pipeline y detalla los flujos narrativos que habilita el monolito modular. Cada caso de uso describe la configuración RBAC, el recorrido paso a paso y los artefactos del repositorio que participan.

## 1. Startup con fundador + contador (Configuración MICRO)

- **Contexto:** Empresas de 1 a 3 integrantes donde la persona fundadora concentra decisiones. Ingresos anuales menores a $500k.
- **Actores:** Fundador (roles acumulados CEO+CFO+Controller+Analista), Contador externo.
- **Objetivo:** Permitir trabajo sin fricciones para el fundador asegurando cumplimiento fiscal por parte del contador.
- **Recorrido:**
  1. Fundador abre el modelo; `identity.models.Role` asigna roles acumulados y `access_control.services.resolve_sheet_permissions` desbloquea todas las hojas salvo las fiscales definitivas.
  2. Puede modificar parámetros globales, inversiones y escenarios mediante los workflows declarados en `finance.domain`.
  3. Contador accede posteriormente; sus permisos restringen hojas sensibles y sólo otorgan `RWA` en impuestos (`SheetPermission` + `finance.models.Workflow`).
  4. Los cambios del contador generan eventos en `audit.models.AuditEvent` y el log en memoria `audit.services.AuditLog`.
  5. Las notificaciones se entregan a través de `notifications.models.AlertRule` cuando la declaración fiscal se marca como completada.
- **Resultado:** Cumplimiento fiscal con trazabilidad total sin bloquear al fundador.

## 2. Cambio de precios con aprobación CEO (Configuración PEQUEÑA)

- **Contexto:** Compañías de 4 a 10 personas con separación CEO/CFO. Ingresos $500k-$5M.
- **Actores:** CFO (proponente), CEO (aprobador), equipos de ventas/operaciones (informados).
- **Objetivo:** Elevar tarifas con análisis de impacto y controles de aprobación.
- **Recorrido:**
  1. CFO modifica hojas de precios (`finance.domain.REVENUE_MODEL`) y genera una solicitud >10% que queda en estado `PROPUESTO`.
  2. El pipeline registra la petición en `finance.models.Workflow` y la expone en el dashboard CEO vía `dashboards.models.Dashboard`.
  3. CEO revisa métricas, documentación adjunta y aprueba la solicitud. El sistema recalcula proyecciones (`finance.domain.CASH_FLOW`) y actualiza dashboards (`dashboards.configs.DASHBOARD_LAYOUTS`).
  4. Auditoría y notificaciones capturan todo el flujo (`audit.models.AuditEvent`, `notifications.models.AlertRule`).
- **Resultado:** Ajuste de precios aplicado sólo tras validación ejecutiva, con análisis y notificación automática.

## 3. Declaración fiscal preparada por el contador (Configuración MEDIANA)

- **Contexto:** Empresas de 11 a 50 personas con roles especializados (Controller separado del CFO).
- **Actores:** Contador (edición fiscal), CFO (validador), Auditor (lectura).
- **Objetivo:** Generar declaraciones tributarias con segregación de funciones y registro de cambios.
- **Recorrido:**
  1. Contador actualiza nóminas, impuestos y depreciaciones en `finance.domain.TAX_COMPLIANCE`.
  2. Los cambios se auditan y se exigen justificaciones mediante `audit.models.AuditEvent.details`.
  3. CFO valida y aprueba la declaración; la acción dispara alertas internas y actualiza flujos de efectivo.
  4. Auditor tiene lectura total para revisiones externas, garantizando el principio de sólo lectura.
- **Resultado:** Declaración con aprobación dual y trazabilidad para auditorías.

## 4. Planeación de escenarios y validación ejecutiva (Configuración MEDIANA/GRANDE)

- **Contexto:** Organización con analistas dedicados y comité ejecutivo.
- **Actores:** Analista financiero (crea escenarios), CFO (valida), CEO/Board (aprueba), Gerentes (consumen dashboards).
- **Objetivo:** Elaborar escenarios alternos, validar supuestos y decidir la estrategia.
- **Recorrido:**
  1. Analista genera un nuevo escenario en las hojas de planeación (`finance.domain.SCENARIO_PLANNING`).
  2. El workflow requiere validación del CFO antes de exponer resultados a directivos.
  3. Dashboards especializados (`dashboards.models.DashboardKPI`) muestran impacto en métricas clave.
  4. Una aprobación final del CEO/Board activa el escenario como oficial y bloquea versiones previas.
- **Resultado:** Escenarios controlados con etapas de aprobación y comunicación a responsables operativos.

## 5. Solicitud de presupuesto por gerente (Configuración PEQUEÑA/GRANDE)

- **Contexto:** Múltiples áreas con responsables que no deben ver datos sensibles de otras unidades.
- **Actores:** Gerente operativo (solicita), Controller (aprueba nivel 1), CFO/CEO (aprueban niveles superiores).
- **Objetivo:** Ajustar presupuestos con protección de información y workflow escalonado.
- **Recorrido:**
  1. Gerente ingresa al modelo; los filtros automáticos de `access_control.services.resolve_sheet_permissions` limitan visibilidad a su área.
  2. Solicita incremento presupuestal mediante el workflow de costos (`finance.domain.COST_STRUCTURE`).
  3. Controller revisa y aprueba según umbrales. Monto mayores escalan a CFO y eventualmente a CEO/Board.
  4. El pipeline actualiza las hojas, recalcula proyecciones y notifica a las partes (`notifications.models.AlertRule`).
- **Resultado:** Cambios presupuestales controlados, con privacidad y reglas de aprobación configurables.

## 6. Workflow completo corporativo (Configuración GRANDE)

- **Contexto:** Empresas con más de 50 personas, compliance estricto y auditorías formales.
- **Actores:** Super Admin, CEO, CFO, Controller, Contador, Analistas, Gerentes, Auditor interno, Viewer externos.
- **Objetivo:** Operar todos los módulos con jerarquías de aprobación de hasta cinco niveles.
- **Recorrido:**
  1. El Super Admin mantiene usuarios y permisos en `access_control` y realiza pruebas de regresión.
  2. Los cambios operativos recorren el pipeline: autenticación → permisos → finanzas → dashboards → alertas, manteniendo dependencias apuntando a los contratos de `finance.domain`.
  3. Auditorías internas consultan `audit.models.AuditEvent` y generan reportes regulatorios.
  4. Stakeholders externos acceden únicamente a dashboards públicos (`dashboards.configs.PUBLIC_LAYOUTS`).
- **Resultado:** Operación empresarial completa con cumplimiento SOX-ready y trazabilidad transversal.

## 7. Matriz de referencia rápida

| Tamaño | Personas | Roles activos | Niveles de aprobación | Tiempo de setup |
| --- | --- | --- | --- | --- |
| Micro | 1-3 | 2-3 | Sin aprobaciones | 30 minutos |
| Pequeña | 4-10 | 3-5 | CEO > $5k | 2 horas |
| Mediana | 11-50 | 5-7 | Controller → CFO → CEO | 1 día |
| Grande | 50+ | 9 (todos) | Hasta Board | 3 días + capacitación |

> Para diagramas detallados, fases del pipeline y matrices de permisos, consulte `docs/data_flow_pipeline.md`.
