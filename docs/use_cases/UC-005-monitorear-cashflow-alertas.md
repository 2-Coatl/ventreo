# UC-005: MONITOREAR FLUJO DE EFECTIVO Y ALERTAS AUTOMÁTICAS

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-005|
|**Nombre**|Monitorear flujo de efectivo y alertas|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Gestión de Liquidez|
|**Actores**|CFO (R002), Controller (R005), CEO (R003), Alerting Bot|
|**Precondiciones**|Hoja `13_Flujo_Efectivo` actualizada; reglas de alerta configuradas|
|**Postcondiciones**|Alertas emitidas y dashboards sincronizados|
|**Frecuencia de Uso**|Diaria|

---

## 🎯 DESCRIPCIÓN

Centraliza la supervisión de liquidez y runway, activando alertas automáticas cuando los umbrales definidos en `finance/domain.py::CASH_FLOW` se alcanzan. Coordina dashboards ejecutivos y notificaciones.

**Objetivo:** Permitir detección temprana de riesgos de caja y cumplimiento de obligaciones fiscales.

---

## 👥 ACTORES

- **CFO:** Responsable de revisar indicadores y activar planes de acción.
- **Controller:** Investiga desviaciones de presupuesto.
- **CEO:** Recibe alertas críticas para decisiones estratégicas.
- **Alerting Bot:** Servicio que envía notificaciones según `alert_rules`.

---

## 📝 PRECONDICIONES

1. Datos consolidados en `13_Flujo_Efectivo` provenientes de ingresos/costos actualizados.
2. Reglas `runway_critical`, `burn_over_budget`, `tax_deadline` activas en `notifications`.
3. Dashboards `30`–`33` conectados a métricas más recientes.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Consolidar flujo diario

```pseudocode
actualizar_cashflow():
    ingresos = obtener_totales_ingresos()
    egresos = obtener_totales_costos()
    impuestos = obtener_obligaciones()
    hoja13.recalcular(ingresos, egresos, impuestos)
```

### Paso 2: Evaluar umbrales

```pseudocode
runway = hoja13.calcular_runway()
if runway < 3
    trigger_alert('runway_critical', destinatarios=[CEO, CFO])
if burn_rate > presupuesto * 1.1
    trigger_alert('burn_over_budget', destinatarios=[Controller])
```

### Paso 3: Programar recordatorios fiscales

```pseudocode
para obligacion, schedule en CASH_FLOW.alert_rules['tax_deadline']:
    notifications.schedule(obligacion, schedule)
```

### Paso 4: Actualizar dashboards

```pseudocode
dashboards.sync(['30_Dashboard_CEO','31_Dashboard_CFO','32_Dashboard_Contador','33_Dashboard_Operaciones'])
```

### Paso 5: Registrar auditoría

```pseudocode
audit.register('CASHFLOW_REFRESH', usuario=bot, detalles={runway, burn_rate})
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Datos inconsistentes → se genera alerta "cashflow_data_error" al Super Admin.
- **FA-002:** Runway recuperado → se envía notificación de cierre del incidente.
- **FA-003:** Alertas no entregadas → reintentos automáticos y escalación a soporte.

---

## ✅ POSTCONDICIONES

- Indicadores de liquidez actualizados.
- Alertas registradas en bitácora.
- Dashboards reflejan situación actual.

---

## 📊 REGLAS DE NEGOCIO

1. Runway mínimo objetivo: 6 meses.
2. Burn rate debe mantenerse ≤ presupuesto +5%.
3. Recordatorios fiscales se envían 7, 4, 2 y 0 días antes de la obligación.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.domain.CASH_FLOW`
- `notifications.AlertRule`
- `audit.models.AuditEvent`

---

## 📈 MÉTRICAS

- Runway actual (meses).
- Alertas generadas vs atendidas.
- Tiempo de reacción promedio.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Alertas críticas firmadas digitalmente.
- Acceso de solo lectura para CEO/Controller.

---

**FIN DEL CASO DE USO UC-005**
