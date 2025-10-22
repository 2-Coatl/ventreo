# UC-009: CONFIGURAR PARÁMETROS MAESTROS DEL MODELO

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-009|
|**Nombre**|Configurar parámetros maestros del modelo|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Planeación y Setup Inicial|
|**Actores**|CFO (R002), Controller (R006), Contador (R004)|
|**Precondiciones**|Hoja `01_Parametros_Globales` desbloqueada para el actor|
|**Postcondiciones**|Parámetros validados, propagados y registrados en auditoría|
|**Frecuencia de Uso**|Mensual (cambios de impuestos o escenario)|

---

## 🎯 DESCRIPCIÓN

El caso de uso cubre la actualización de impuestos, supuestos comerciales y selección de escenarios en la hoja maestra `01_Parametros_Globales`. Este módulo alimenta múltiples fases del pipeline descritas en `finance/domain.py`, por lo que exige controles estrictos de autorización y registro.

**Objetivo:** Asegurar que las variables críticas (IVA, ISR, ARPU, Escenario Activo, etc.) se actualicen con validaciones formales y propaguen sus efectos a proyecciones, impuestos y dashboards.

---

## 👥 ACTORES

### Actor Principal: CFO (R002)

**Descripción:** Responsable de mantener vigentes los supuestos financieros.

**Responsabilidades:**
- Ajustar tasas impositivas y supuestos comerciales.
- Seleccionar escenarios de proyección.
- Coordinar aprobaciones cuando se exceden umbrales críticos.

**Características:**
- Permisos completos (`can_write` y `can_approve`) sobre la hoja `01_Parametros_Globales` según `access_control.models.SheetPermission`.
- Recibe notificaciones críticas desde `notifications.AlertRule` cuando los cambios afectan KPIs del CEO.

### Actor Secundario: Controller (R006)

- Puede proponer ajustes a costos base y churn, pero requiere aprobación del CFO.
- Acceso limitado a celdas etiquetadas como "editable_controller".

### Actor Secundario: Contador (R004)

- Actualiza umbrales fiscales y parámetros contables.
- Debe validar consistencia con `26_Calculadora_Impuestos`.

---

## 📝 PRECONDICIONES

### PRE-001: Sesión autenticada y con roles vigentes
**Verificación:** Entrada en `identity_role` y relación activa en `access_control_sheetpermission` para la hoja objetivo.

### PRE-002: Hoja protegida sincronizada
**Verificación:** `resolve_sheet_permissions('01_Parametros_Globales', roles)` devuelve `write = TRUE` para el actor (`access_control.services`).

### PRE-003: Auditoría operativa disponible
**Verificación:** Servicio `audit.services.AuditLog` inicializado para registrar eventos de configuración.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Abrir módulo de parámetros

```pseudocode
INICIO configurar_parametros
usuario = obtener_usuario_actual()
roles = obtener_roles(usuario)
permisos = resolve_sheet_permissions('01_Parametros_Globales', roles)
SI permisos.write == FALSE ENTONCES
    mostrar_error("No tienes permisos de edición sobre parámetros")
    registrar_evento_auditoria(usuario, 'ACCESS_DENIED', sheet='01_Parametros_Globales')
    RETORNAR
FIN_SI
activar_hoja('01_Parametros_Globales')
```

### Paso 2: Editar variables críticas con validaciones

```pseudocode
celdas_validables = {
    'IVA': rango(0, 0.25),
    'ISR': rango(0, 0.4),
    'ARPU': rango(0, 5000),
    'Churn': rango(0, 0.3)
}
PARA (campo, regla) EN celdas_validables
    valor = leer_celda(campo)
    SI no cumple regla ENTONCES
        marcar_error_visual(campo)
        agregar_mensaje_validacion(campo, "Valor fuera de rango permitido")
        RETORNAR
    FIN_SI
FIN_PARA
```

### Paso 3: Seleccionar escenario activo

```pseudocode
escenario_anterior = leer_celda('EscenarioActivo')
escenario_nuevo = seleccionar_opcion(['Bootstrapping','Base','Acelerado','Conservador'])
SI escenario_nuevo != escenario_anterior ENTONCES
    escribir_celda('EscenarioActivo', escenario_nuevo)
    notificar('scenario_changed', roles=[Role.CEO, Role.CFO])
FIN_SI
```

### Paso 4: Propagar cambios a hojas dependientes

```pseudocode
sheets_dependientes = [
    '09_Modelo_Precios',
    '10_Proyeccion_Ventas',
    '11_Suscripcion_MRR_LTV',
    '13_Flujo_Efectivo',
    '26_Calculadora_Impuestos',
    '27_Depreciacion_Equipamiento'
]
PARA hoja EN sheets_dependientes
    recalcular_hoja(hoja)
FIN_PARA
actualizar_dashboards(['30_Dashboard_CEO','31_Dashboard_CFO'])
```

