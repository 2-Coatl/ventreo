# UC-015: MONITOREAR BITÁCORA DE AUDITORÍA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-015|
|**Nombre**|Monitorear bitácora de auditoría|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Cumplimiento y Trazabilidad|
|**Actores**|Auditor (R005), Super Admin (R001), CFO (R002)|
|**Precondiciones**|Eventos registrados en `audit_auditevent`|
|**Postcondiciones**|Hallazgos documentados, incidentes escalados|
|**Frecuencia de Uso**|Diario para auditor, semanal para CFO|

---

## 🎯 DESCRIPCIÓN

`audit.views.AuditEventViewSet` ofrece acceso de solo lectura a la bitácora de acciones del modelo financiero. Este caso de uso se centra en revisar quién editó, aprobó o exportó datos críticos, alineado con controles SOX.

**Objetivo:** Detectar actividades anómalas, validar segregación de funciones y alimentar reportes de cumplimiento.

---

## 👥 ACTORES

- **Auditor:** Revisa eventos y genera hallazgos.
- **Super Admin:** Investiga incidentes y aplica correcciones.
- **CFO:** Supervisa actividades financieras clave.

---

## 📝 PRECONDICIONES

1. Sistema registra eventos (`AuditEvent` con `action` y `metadata`).
2. API `/api/audit/events/` disponible.
3. Roles involucrados tienen permisos `can_read` sobre auditoría.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Filtrar eventos por fecha

```pseudocode
events = GET /api/audit/events/?ordering=-created_at&limit=200
verificar_status(events.status_code)
lista = events.json()['results']
```

### Paso 2: Identificar eventos críticos

```pseudocode
criticos = [e for e in lista if e['action'] in ['approve','export']]
PARA evento EN criticos
    evaluar_riesgo(evento)
FIN_PARA
```

### Paso 3: Cruce con casos de uso

```pseudocode
PARA evento EN lista
    uc = mapear_caso_de_uso(evento['sheet'])
    adjuntar_a_reporte(uc, evento)
FIN_PARA
```

### Paso 4: Generar hallazgos

```pseudocode
SI evento_sospechoso(en criticos)
    crear_ticket('AUDIT_ALERT', detalle=evento)
FIN_SI
```

### Paso 5: Cerrar ciclo con SecurityRAT

```pseudocode
securityrat.update_requirement('ASVS V13', status='Verified', evidence=link_reporte)
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** No hay eventos → se verifica salud del pipeline y se documenta "sin actividad".
- **FA-002:** Registro incompleto (`metadata` vacío) → se genera bug para revisar proceso de logging.
- **FA-003:** Acceso denegado → se valida que el usuario tenga rol `auditor` o `super_admin`.

---

## ✅ POSTCONDICIONES

1. Reporte de auditoría actualizado con eventos críticos.
2. Incidentes escalados cuando corresponde.
3. SecurityRAT actualizado con evidencia.

---

## 📊 REGLAS DE NEGOCIO

1. Exportaciones deben estar acompañadas de ticket autorizado.
2. Aprobaciones deben provenir de roles con jerarquía ≤3.
3. Cualquier acción fuera de horario laboral genera alerta `after_hours_activity`.

---

## 🗄️ CONSULTAS

```sql
SELECT user_identifier, role_id, sheet, action, created_at
FROM audit_auditevent
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;
```

---

## 📈 MÉTRICAS

- Número de eventos críticos por semana.
- Tiempo promedio para cerrar incidentes detectados.

---

## 🔐 SEGURIDAD

- Endpoint de auditoría requiere autenticación; se recomienda read replica dedicada.
- Datos exportados se almacenan cifrados en repositorio seguro.

---

## 💡 EJEMPLO

- Auditor detecta aprobación realizada por rol `analista`; genera hallazgo `segregation_violation` y solicita corrección en matriz RBAC.

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. Endpoint expone campos `user_identifier`, `role`, `sheet`, `action`, `metadata`.
2. Eventos se pueden filtrar por fecha y tipo.
3. Hallazgos críticos generan ticket automático.
4. Evidencia queda asociada en SecurityRAT.

---

**FIN DEL CASO DE USO UC-015**
