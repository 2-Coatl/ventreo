# UC-016: CATALOGAR ROLES JERÁRQUICOS DEL RBAC

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-016|
|**Nombre**|Catalogar roles jerárquicos del RBAC|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Gestión de Identidades|
|**Actores**|Super Admin (R001), Equipo de Seguridad (R008)|
|**Precondiciones**|Roles registrados en `identity_role`; API disponible|
|**Postcondiciones**|Listado jerarquizado de roles exportado|
|**Frecuencia de Uso**|Semanal o cuando se agregan roles|

---

## 🎯 DESCRIPCIÓN

Permite consultar el catálogo maestro de roles que gobierna el modelo financiero modular. Usa el endpoint de sólo lectura expuesto por `identity.views.RoleViewSet` para extraer slugs, nombres y nivel jerárquico, garantizando que los equipos de seguridad trabajen con la misma matriz que consume el RBAC del libro Excel.

**Objetivo:** Mantener sincronizada la documentación de roles con la implementación (`identity/models.py::Role`) y facilitar auditorías o integraciones externas.

---

## 👥 ACTORES

### Actor Principal: Super Admin (R001)

**Responsabilidades:**
- Ejecutar inventarios periódicos de roles.
- Compartir la jerarquía con equipos de cumplimiento.
- Detectar duplicidades o brechas en la matriz.

**Características:**
- Acceso API autenticado.
- Permisos de lectura en módulo `identity`.

### Actor Secundario: Equipo de Seguridad (R008)

**Responsabilidades:**
- Revisar que los roles alineen con políticas corporativas.
- Registrar cambios solicitados por auditorías.

**Características:**
- Recepción del catálogo exportado.

---

## 📝 PRECONDICIONES

### PRE-001: Roles sembrados
**Condición:** Deben existir registros en `identity_role`.
**Verificación:** `SELECT COUNT(*) FROM identity_role` > 0.

### PRE-002: Endpoint disponible
**Condición:** Servicio `GET /api/identity/roles/` accesible.
**Verificación:** Respuesta HTTP 200 con payload JSON.

### PRE-003: Token válido
**Condición:** Actor autenticado con permisos RBAC.
**Verificación:** Cabecera `Authorization` vigente.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Solicitar catálogo

```pseudocode
INICIO catalogar_roles_rbac
respuesta = http.get("/api/identity/roles/", headers={Authorization: token})
SI respuesta.status != 200 ENTONCES
    registrar_error("Fallo catálogo roles", respuesta.status)
    RETORNAR
FIN_SI
```

### Paso 2: Ordenar por jerarquía

```pseudocode
datos = respuesta.json()
roles_ordenados = ordenar_por(datos, clave="hierarchy_level")
```

### Paso 3: Exportar resultado

```pseudocode
tabla = formatear_tabla(
    columnas=["slug", "name", "hierarchy_level", "description"],
    filas=roles_ordenados,
)
exportar(tabla, destino="docs/security/catalogo_roles.csv")
```

### Paso 4: Compartir con stakeholders

```pseudocode
enviar_correo(
    asunto="Catálogo de roles actualizado",
    adjuntos=["docs/security/catalogo_roles.csv"],
    destinatarios=["seguridad@ventreo.com"],
)
```

---

## 🔀 FLUJOS ALTERNATIVOS

### FA-001: Catálogo vacío
**Condición:** `identity_role` sin registros.

```pseudocode
SI len(datos) == 0 ENTONCES
    mostrar_alerta("No hay roles definidos")
    abrir_ticket("Crear roles base en identity")
    RETORNAR
FIN_SI
```

### FA-002: Error de autenticación
**Condición:** Token inválido o vencido.

```pseudocode
SI respuesta.status == 401 ENTONCES
    solicitar_token_nuevo()
    reintentar_catalogar_roles()
    registrar_evento_seguridad(usuario_actual)
FIN_SI
```

---

## ✅ POSTCONDICIONES

1. **POST-001:** Catálogo exportado con jerarquía ascendente.
2. **POST-002:** Registro de auditoría `MODULE_CATALOG_ACCESSED` en `audit_event`.
3. **POST-003:** Equipo de seguridad informado vía correo.

---

## 📊 REGLAS DE NEGOCIO

- **RN-001:** Los slugs deben ser únicos (`identity_role.slug`).
- **RN-002:** Niveles jerárquicos menores representan mayor privilegio (`hierarchy_level`).
- **RN-003:** Ningún rol puede omitirse en reportes de cumplimiento.

---

## 🗄️ MODELO DE DATOS

Tabla `identity_role`:

```sql
CREATE TABLE identity_role (
    slug VARCHAR(50) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    hierarchy_level SMALLINT NOT NULL
);
```

---

## 📈 MÉTRICAS

- Tiempo de respuesta del endpoint (`p95` < 250 ms).
- Número de roles activos vs. planificados.
- Última fecha de sincronización documentada.

---

## 🔐 SEGURIDAD

- Endpoint protegido por autenticación JWT/Session.
- Monitorear intentos fallidos consecutivos (`audit_event` acción `login`).
- Catálogo exportado almacenado en repositorio privado.

---

## 💡 NOTAS

- Para automatizar la extracción, integrar con SecurityRAT y asociar cada rol a requisitos del estándar ASVS.
- Mantener versión del catálogo dentro de `docs/security/` junto con evidencia de aprobación.

---

**FIN DEL CASO DE USO UC-016**
