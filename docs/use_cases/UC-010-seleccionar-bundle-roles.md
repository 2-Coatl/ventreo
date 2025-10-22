# UC-010: SELECCIONAR BUNDLE DE ROLES SEGÚN TAMAÑO DE EMPRESA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-010|
|**Nombre**|Seleccionar bundle de roles según tamaño de empresa|
|**Prioridad**|🟠 MEDIA|
|**Categoría**|Gobernanza de Identidades|
|**Actores**|Super Admin (R001), CEO (R003)|
|**Precondiciones**|Catálogo de roles poblado; usuario con permiso de administración|
|**Postcondiciones**|Bundle recomendado asignado y comunicado|
|**Frecuencia de Uso**|Al onboarding o al crecer de tier|

---

## 🎯 DESCRIPCIÓN

Los bundles definidos en `identity.models.RoleBundle` condensan configuraciones recomendadas de roles según el tamaño de la compañía. Este caso de uso permite seleccionar la combinación adecuada y propagarla hacia `access_control` y `finance`.

**Objetivo:** Garantizar que cada etapa de madurez cuente con los roles mínimos necesarios y que la matriz RBAC refleje dicha selección.

---

## 👥 ACTORES

### Actor Principal: Super Admin (R001)

- Responsable de hardening inicial y escalamiento de permisos.
- Accede al endpoint `identity.RoleBundleViewSet` para consultar bundles disponibles.
- Ejecuta scripts de asignación en `scripts/bootstrap_rbac.py` (si existiera).

### Actor Colaborador: CEO (R003)

- Confirma que la recomendación se alinea con estructura organizacional.
- Autoriza creación de cuentas nuevas si el bundle incrementa roles activos.

---

## 📝 PRECONDICIONES

1. **PRE-001:** Existen roles base en `identity_role` y jerarquía definida.
2. **PRE-002:** `RoleBundle` tiene relaciones M2M pobladas (`identity_rolebundle_roles`).
3. **PRE-003:** Usuario autenticado posee privilegios de Super Admin (`hierarchy_level = 1`).

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Consultar bundles disponibles

```pseudocode
response = GET /api/identity/role-bundles/
SI response.status != 200 ENTONCES
    registrar_error('ROLE_BUNDLE_LIST_FAILED')
    RETORNAR
FIN_SI
bundles = response.json()
```

### Paso 2: Seleccionar bundle compatible

```pseudocode
criterios = {
    'micro': {'personas': 3, 'roles_requeridos': ['CEO','CONTADOR']},
    'pequena': {'personas': 8, 'roles_requeridos': ['CEO','CFO','CONTROLLER','GERENTE']},
    'mediana': {'personas': 25, 'roles_requeridos': ['CEO','CFO','CONTROLLER','CONTADOR','ANALISTA','GERENTE','AUDITOR']},
    'grande': {'personas': 120, 'roles_requeridos': ['SUPER_ADMIN','CEO','CFO','CONTROLLER','CONTADOR','ANALISTA','GERENTE','AUDITOR']}
}
perfil_empresa = evaluar_datos_empresa()
 bundle = elegir_bundle(bundles, perfil_empresa)
```

### Paso 3: Comunicar asignación

```pseudocode
POST /api/identity/role-bundles/{bundle.key}/select
 payload = {
    'empresa': perfil_empresa.nombre,
    'justificacion': generar_justificacion(bundle, perfil_empresa),
    'usuarios_involucrados': listar_usuarios_por_rol(bundle)
 }
```

### Paso 4: Propagar a matriz de permisos

```pseudocode
PARA rol EN bundle.roles
    asegurar_permiso_sheet(rol, '28_Control_Acceso_RBAC')
    actualizar_sheet_permissions(rol)
FIN_PARA
sincronizar_finance_phase_outputs(bundle.roles)
```

### Paso 5: Registrar auditoría y SecurityRAT

```pseudocode
audit_log.record(AuditEntry(
    timestamp=ahora(),
    user=super_admin.email,
    role='super_admin',
    sheet='28_Control_Acceso_RBAC',
    action='approve',
    description=f'Selección bundle {bundle.key}'
))
securityrat.update_requirement('ASVS-V4.1', status='In progress', notes=bundle.key)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Bundle inexistente
- Endpoint retorna 404.
- Se propone crear bundle custom (`POST /api/identity/role-bundles/`).

### FA-002: Falta de licencias para roles nuevos
- Integración con HR marca error y se registra issue `RBAC_LICENSING_BLOCKED`.

### FA-003: CEO rechaza recomendación
- Super Admin documenta rechazo y mantiene bundle actual.
- Se agenda revisión trimestral.

---

## ✅ POSTCONDICIONES

1. Bundle seleccionado queda registrado en bitácora y comunicado al equipo.
2. Matriz `access_control_sheetpermission` refleja nuevos roles.
3. Dashboards de `dashboards/configs.py` muestran audiencias actualizadas.

---

## 📊 REGLAS DE NEGOCIO

1. **RN-001:** Roles de jerarquía ≤2 no pueden coexistir en un mismo usuario sin MFA.
2. **RN-002:** Bundle `micro` permite roles acumulados en una sola persona.
3. **RN-003:** Cambios de bundle requieren notificación al área de cumplimiento.

---

## 🗄️ DATOS RELACIONADOS

```sql
SELECT rb.key, r.slug
FROM identity_rolebundle rb
JOIN identity_rolebundle_roles rbr ON rb.id = rbr.rolebundle_id
JOIN identity_role r ON rbr.role_id = r.slug;
```

---

## 📈 MÉTRICAS

- **Cobertura de roles por bundle:**

```sql
SELECT rb.key, COUNT(rbr.role_id) AS total_roles
FROM identity_rolebundle rb
LEFT JOIN identity_rolebundle_roles rbr ON rb.id = rbr.rolebundle_id
GROUP BY rb.key;
```

- **Tiempo de adopción:** Medir días desde selección hasta asignación completa (`user_roles`).

---

## 🔐 SEGURIDAD

- Endpoint protegido por `CallCenterPermission` (lectura libre, escritura restringida).
- SecurityRAT requisito `ASVS V2` vinculado para garantizar autenticación robusta.

---

## 💡 EJEMPLOS

- Startup de 4 personas selecciona bundle `pequena`; CFO obtiene permisos de aprobación y se habilita dashboard `31_Dashboard_CFO`.
- Escalamiento a `mediana` incorpora rol de Auditor y activa vistas en `29_Auditoria_Cambios`.

---

## 🎨 INTERFAZ (wireframe API explorer)

```
GET /api/identity/role-bundles/
┌────────────────────────────────┐
│ key      title        roles    │
├────────────────────────────────┤
│ micro    Micro Tier   [ceo,…]  │
│ pequena  Small Tier   [ceo,cfo]│
│ mediana  Mid Tier     […]      │
│ grande   Enterprise   […]      │
└────────────────────────────────┘
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. El endpoint lista bundles con roles anidados.
2. Selección queda auditada y vincula SecurityRAT.
3. Matriz de permisos se actualiza para cada rol del bundle.
4. Si el CEO rechaza, se documenta y mantiene estado previo.

---

**FIN DEL CASO DE USO UC-010**