### Paso 5: Registrar auditoría

```pseudocode
audit_log.record(AuditEntry(
    timestamp=ahora(),
    user=usuario.email,
    role=roles.principal(),
    sheet='01_Parametros_Globales',
    action='edit',
    description='Actualización de parámetros maestros',
    metadata={'escenario': escenario_nuevo}
))
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Usuario sin permisos de edición
- Sistema bloquea edición y solo permite lectura.
- Evento `ACCESS_DENIED` registrado con severidad WARNING.
- Se envía alerta mediante `AlertRule` `rbac_sheet_denied` al Super Admin.

### FA-002: Valor fuera de rango crítico
- Se revierte el cambio y se solicita justificación.
- Controller debe abrir solicitud de aprobación (workflow manual con CFO) si requiere excepción.

### FA-003: Cambio simultáneo detectado
- Si `audit_auditevent` contiene registro `edit` hace <5 minutos por otro usuario, el sistema muestra modal de bloqueo y ofrece opción de reintentar en modo "solo lectura".

### FA-004: Integridad fallida al propagar
- Si `recalcular_hoja` lanza error, se levanta incidente `param_sync_failed` y se genera ticket en JIRA mediante SecurityRAT.

---

## ✅ POSTCONDICIONES

1. `01_Parametros_Globales` contiene valores vigentes y validados.
2. Dashboards del CEO y CFO reflejan supuestos actualizados.
3. Existe registro en `audit_auditevent` con acción `edit` vinculada al usuario.
4. Se actualiza métrica "Última actualización de parámetros" mostrada en `33_Dashboard_Operaciones` para visibilidad operativa.

---

## 📊 REGLAS DE NEGOCIO

1. **RN-001:** IVA e ISR deben mantenerse dentro de los rangos regulatorios definidos por cumplimiento.
2. **RN-002:** Cambios en `EscenarioActivo` >15% en variación de MRR requieren aprobación del CEO (Workflow `INVESTMENT_WORKFLOW` en `finance/domain.py`).
3. **RN-003:** Solo un cambio por día laborable puede marcarse como "definitivo"; ajustes adicionales deben quedar como borrador hasta la revisión semanal.

---

## 🗄️ ESTRUCTURA DE DATOS RELACIONADA

### Tabla: access_control_sheetpermission (fragmento relevante)

```sql
SELECT role_id, can_read, can_write, can_approve
FROM access_control_sheetpermission
WHERE sheet_id = (SELECT id FROM access_control_sheet WHERE code = '01_Parametros_Globales');
```

### Tabla: audit_auditevent

```sql
CREATE INDEX idx_audit_sheet ON audit_auditevent (sheet, created_at DESC);
```

---

## 📈 MÉTRICAS Y REPORTES

- **Tiempo promedio de actualización:**

```sql
SELECT AVG(EXTRACT(EPOCH FROM (created_at - LAG(created_at) OVER (ORDER BY created_at)))) AS segundos_entre_actualizaciones
FROM audit_auditevent
WHERE sheet = '01_Parametros_Globales' AND action = 'edit';
```

- **Impacto por parámetro:** Registrar en tabla auxiliar `finance_parameter_history` (sugerida) con columnas `field`, `old_value`, `new_value`, `impacto_estimado`.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Cada edición dispara alerta `param_change_review` para el Controller.
- Se exige MFA para usuarios con `can_write` según política `identity.Role` de jerarquía ≤3.
- SecurityRAT debe mapear requisito `ASVS V4` a este caso de uso para validar controles de autorización.

---

## 💡 EJEMPLOS DE USO

- Ajustar IVA de 16% a 17% tras cambio regulatorio; sistema recalcula flujo de efectivo y envía alerta al CEO.
- Cambiar escenario de `Base` a `Acelerado` antes de junta directiva; CFO documenta justificación y se audita el cambio.

---

## 🎨 INTERFAZ (Wireframe simplificado)

```
┌────────────────────────────────────────────┐
│ PARÁMETROS GLOBALES                        │
├────────────────────────────────────────────┤
│ IVA [%]        [16.0] ⓘ  │ ISR [%] [30.0] │
│ ARPU [$]       [1800]     │ Churn [%] [4]  │
│ Escenario Activo: [Base ▼]                │
├────────────────────────────────────────────┤
│ [Validar Cambios] [Guardar Definitivo]     │
└────────────────────────────────────────────┘
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. Usuario con rol autorizado puede editar y guardar cambios dentro de rangos definidos.
2. Cambios se reflejan en `13_Flujo_Efectivo` y dashboards sin errores.
3. Intento de actor no autorizado queda registrado y bloqueado.
4. Auditoría contiene metadata del cambio (antes/después, escenario activo).
5. SecurityRAT vincula requisito ASVS correspondiente y genera issue si falla una validación.

---

**FIN DEL CASO DE USO UC-009**
