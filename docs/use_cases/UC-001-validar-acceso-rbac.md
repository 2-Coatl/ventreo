# UC-001: VALIDAR ACCESO RBAC Y DESBLOQUEAR HOJAS

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-001|
|**Nombre**|Validar acceso RBAC y preparar entorno|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Seguridad y Gobernanza|
|**Actores**|Super Admin (R001), CFO (R002), CEO (R003), Contador (R004)|
|**Precondiciones**|Usuario autenticado; hoja `28_Control_Acceso_RBAC` disponible|
|**Postcondiciones**|Permisos aplicados, auditoría registrada, dashboards redirigidos|
|**Frecuencia de Uso**|Cada inicio de sesión|

---

## 🎯 DESCRIPCIÓN

Este caso de uso garantiza que el modelo financiero solo se desbloquea para personas autorizadas. Toma la identidad del usuario, recupera sus roles y aplica protecciones de hoja, además de registrar toda la sesión en la auditoría central.

**Objetivo:** Asegurar que la plataforma cargue únicamente las hojas y acciones permitidas según la configuración RBAC declarada en `finance/domain.py::ACCESS_PHASES`.

---

## 👥 ACTORES

### Actor Principal: Persona autenticada (roles R001–R004)

**Descripción:** Miembros del equipo financiero con acceso directo al archivo maestro.

**Responsabilidades:**

- Abrir el modelo y autenticarse.
- Mantener credenciales activas y actualizadas.
- Reportar accesos inusuales.

**Características:**

- Registro activo en `identity`.
- Asociación de roles mediante `access_control`.
- Soporte para multi-rol (roles acumulables).

---

## 📝 PRECONDICIONES

### PRE-001: Usuario autenticado en el sistema operativo
**Condición:** Identidad validada previo a abrir el archivo.
**Verificación:** Registro válido en `identity_user` y token local.

### PRE-002: Registro en tabla de control RBAC
**Condición:** Existencia en `access_control_sheetpermission`.
**Verificación:** Entrada con `sheet_slug` y `permission` activos.

### PRE-003: Hojas protegidas configuradas
**Condición:** Metadatos de hoja cargados en `finance/domain.py`.
**Verificación:** Enumeraciones disponibles para `ACCESS_PHASES` y `DASHBOARD_VIEWS`.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Ingreso al modelo

```pseudocode
INICIO validar_sesion_rbac
usuario_actual = obtener_usuario_activo()
SI usuario_actual == NULL ENTONCES
    mostrar_dialogo_login()
    RETORNAR
FIN_SI
```

### Paso 2: Resolución de roles y permisos

```pseudocode
roles = access_control.services.resolve_user_roles(usuario_actual)
permisos = access_control.services.resolve_sheet_permissions(usuario_actual, roles)
SI permisos.vacios() ENTONCES
    mostrar_error("No posee permisos activos")
    registrar_evento_auditoria(tipo="ACCESS_DENIED", usuario=usuario_actual)
    RETORNAR
FIN_SI
```

### Paso 3: Aplicar protecciones de hoja

```pseudocode
PARA cada hoja EN libro
    SI hoja.slug EN permisos.lectura
        hoja.desbloquear(modo="read")
    SI hoja.slug EN permisos.escritura
        hoja.desbloquear(modo="write")
    SI hoja.slug NO_EN permisos.todos
        hoja.ocultar()
FIN_PARA
```

### Paso 4: Registrar evento de auditoría

```pseudocode
audit.services.AuditLog.register(
    evento="LOGIN",
    usuario=usuario_actual.email,
    roles=roles,
    detalles={
        "hojas_desbloqueadas": permisos.total(),
        "ip": contexto.ip,
        "user_agent": contexto.user_agent,
    }
)
```

### Paso 5: Redirigir a dashboard adecuado

```pseudocode
dashboard = dashboards.services.resolve_home_dashboard(roles)
libro.ir_a(dashboard.sheet)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Usuario sin roles asignados
- Sistema bloquea acceso.
- Evento `ACCESS_DENIED` en `audit.models.AuditEvent`.
- Notificación automática a `notifications.AlertRule` "account_without_role".

### FA-002: Rol suspendido
- Se detecta `is_active = FALSE` en la relación usuario-rol.
- Se invoca `notifications.tasks.send_account_disabled_alert`.
- Se mantiene bloqueo total del archivo.

### FA-003: Error de sincronización de permisos
- Excepción al consultar `resolve_sheet_permissions`.
- Se captura y reporta al `Super Admin` mediante canal "rbac_sync_failed".

---

## ✅ POSTCONDICIONES

- `audit_auditevent` guarda el registro de sesión.
- Solo las hojas autorizadas quedan visibles y desbloqueadas.
- Dashboards se actualizan con métricas del rol activo.

---

## 📊 REGLAS DE NEGOCIO

1. **RN-001:** Ningún usuario puede ver hojas fuera de sus permisos acumulados.
2. **RN-002:** Roles críticos (CFO, CEO) requieren autenticación multifactor.
3. **RN-003:** Accesos fallidos consecutivos ≥3 generan bloqueo temporal.

---

## 🗄️ ENTIDADES RELACIONADAS

- `identity.models.Role`
- `access_control.models.SheetPermission`
- `audit.models.AuditEvent`
- `dashboards.models.Dashboard`

---

## 📈 MÉTRICAS

- Tiempo de desbloqueo < 3 segundos.
- 100% de sesiones registradas en auditoría.
- Incidentes críticos respondidos en <15 minutos.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Eventos `LOGIN`, `ACCESS_DENIED`, `ROLE_ESCALATION` almacenados para trazabilidad.
- Hash de dispositivo y dirección IP protegidos.
- Cumplimiento con principio "dependencies point inward": reglas viven en dominio.

---

## 💡 NOTAS

- La automatización se orquesta mediante macros/servicios equivalentes fuera del repo.
- El caso de uso es requisito previo para todos los demás.

---

**FIN DEL CASO DE USO UC-001**
