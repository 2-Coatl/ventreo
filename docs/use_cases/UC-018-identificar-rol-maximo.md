# UC-018: IDENTIFICAR EL ROL DE MAYOR PRIVILEGIO

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-018|
|**Nombre**|Identificar el rol de mayor privilegio|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Governance, Risk & Compliance|
|**Actores**|Auditor Interno (R005), Super Admin (R001)|
|**Precondiciones**|Roles consolidados disponibles|
|**Postcondiciones**|Rol dominante documentado|
|**Frecuencia de Uso**|En cada revisión trimestral o acceso sensible|

---

## 🎯 DESCRIPCIÓN

Determina qué rol posee la mayor jerarquía dentro del conjunto asignado a una persona. Se basa en la función `identity.services.highest_privilege_role`, que consulta `identity_role` ordenando por `hierarchy_level`. El resultado se usa para definir qué flujos de aprobación requiere el usuario y qué dashboards se habilitan.

**Objetivo:** Aplicar controles de segregación de funciones priorizando el rol con mayores privilegios.

---

## 👥 ACTORES

### Auditor Interno (R005)
- Verifica que los accesos otorgados son proporcionales a las funciones.
- Documenta hallazgos en la bitácora de cumplimiento.

### Super Admin (R001)
- Valida solicitudes de elevación de privilegios.
- Ajusta configuraciones RBAC si detecta inconsistencias.

---

## 📝 PRECONDICIONES

1. Resultado de UC-017 disponible (roles consolidados).
2. Servicio de base de datos accesible.
3. Auditor autenticado con permisos de consulta.

---

## 🔄 FLUJO PRINCIPAL

```pseudocode
from identity.services import highest_privilege_role

roles_usuario = ["cfo", "controller", "analista"]
rol_dominante = highest_privilege_role(roles_usuario)
SI rol_dominante ES None ENTONCES
    registrar_alerta("Usuario sin roles activos")
    RETORNAR
FIN_SI

registrar_auditoria(
    usuario="ana@ventreo.com",
    accion="ROLE_PRIVILEGE_EVALUATION",
    detalle={"rol_maximo": rol_dominante.slug}
)

si rol_dominante.slug == "super_admin":
    aplicar_monitoring_intensivo(usuario)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Roles inexistentes

```pseudocode
SI highest_privilege_role(devuelve=None) ENTONCES
    crear_ticket("Asignar roles al usuario")
    restringir_accesos_temporales(usuario)
FIN_SI
```

### FA-002: Inconsistencia de jerarquía

```pseudocode
SI rol_dominante.hierarchy_level > umbral_permitido:
    escalar_a_comite_seguridad()
    congelar_operaciones_sensibles(usuario)
FIN_SI
```

---

## ✅ POSTCONDICIONES

- Rol dominante archivado en expediente de auditoría.
- Alertas configuradas si el rol excede el perfil esperado.
- Dashboard correspondiente validado para el usuario.

---

## 📊 REGLAS DE NEGOCIO

- Sólo se considera la jerarquía declarada en `identity_role.hierarchy_level`.
- El rol con menor valor numérico equivale al mayor privilegio.
- Cambios en jerarquía requieren aprobación del comité de seguridad.

---

## 🗄️ BASE DE DATOS

Consulta utilizada:

```sql
SELECT slug, name, hierarchy_level
FROM identity_role
WHERE slug IN (%s)
ORDER BY hierarchy_level ASC, slug ASC
LIMIT 1;
```

---

## 📈 MÉTRICAS

- Número de usuarios con roles por encima del esperado.
- Tiempo promedio para evaluar privilegios (`p95` < 100 ms).

---

## 🔐 SEGURIDAD

- Registrar todas las evaluaciones en `audit_event` (acción `view`).
- Alertar si un rol crítico se asigna sin aprobación documentada.

---

## 💡 NOTAS

- Integrar este caso con SecurityRAT mapeando el requisito ASVS V4 (Control de Acceso).
- Útil para generar reportes de segregación de funciones en auditorías SOX.

---

**FIN DEL CASO DE USO UC-018**
