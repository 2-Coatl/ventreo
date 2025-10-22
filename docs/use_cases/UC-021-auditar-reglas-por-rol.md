# UC-021: AUDITAR REGLAS DE ALERTA APLICABLES A UN ROL

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-021|
|**Nombre**|Auditar reglas de alerta por rol|
|**Prioridad**|🟠 ALTA|
|**Categoría**|Governance de Notificaciones|
|**Actores**|Auditor (R005), Super Admin (R001), CFO (R002)|
|**Precondiciones**|Reglas activas y asociadas a roles|
|**Postcondiciones**|Reporte de reglas por rol disponible|
|**Frecuencia de Uso**|Mensual o ante cambios regulatorios|

---

## 🎯 DESCRIPCIÓN

Listar y revisar todas las reglas de alerta que impactan a uno o varios roles. Usa `notifications.services.rules_for_roles` para obtener `AlertRule` con `distinct()` evitando duplicidad cuando múltiples reglas comparten destinatarios. El reporte se emplea en auditorías SOX/ISO y para validar que cada rol reciba únicamente las alertas necesarias.

**Objetivo:** Proporcionar trazabilidad completa entre roles y reglas de notificación.

---

## 👥 ACTORES

- **Auditor (R005):** Responsable del informe de cumplimiento.
- **Super Admin (R001):** Garantiza que las relaciones roles↔alertas estén actualizadas.
- **CFO (R002):** Aprueba ajustes en caso de exceso o falta de alertas.

---

## 📝 PRECONDICIONES

1. Caso UC-020 ejecutado (destinatarios validados).
2. Acceso de lectura al módulo `notifications`.
3. Lista de roles objetivo definida (ej. `["cfo", "controller"]`).

---

## 🔄 FLUJO PRINCIPAL

```pseudocode
from notifications.services import rules_for_roles

roles_objetivo = ["cfo", "controller"]
reglas = rules_for_roles(roles_objetivo)

reporte = []
for regla in reglas:
    reporte.append({
        "codigo": regla.code,
        "nombre": regla.name,
        "descripcion": regla.description,
        "severidad": regla.severity,
        "sheet": regla.sheet,
        "roles": [rol.slug for rol in regla.audience.all()]
    })

guardar_archivo("reports/alertas_por_rol.json", reporte)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Roles sin reglas asociadas

```pseudocode
SI len(reglas) == 0 ENTONCES
    registrar_hallazgo("Roles sin alertas")
    recomendar_configurar_reglas(roles_objetivo)
FIN_SI
```

### FA-002: Regla con severidad incorrecta

```pseudocode
para cada regla en reglas:
    SI regla.severity == "info" y "cfo" en regla.roles:
        proponer_escalar_severidad(regla, nueva="warning")
FIN_PARA
```

---

## ✅ POSTCONDICIONES

- Reporte almacenado con sello de tiempo.
- Hallazgos documentados en `audit_event` con acción `view`.
- CFO informado de recomendaciones de ajuste.

---

## 📊 REGLAS DE NEGOCIO

- Cada rol crítico (`cfo`, `ceo`, `super_admin`) debe tener al menos una alerta `critical` o `warning`.
- Las reglas deben describir claramente el `trigger_condition`.
- Cambios al set de reglas requieren aprobación del CFO.

---

## 🗄️ MODELO DE DATOS

Tablas involucradas: `notifications_alertrule`, `notifications_alertrule_audience`, `identity_role`.

```sql
SELECT ar.code, ar.name, ar.severity, ar.sheet, r.slug
FROM notifications_alertrule ar
JOIN notifications_alertrule_audience ara ON ara.alertrule_id = ar.id
JOIN identity_role r ON r.id = ara.role_id
WHERE r.slug IN (%s);
```

---

## 📈 MÉTRICAS

- Número de reglas por rol.
- Porcentaje de reglas sin documentación (`description` vacía).
- Tiempo de respuesta de la consulta (< 300 ms p95).

---

## 🔐 SEGURIDAD

- Registrar quién generó el reporte y desde qué IP.
- Evitar exponer detalles de `trigger_condition` fuera de equipos autorizados.

---

## 💡 NOTAS

- Integrar reporte con SecurityRAT como evidencia del cumplimiento del requisito ASVS V11 (Lógica de negocio) en cuanto a alertado de eventos críticos.
- Se recomienda versionar el JSON en `docs/security/alertas_por_rol/` con control de cambios.

---

**FIN DEL CASO DE USO UC-021**
