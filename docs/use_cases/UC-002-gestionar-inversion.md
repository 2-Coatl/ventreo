# UC-002: GESTIONAR PROPUESTA DE INVERSIÓN CAPEX/OPEX

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-002|
|**Nombre**|Gestionar propuesta de inversión|
|**Prioridad**|🟠 ALTA|
|**Categoría**|Planeación Financiera|
|**Actores**|Controller (R005), CFO (R002), CEO (R003)|
|**Precondiciones**|Hoja `02_Inversion_Inicial` accesible; workflow activo|
|**Postcondiciones**|Solicitud aprobada/rechazada con trazabilidad|
|**Frecuencia de Uso**|Semanal / según necesidades de inversión|

---

## 🎯 DESCRIPCIÓN

El caso de uso define cómo se registran, evalúan y aprueban inversiones dentro del modelo financiero. Alinea las etapas del workflow descrito en `finance/domain.py::INVESTMENT_WORKFLOW` con los actores y hojas dependientes.

**Objetivo:** Garantizar que toda inversión mayor a $50,000 tenga aprobación escalonada y actualice automáticamente depreciación, impuestos y flujo de efectivo.

---

## 👥 ACTORES

### Actor Principal: Controller (R005)

**Responsabilidades:**
- Capturar propuestas con sustento.
- Adjuntar documentación de soporte.
- Atender observaciones del CFO.

### Actores Secundarios: CFO (R002) y CEO (R003)

- Validar impacto financiero.
- Autorizar niveles de aprobación.
- Comunicar decisiones al equipo.

---

## 📝 PRECONDICIONES

1. **PRE-001:** Controller con permiso `WRITE` en `02_Inversion_Inicial` (`access_control.SheetPermission`).
2. **PRE-002:** Workflow configurado con umbral `auto_approval_threshold=50000`.
3. **PRE-003:** Depreciación y cálculo fiscal enlazados (`27_Depreciacion_Equipamiento`, `26_Calculadora_Impuestos`).

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Registro de propuesta

```pseudocode
controller = usuario_actual
monto = formulario.monto
IF monto <= 0 THEN lanzar_error("Monto inválido")
insertar_fila(
    hoja='02_Inversion_Inicial',
    datos={concepto, monto, fecha, justificacion, estado='PROPUESTO'}
)
registrar_auditoria("INVESTMENT_PROPOSED", controller, monto)
```

### Paso 2: Evaluación automática

```pseudocode
impacto = finanzas.calcular_impacto(monto)
SI monto > INVESTMENT_WORKFLOW.auto_approval_threshold
    estado = 'PENDIENTE_CFO'
    notificar(CFO, 'Nueva inversión pendiente')
SINO
    estado = 'APROBADO_AUTO'
    aplicar_cambios()
FIN
```

### Paso 3: Aprobación CFO

```pseudocode
SI CFO.aprueba()
    actualizar_estado('APROBADO_CFO')
    notificar(CEO, 'Inversión requiere aprobación final')
SINO
    actualizar_estado('RECHAZADO_CFO')
    notificar(controller, 'Rechazo con comentarios')
```

### Paso 4: Aprobación CEO

```pseudocode
SI CEO.aprueba()
    actualizar_estado('APROBADO_FINAL')
    aplicar_cambios_financieros()
SINO
    actualizar_estado('RECHAZADO_CEO')
```

### Paso 5: Aplicación de efectos

```pseudocode
aplicar_cambios_financieros():
    depreciacion.actualizar(item)
    impuestos.recalcular()
    cashflow.recalcular()
    dashboards.actualizar_metricas()
    registrar_auditoria("INVESTMENT_APPLIED", datos)
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Monto bajo (<$50k) → Autoaprobación Controller, CFO/CEO informados.
- **FA-002:** Solicitud incompleta → Estado `REVISION_REQUERIDA`, se solicita documentación.
- **FA-003:** Rechazo CFO → Fin del flujo; Controller debe reingresar propuesta.
- **FA-004:** CEO solicita cambios → Estado `AJUSTES_SOLICITADOS`, regresa a Controller.

---

## ✅ POSTCONDICIONES

- Línea registrada con estado final y firmas digitales.
- Dependencias recalculadas (`27`, `26`, `13`).
- Evento de auditoría con detalle de aprobaciones.

---

## 📊 REGLAS DE NEGOCIO

1. **RN-001:** Propuestas ≥$250k requieren adjuntar ROI anual > 20%.
2. **RN-002:** Solo el Controller puede editar propuestas en estado `PROPUESTO`.
3. **RN-003:** Aprobaciones deben completarse en ≤3 días hábiles.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.models.InvestmentProposal` (siembra inicial).
- `audit.models.AuditEvent`.
- `notifications.models.AlertRule` (alerta "investment_pending").

---

## 📈 MÉTRICAS

- Tiempo promedio de aprobación.
- Número de propuestas por mes.
- ROI acumulado post implementación.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Firma digital de CFO/CEO almacenada en `audit_event.details`.
- Historial disponible para auditorías externas.

---

**FIN DEL CASO DE USO UC-002**
