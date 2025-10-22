# UC-020: DERIVAR DESTINATARIOS DE ALERTAS POR SEVERIDAD

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-020|
|**Nombre**|Derivar destinatarios por severidad de alerta|
|**Prioridad**|🟠 ALTA|
|**Categoría**|Gestión de Notificaciones|
|**Actores**|CFO (R002), Controller (R006), Equipo de IT Ops|
|**Precondiciones**|Reglas configuradas en `notifications_alertrule`|
|**Postcondiciones**|Lista de roles destinatarios validada|
|**Frecuencia de Uso**|Cada vez que se ajustan reglas o se dispara una alerta crítica|

---

## 🎯 DESCRIPCIÓN

Identifica qué roles deben recibir una notificación cuando se produce una alerta según su severidad (`info`, `warning`, `critical`). Se apoya en `notifications.services.recipients_by_severity`, que consulta las relaciones `AlertRule.audience` para evitar duplicidades y garantizar cobertura completa.

**Objetivo:** Asegurar que las alertas lleguen a los responsables correctos sin redundancia excesiva.

---

## 👥 ACTORES

- **CFO:** Verifica que las alertas financieras lleguen a ejecutivos y controller.
- **Controller:** Confirma que su equipo recibe avisos operativos oportunos.
- **IT Ops:** Integra la lista de destinatarios con canales (correo, Slack, webhooks).

---

## 📝 PRECONDICIONES

1. Reglas de alerta cargadas (UC-013).
2. Roles asignados a cada regla mediante panel de administración.
3. Servicio de notificaciones disponible.

---

## 🔄 FLUJO PRINCIPAL

```pseudocode
from notifications.services import recipients_by_severity

severidad = "critical"
destinatarios = recipients_by_severity(severidad)

for rol in destinatarios:
    canal = resolver_canal_por_rol(rol)
    programar_envio_alerta(rol=rol, canal=canal, severidad=severidad)

registrar_auditoria(
    accion="ALERT_RECIPIENTS_RESOLVED",
    metadata={"severidad": severidad, "destinatarios": destinatarios}
)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Sin reglas para severidad

```pseudocode
destinatarios = recipients_by_severity("warning")
SI len(destinatarios) == 0 ENTONCES
    registrar_alerta_config("Sin receptores para alertas WARNING")
    asignar_roles_por_defecto(["controller", "cfo"])
FIN_SI
```

### FA-002: Rol duplicado

`recipients_by_severity` ya evita duplicados, pero si se detecta manualmente:

```pseudocode
if destinatarios.count("cfo") > 1:
    limpiar_relaciones_repetidas("cfo", severidad)
```

---

## ✅ POSTCONDICIONES

- Destinatarios finales registrados en bitácora de alertas.
- Integración con canales actualizada.
- Reporte compartido con CFO y Controller.

---

## 📊 REGLAS DE NEGOCIO

- Alertas `critical` deben incluir al menos roles `cfo` y `ceo`.
- Alertas `info` no deben notificar a más de 5 roles para evitar fatiga.
- Cambios en destinatarios requieren notificación automática a Seguridad.

---

## 🗄️ MODELO DE DATOS

`notifications_alertrule_audience` (tabla intermedia) relaciona reglas con roles:

```sql
SELECT r.code, rr.role_id
FROM notifications_alertrule r
JOIN notifications_alertrule_audience rr ON rr.alertrule_id = r.id
WHERE r.severity = %s;
```

---

## 📈 MÉTRICAS

- Tiempo promedio de resolución de destinatarios (`p95` < 150 ms).
- Número de alertas sin destinatario configurado.
- Niveles de severidad con mayor volumen.

---

## 🔐 SEGURIDAD

- Registrar cada ejecución con `audit_event` (acción `view`).
- Validar que roles sensibles sólo reciban alertas relevantes.

---

## 💡 NOTAS

- Asociar este caso en SecurityRAT con requisitos ASVS V7 (Manejo de errores y registro) y V9 (Comunicación).
- Se recomienda cachear resultados de severidad `info` para reducir consultas.

---

**FIN DEL CASO DE USO UC-020**
