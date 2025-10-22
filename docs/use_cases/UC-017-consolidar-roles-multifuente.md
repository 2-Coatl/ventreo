# UC-017: CONSOLIDAR ROLES MULTIFUENTE PARA UN COLABORADOR

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-017|
|**Nombre**|Consolidar roles multifuente|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Gestión de Identidades|
|**Actores**|Administrador de Identidad (R001), Mesa de Soporte|
|**Precondiciones**|Asignaciones parciales disponibles|
|**Postcondiciones**|Lista única de roles aplicada|
|**Frecuencia de Uso**|Cuando un usuario recibe nuevos accesos|

---

## 🎯 DESCRIPCIÓN

Unifica los roles otorgados a un colaborador desde múltiples fuentes (por ejemplo, bundles preconfigurados y asignaciones manuales). Utiliza el servicio `identity.services.flatten_role_assignments` para generar un set único que luego se almacena en la matriz RBAC y se comunica a los responsables de seguridad.

**Objetivo:** Eliminar inconsistencias de permisos al combinar roles acumulables sin duplicados.

---

## 👥 ACTORES

### Actor Principal: Administrador de Identidad

**Responsabilidades:**
- Registrar asignaciones individuales y grupales.
- Consolidar los roles definitivos para el usuario.
- Actualizar la tabla de permisos por hoja según el resultado.

**Características:**
- Acceso directo a herramientas de soporte y base de datos.

### Actor de Apoyo: Mesa de Soporte

**Responsabilidades:**
- Ejecutar scripts de consolidación.
- Documentar evidencia del cambio.

---

## 📝 PRECONDICIONES

1. **PRE-001:** Asignaciones parciales registradas en sistemas externos o tablas auxiliares.
2. **PRE-002:** Usuario autenticado con permisos para modificar RBAC.
3. **PRE-003:** Biblioteca `identity.services` importable en el entorno de trabajo.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Definir asignaciones de entrada

```pseudocode
from identity.services import RoleAssignment, flatten_role_assignments

asignaciones = [
    RoleAssignment(user_identifier="ana@ventreo.com", roles=["cfo", "controller"]),
    RoleAssignment(user_identifier="ana@ventreo.com", roles=["analista"]),
    RoleAssignment(user_identifier="ana@ventreo.com", roles=["gerente"]),
]
```

### Paso 2: Consolidar

```pseudocode
roles_unicos = flatten_role_assignments(asignaciones)
# roles_unicos => {"cfo", "controller", "analista", "gerente"}
```

### Paso 3: Persistir resultado en RBAC

```pseudocode
actualizar_sheet_permissions(usuario="ana@ventreo.com", roles=roles_unicos)
registrar_auditoria(usuario="ana@ventreo.com", accion="ROLE_ASSIGNMENT", detalle=roles_unicos)
```

### Paso 4: Notificar al usuario y a seguridad

```pseudocode
enviar_correo(destinatario="ana@ventreo.com", asunto="Roles actualizados", cuerpo=roles_unicos)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Asignaciones vacías

```pseudocode
SI len(asignaciones) == 0 ENTONCES
    lanzar_error("Usuario sin asignaciones")
    crear_ticket_soporte("Definir roles para usuario")
    RETORNAR
FIN_SI
```

### FA-002: Conflicto de roles prohibidos

```pseudocode
roles_prohibidos = {"auditor", "super_admin"}
SI roles_unicos.intersection(roles_prohibidos) ENTONCES
    escalar_a_seguridad(usuario, roles_unicos)
    suspender_provision_hasta_revision()
FIN_SI
```

---

## ✅ POSTCONDICIONES

- **POST-001:** Set consolidado almacenado en `access_control_sheetpermission`.
- **POST-002:** Registro de auditoría con detalle de roles otorgados.
- **POST-003:** Usuario informado de nuevos accesos.

---

## 📊 REGLAS DE NEGOCIO

- **RN-001:** Los roles son acumulables salvo los marcados como incompatibles por seguridad.
- **RN-002:** Siempre se mantiene un historial de asignaciones previas.
- **RN-003:** La consolidación debe ejecutarse antes de actualizar permisos de hoja.

---

## 🗄️ DATOS RELACIONADOS

- Tabla `identity_rolebundle_roles` (roles incluidos en bundles).
- Tabla `access_control_sheetpermission` (permisos efectivos).

---

## 📈 MÉTRICAS

- Tiempo para consolidar asignaciones (`< 1s` para ≤10 roles).
- Número de incidencias por permisos duplicados detectadas en auditorías.

---

## 🔐 SEGURIDAD

- Validar que las asignaciones provengan de fuentes confiables.
- Registrar quién ejecutó la consolidación y desde qué IP.

---

## 💡 NOTAS

- Recomendado integrar este flujo a un playbook de onboarding para nuevos colaboradores.
- SecurityRAT puede referenciar este caso mediante atributo `UC-017` para rastrear requisitos de segregación de funciones.

---

**FIN DEL CASO DE USO UC-017**
