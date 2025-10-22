# UC-012: CONSULTAR FASES DEL PIPELINE FINANCIERO

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-012|
|**Nombre**|Consultar fases del pipeline financiero|
|**Prioridad**|🟠 MEDIA|
|**Categoría**|Documentación Operativa|
|**Actores**|Analista (R007), CFO (R002), Auditor (R005)|
|**Precondiciones**|Phases, Workflows y Outputs sincronizados|
|**Postcondiciones**|Mapa de fases consumido y referenciado|
|**Frecuencia de Uso**|Antes de releases o auditorías|

---

## 🎯 DESCRIPCIÓN

Expone la secuencia de fases, workflows y outputs definidos en `finance.models` mediante `PhaseViewSet`. Permite validar que cada caso de uso tenga soporte documental y que los dashboards reflejen salidas correctas.

**Objetivo:** Ofrecer una visión centralizada de cómo fluye la información desde la autenticación hasta los dashboards, alineando la arquitectura con los principios de Clean Architecture.

---

## 👥 ACTORES

- **Analista:** Usa el catálogo para preparar documentación o definir nuevas simulaciones.
- **CFO:** Revisa dependencias antes de aprobar cambios estructurales.
- **Auditor:** Comprueba trazabilidad de outputs y audiencias.

---

## 📝 PRECONDICIONES

1. Existencia de registros en `finance_phase`, `finance_workflow`, `finance_phaseoutput`.
2. Roles cargados para relaciones ManyToMany (`approval_roles`, `audience`).
3. Endpoint `/api/finance/phases/` disponible.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Obtener listado ordenado

```pseudocode
phases = GET /api/finance/phases/?ordering=order
validar_status(phases.status_code)
fases_json = phases.json()
```

### Paso 2: Documentar workflows y dependencias

```pseudocode
PARA fase EN fases_json
    registrar(fase['title'], fase['summary'])
    PARA wf EN fase['workflows']
        documentar_workflow(wf['name'], wf['sheet'], wf['approval_roles'])
    FIN_PARA
    PARA output EN fase['outputs']
        documentar_output(output['label'], output['sheet'], output['audience'])
    FIN_PARA
FIN_PARA
```

### Paso 3: Mapear a casos de uso

```pseudocode
mapa = cargar('docs/use_cases.md')
PARA fase EN fases_json
    vincular_uc = buscar_uc_por_sheet(fase, mapa)
    actualizar_documento(vincular_uc, fase['slug'])
FIN_PARA
```

### Paso 4: Generar infografía o pipeline

```pseudocode
crear_diagrama_mermaid(fases_json, destino='docs/pipeline_diagram.mmd')
```

### Paso 5: Validar consistencia

```pseudocode
SI falta_sheet_en_domain(fases_json, finance/domain.py)
    crear_issue('PIPELINE_MISMATCH', detalle)
FIN_SI
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Fase sin workflows → se marca como pendiente de definir (status `draft`).
- **FA-002:** Roles ausentes → se solicita a identidad completar catálogos.
- **FA-003:** Endpoint fuera de línea → se usa respaldo `docs/data_flow_pipeline.md`.

---

## ✅ POSTCONDICIONES

1. Documento actualizado con referencia cruzada fase ↔ caso de uso.
2. Diagrama del pipeline almacenado en `docs/`.
3. SecurityRAT etiqueta requisitos por fase (`tag = fase.slug`).

---

## 📊 REGLAS DE NEGOCIO

1. El orden de fases debe coincidir con `order` ascendente.
2. Todo workflow con `requires_approval = TRUE` necesita al menos un rol aprobador.
3. Outputs deben mapear a dashboards existentes (`dashboards/models.Dashboard`).

---

## 🗄️ CONSULTAS

```sql
SELECT p.slug, p.title, w.name, o.label
FROM finance_phase p
LEFT JOIN finance_workflow w ON w.phase_id = p.id
LEFT JOIN finance_phaseoutput o ON o.phase_id = p.id
ORDER BY p.order;
```

---

## 📈 MÉTRICAS

- Conteo de workflows por fase.
- Número de outputs por audiencia (CFO, CEO, etc.).

---

## 🔐 SEGURIDAD

- Solo lectura; se recomienda exponer API bajo autenticación básica si se publica externamente.
- Auditoría registra acción `view` con metadata `phase_count`.

---

## 💡 EJEMPLO

- Analista exporta JSON y genera diagrama que muestra Fase 0 (autenticación), Fase 2 (inversiones), Fase 7 (escenarios) enlazados con dashboards `30-33`.

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. Endpoint retorna fases con workflows y outputs anidados.
2. Cada fase tiene coincidencia con al menos un caso de uso en `docs/use_cases.md`.
3. Se genera diagrama actualizado.
4. Auditoría documenta la consulta.

---

**FIN DEL CASO DE USO UC-012**
