# UC-011: REVISAR MATRIZ DE PERMISOS POR HOJA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-011|
|**Nombre**|Revisar matriz de permisos por hoja|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Seguridad Operativa|
|**Actores**|Super Admin (R001), Controller (R006), Auditor (R005)|
|**Precondiciones**|Catálogo `access_control_sheet` poblado|
|**Postcondiciones**|Permisos confirmados, anomalías registradas|
|**Frecuencia de Uso**|Semanal o tras incidentes|

---

## 🎯 DESCRIPCIÓN

Este caso de uso permite inspeccionar la matriz RBAC hoja-rol expuesta por `access_control.views.SheetViewSet`. Facilita detectar privilegios excesivos y verificar consistencia con los casos de uso documentados.

**Objetivo:** Validar que cada rol cuente únicamente con los accesos necesarios, manteniendo el principio de menor privilegio.

---

## 👥 ACTORES

- **Super Admin:** Realiza auditorías completas y aplica correcciones.
- **Controller:** Verifica que gerentes solo vean su área.
- **Auditor:** Consulta matriz como parte de revisiones de cumplimiento.

---

## 📝 PRECONDICIONES

1. `Sheet` y `SheetPermission` con datos actualizados.
2. API disponible en `/api/access-control/sheets/`.
3. Usuario autenticado con permiso de lectura (`CallCenterPermission` admite GET anónimo, pero para diffs se requiere sesión).

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Consultar catálogo de hojas

```pseudocode
response = GET /api/access-control/sheets/?ordering=code
SI response.status != 200 ENTONCES registrar_error('SHEET_MATRIX_UNAVAILABLE')
matriz = response.json()
```

### Paso 2: Analizar permisos por hoja

```pseudocode
PARA hoja EN matriz
    mostrar(hoja.code, hoja.title)
    PARA permiso EN hoja.permissions
        evaluar_permiso(permiso.role.slug, permiso.can_read, permiso.can_write, permiso.can_approve, permiso.can_export)
    FIN_PARA
FIN_PARA
```

### Paso 3: Detectar desviaciones

```pseudocode
reglas = cargar_reglas('docs/use_cases/reglas_rbac.yaml')
para cada permiso evaluado
    SI viola(reglas[hoja], permiso)
        registrar_anomalia(hoja.code, permiso.role.slug)
        notificar('rbac_deviation', datos)
    FIN_SI
FIN_PARA
```

### Paso 4: Generar reporte

```pseudocode
exportar_csv(matriz, destino='reports/rbac_matrix_{fecha}.csv')
```

### Paso 5: Registrar auditoría

```pseudocode
audit_log.record(AuditEntry(
    timestamp=ahora(),
    user=actor.email,
    role=actor.rol_principal,
    sheet='RBAC_MATRIX',
    action='view',
    description='Consulta matriz permisos',
    metadata={'total_sheets': len(matriz)}
))
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Hoja sin permisos definidos → se genera tarea para asignar roles mínimos.
- **FA-002:** Permisos duplicados → se normaliza la tabla para evitar combinaciones contradictorias.
- **FA-003:** API sin respuesta → se utiliza backup `reports/rbac_matrix_latest.csv` y se abre incidente.

---

## ✅ POSTCONDICIONES

1. Reporte exportado y compartido con stakeholders.
2. Anomalías registradas en `audit_auditevent` como `view` + metadata `issues_detected`.
3. SecurityRAT requisito `ASVS V4.1.2` actualizado a "Monitored".

---

## 📊 REGLAS DE NEGOCIO

1. Cualquier hoja crítica (`code` que inicia con `26_` o `13_`) debe tener `can_write` limitado a CFO/Contador.
2. Roles de auditoría solo obtienen `can_read` y `can_export`.
3. Cambios a la matriz requieren ticket y aprobación del Super Admin.

---

## 🗄️ CONSULTAS ÚTILES

```sql
SELECT s.code, s.title, r.slug, sp.can_read, sp.can_write, sp.can_approve, sp.can_export
FROM access_control_sheet s
JOIN access_control_sheetpermission sp ON sp.sheet_id = s.id
JOIN identity_role r ON r.slug = sp.role_id
ORDER BY s.code, r.hierarchy_level;
```

---

## 📈 MÉTRICAS

- Número de anomalías por semana.
- Tiempo promedio de resolución (`audit_auditevent` acción `approve` en hoja `RBAC_MATRIX`).

---

## 🔐 SEGURIDAD

- Exportaciones se cifran antes de compartirse (`gpg --encrypt`).
- Resultados se almacenan en carpeta protegida `secure-reports/` con control de versiones.

---

## 💡 EJEMPLO

- Auditor detecta que rol `viewer` tiene `can_export` en `26_Calculadora_Impuestos`; se revoca y se documenta en SecurityRAT.

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. El endpoint devuelve permisos con roles embebidos (`identity.serializers.RoleSerializer`).
2. El reporte muestra al menos los campos requeridos.
3. Anomalías generan notificación automática.
4. Auditoría captura la consulta con metadata.

---

**FIN DEL CASO DE USO UC-011**
