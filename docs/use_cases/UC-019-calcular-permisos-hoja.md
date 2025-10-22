# UC-019: CALCULAR PERMISOS EFECTIVOS SOBRE UNA HOJA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-019|
|**Nombre**|Calcular permisos efectivos sobre una hoja|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Control de Accesos|
|**Actores**|Controller (R006), Super Admin (R001), Auditor (R005)|
|**Precondiciones**|Roles consolidados; entradas en `access_control_sheetpermission`|
|**Postcondiciones**|Permisos efectivos documentados y aplicados|
|**Frecuencia de Uso**|Antes de cada liberación del modelo|

---

## 🎯 DESCRIPCIÓN

Evalúa los permisos reales (lectura, escritura, aprobación, exportación) que tendrá una persona sobre una hoja específica del libro financiero. Usa la función `access_control.services.resolve_sheet_permissions` para combinar las banderas otorgadas a todos los roles del usuario.

**Objetivo:** Garantizar que las hojas sensibles sólo se expongan con los privilegios apropiados.

---

## 👥 ACTORES

- **Controller (R006):** Valida permisos de gerentes y analistas en su área.
- **Super Admin (R001):** Revisa consistencia global antes de liberar una versión.
- **Auditor (R005):** Comprueba que la segregación de funciones se cumpla.

---

## 📝 PRECONDICIONES

1. Matriz de permisos actualizada en `access_control_sheetpermission`.
2. Lista consolidada de roles por usuario (UC-017).
3. Servicio de acceso a datos disponible.

---

## 🔄 FLUJO PRINCIPAL

```pseudocode
from access_control.services import resolve_sheet_permissions

sheet_code = "05_Costos_Fijos"
roles_usuario = ["controller", "gerente"]
permisos = resolve_sheet_permissions(sheet_code, roles_usuario)

if not permisos.read:
    bloquear_acceso(sheet_code, usuario)
if permisos.write:
    habilitar_edicion(sheet_code)
if permisos.approve:
    requerir_token_aprobacion(sheet_code)
if not any([permisos.read, permisos.write, permisos.approve, permisos.export]):
    registrar_alerta("Usuario sin permisos en hoja crítica")
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Hoja sin configuración

```pseudocode
permisos = resolve_sheet_permissions("sheet_desconocida", roles)
SI permisos == PermissionSet():
    crear_ticket("Configurar hoja en matriz RBAC")
    restringir_hoja_temporalmente()
FIN_SI
```

### FA-002: Permisos excesivos

```pseudocode
SI permisos.write y rol_usuario == "viewer":
    escalar_a_seguridad("Viewer con escritura")
    revocar_permiso(sheet_code, "viewer")
FIN_SI
```

---

## ✅ POSTCONDICIONES

- Permisos documentados en acta de liberación.
- Ajustes realizados si se detectaron inconsistencias.
- Registro en `audit_event` con acción `view` y metadatos de evaluación.

---

## 📊 REGLAS DE NEGOCIO

- Lectura es prerequisito para exportar.
- Aprobación sólo disponible para roles `cfo`, `ceo`, `controller` según matriz.
- Ningún rol con jerarquía > 6 puede tener permisos de escritura en hojas fiscales.

---

## 🗄️ MODELO DE DATOS

Tabla `access_control_sheetpermission`:

```sql
SELECT role_id, can_read, can_write, can_approve, can_export
FROM access_control_sheetpermission
WHERE sheet_id = (SELECT id FROM access_control_sheet WHERE code = %s);
```

---

## 📈 MÉTRICAS

- Número de hojas evaluadas por liberación.
- Porcentaje de hallazgos corregidos antes de producción.

---

## 🔐 SEGURIDAD

- Registrar quién consultó la matriz de permisos.
- Enviar alerta automática si un rol de alto privilegio pierde acceso crítico.

---

## 💡 NOTAS

- SecurityRAT puede vincular este caso a los requisitos ASVS V4 (Control de Acceso) y V8 (Protección de Datos).
- Integrar en pipelines CI ejecutando pruebas unitarias sobre `resolve_sheet_permissions` con fixtures de roles.

---

**FIN DEL CASO DE USO UC-019**
