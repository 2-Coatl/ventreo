# UC-007: GESTIONAR ESCENARIOS Y SIMULACIONES

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-007|
|**Nombre**|Gestionar escenarios y simulaciones|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Planeación Estratégica|
|**Actores**|Analista Financiero (R007), CFO (R002), CEO (R003)|
|**Precondiciones**|Hojas `19_Escenarios`, `20_Montecarlo`, `25_Simulador_Interactivo` habilitadas|
|**Postcondiciones**|Escenario aprobado y comunicado|
|**Frecuencia de Uso**|Mensual / según comité|

---

## 🎯 DESCRIPCIÓN

Estandariza la creación, validación y publicación de escenarios financieros. Usa `finance/domain.py::SCENARIO_PLANNING` como blueprint de hojas y roles.

**Objetivo:** Evaluar alternativas de crecimiento y riesgos antes de ejecutarlas.

---

## 👥 ACTORES

- **Analista:** Diseña supuestos y corre simulaciones Montecarlo.
- **CFO:** Valida consistencia y decide exposición.
- **CEO/Board:** Aprueban escenarios oficiales.

---

## 📝 PRECONDICIONES

1. Datos base actualizados en ingresos y costos.
2. Permisos `WRITE` para Analista/CFO en hojas de control.
3. Reglas de notificación "scenario_pending" disponibles.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Crear escenario

```pseudocode
escenario = analista.crear(
    nombre,
    supuestos={crecimiento, churn, CAC, headcount},
    estado='BORRADOR'
)
registrar_auditoria('SCENARIO_DRAFTED', escenario)
```

### Paso 2: Simulación Montecarlo

```pseudocode
resultados = montecarlo.ejecutar(iteraciones=1000, supuestos)
hoja20.actualizar(resultados)
```

### Paso 3: Envío a validación CFO

```pseudocode
escenario.estado='PENDIENTE_CFO'
notificar(CFO, 'scenario_pending')
```

### Paso 4: Revisión CFO

```pseudocode
if CFO.aprueba():
    escenario.estado='PENDIENTE_CEO'
    notificar(CEO)
else:
    escenario.estado='REVISION_ANALISTA'
```

### Paso 5: Aprobación CEO/Board

```pseudocode
if CEO.aprueba():
    escenario.estado='OFICIAL'
    activar_en_hoja_control()
    dashboards.marcar_escenario_activo()
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Escenario rechazado → vuelve a Analista con comentarios.
- **FA-002:** Simulación falla → log "scenario_simulation_error" al Super Admin.
- **FA-003:** Escenario urgente → CFO puede aprobar temporalmente como "PROVISIONAL".

---

## ✅ POSTCONDICIONES

- Escenario oficial marcado en `01_Parametros`.
- Dashboards muestran métricas del escenario activo.
- Auditoría conserva supuestos y aprobaciones.

---

## 📊 REGLAS DE NEGOCIO

1. Máximo 5 escenarios activos simultáneamente.
2. Escenarios deben documentar supuestos críticos.
3. Simulaciones Montecarlo mínimas 1,000 iteraciones.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.domain.SCENARIO_PLANNING`
- `dashboards.models.Dashboard`
- `notifications.AlertRule` ("scenario_pending")

---

## 📈 MÉTRICAS

- Valor esperado de EBITDA por escenario.
- Probabilidad de alcanzar objetivo de crecimiento.
- Tiempo de ciclo de aprobación.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Solo Analista y CFO pueden editar supuestos.
- CEO/Board firman aprobación final.

---

**FIN DEL CASO DE USO UC-007**
