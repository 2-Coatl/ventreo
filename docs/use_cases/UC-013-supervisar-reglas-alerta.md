# UC-013: SUPERVISAR REGLAS DE ALERTA RBAC

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-013|
|**Nombre**|Supervisar reglas de alerta RBAC|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Notificaciones y Monitoreo|
|**Actores**|CFO (R002), Controller (R006), Super Admin (R001)|
|**Precondiciones**|Reglas cargadas en `notifications_alertrule`|
|**Postcondiciones**|Reglas validadas, audiencias confirmadas|
|**Frecuencia de Uso**|Semanal y tras incidentes críticos|

---

## 🎯 DESCRIPCIÓN

`notifications.views.AlertRuleViewSet` expone las reglas que generan avisos para runway, burn rate y obligaciones fiscales. Este caso de uso garantiza que las reglas reflejen los umbrales vigentes y estén asignadas a los roles correctos.

**Objetivo:** Mantener un monitoreo proactivo del pipeline financiero mediante alertas oportunas.

---

## 👥 ACTORES

- **CFO:** Ajusta severidades y valida que las alertas cubran riesgos financieros.
- **Controller:** Verifica que las audiencias incluyen a responsables operativos.
- **Super Admin:** Supervisa cobertura y compliance.

---

## 📝 PRECONDICIONES

1. Base de datos con reglas de alerta configuradas (`trigger_condition`, `severity`).
2. Roles asociados a las reglas (`many-to-many` con `identity_role`).
3. API `/api/notifications/alert-rules/` accesible.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Listar reglas

```pseudocode
rules = GET /api/notifications/alert-rules/
validar_status(rules.status_code)
cat = rules.json()
```

### Paso 2: Validar severidad y condiciones

```pseudocode
PARA regla EN cat
    revisar(regla['severity'], regla['trigger_condition'])
    asegurar_sheet(regla['sheet'])
FIN_PARA
```

### Paso 3: Confirmar audiencias

```pseudocode
PARA regla EN cat
    roles = [aud['slug'] for aud in regla['audience']]
    SI roles_vacios(roles)
        crear_issue('ALERT_WITHOUT_AUDIENCE', regla['code'])
    FIN_SI
    validar_roles_con_bundle(roles)
FIN_PARA
```

### Paso 4: Ajustar thresholds (opcional)

```pseudocode
SI se requiere ajuste
    PATCH /api/notifications/alert-rules/{code}/ {'trigger_condition': nueva_condicion}
FIN_SI
```

### Paso 5: Registrar revisión

```pseudocode
audit_log.record(AuditEntry(
    timestamp=ahora(),
    user=actor.email,
    role=actor.rol,
    sheet='ALERT_RULES',
    action='view',
    description='Revisión de alert rules',
    metadata={'total_rules': len(cat)}
))
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Alerta sin sheet asociada → se marca como genérica y se revisa en SecurityRAT.
- **FA-002:** Severidad no mapeada (`severity` fuera de choices) → se bloquea hasta corregir.
- **FA-003:** Roles desactivados → se remueven de la audiencia y se asigna reemplazo.

---

## ✅ POSTCONDICIONES

1. Lista de reglas auditada y ajustada.
2. Roles informados de cambios relevantes.
3. SecurityRAT actualiza requisito `ASVS V7` con notas de seguimiento.

---

## 📊 REGLAS DE NEGOCIO

1. Toda alerta `critical` debe incluir al menos a CEO y CFO.
2. Alertas de impuestos deben llegar al Contador y al Controller.
3. No se permiten reglas sin `trigger_condition` documentada.

---

## 🗄️ CONSULTAS

```sql
SELECT code, severity, trigger_condition
FROM notifications_alertrule
ORDER BY severity DESC;
```

---

## 📈 MÉTRICAS

- Cantidad de alertas activadas por semana (`notifications_alertrule_event_log`).
- Tiempo de respuesta promedio del rol responsable.

---

## 🔐 SEGURIDAD

- Cambios vía API requieren token de servicio.
- Notificaciones se firman digitalmente cuando se envían a canales externos (`AlertChannel`).

---

## 💡 EJEMPLO

- CFO revisa `runway_critical`: severidad `critical`, sheet `13_Flujo_Efectivo`, audiencia `[ceo, cfo]`. Ajusta condición a `< 4 meses` tras nueva directriz.

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. API devuelve reglas con audiencia embebida.
2. Se detectan reglas sin audiencia y generan issue.
3. Auditoría refleja revisión.
4. SecurityRAT registra seguimiento.

---

**FIN DEL CASO DE USO UC-013**
