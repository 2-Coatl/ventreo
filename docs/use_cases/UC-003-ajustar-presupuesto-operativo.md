# UC-003: AJUSTAR PRESUPUESTO OPERATIVO POR ÁREA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-003|
|**Nombre**|Solicitar y aprobar ajustes de costos|
|**Prioridad**|🟠 ALTA|
|**Categoría**|Control Presupuestal|
|**Actores**|Gerente Operativo (R006), Controller (R005), CFO (R002), CEO (R003)|
|**Precondiciones**|Acceso filtrado a `05_Costos_Fijos` y `06_Costos_Variables`|
|**Postcondiciones**|Presupuesto actualizado con aprobaciones registradas|
|**Frecuencia de Uso**|Mensual|

---

## 🎯 DESCRIPCIÓN

Controla cómo cada gerente solicita incrementos o recortes en su presupuesto, con visibilidad restringida a su área y aprobaciones escalonadas según monto. Se sustenta en `finance/domain.py::COST_STRUCTURE` y `access_control` para filtros automáticos.

**Objetivo:** Mantener trazabilidad y privacidad en la modificación de costos fijos/variables y nóminas.

---

## 👥 ACTORES

### Actor Principal: Gerente Operativo (R006)
- Propone ajustes de gasto.
- Justifica con métricas de su área.

### Aprobadores: Controller, CFO, CEO
- Controller revisa montos bajos.
- CFO y CEO intervienen según umbrales.

---

## 📝 PRECONDICIONES

1. Hoja `05_Costos_Fijos` accesible en modo filtrado (`resolve_sheet_permissions`).
2. Workflow de aprobación configurado en `notifications.AlertRule` ("budget_request_pending").
3. Datos actuales sincronizados con nómina (`07`, `08`).

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Creación de solicitud

```pseudocode
solicitud = {
  area: gerente.area,
  concepto: formulario.concepto,
  monto_mensual: formulario.monto,
  periodo: formulario.periodo,
  justificante: formulario.justificacion,
  estado: 'PENDIENTE_CONTROLLER'
}
insertar_en_hoja('05_Costos_Fijos', solicitud)
registrar_auditoria('BUDGET_REQUESTED', solicitud)
```

### Paso 2: Revisión Controller

```pseudocode
SI monto_mensual <= 1000
    aprobar_automatico('Controller')
    notificar(CFO, 'Solicitud informativa')
SINO
    esperar_decision_controller()
FIN
```

### Paso 3: Aprobación CFO/CEO

```pseudocode
UMBRAL_CFO = 5000
UMBRAL_CEO = 25000

SI monto_mensual > UMBRAL_CFO
    requerir_aprobacion(CFO)
SI monto_mensual > UMBRAL_CEO
    requerir_aprobacion(CEO)
```

### Paso 4: Aplicación de presupuesto

```pseudocode
actualizar_celdas(area, concepto, monto)
recalcular('13_Flujo_Efectivo')
recalcular('14_Margen_Contribucion')
notificar_involucrados('budget_request_resolved')
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Gerente sin área asignada → mensaje informativo, se notifica al Controller.
- **FA-002:** Filtros sin resultados → tabla vacía, se invita a limpiar filtros.
- **FA-003:** Error BD → se levanta alerta a `Super Admin` y se muestra mensaje amigable.

---

## ✅ POSTCONDICIONES

- Presupuesto actualizado y protegido.
- Auditoría lista para revisión (`audit_event` con `workflow='budget'`).
- Dashboards (`33_Dashboard_Operaciones`) reflejan nuevo gasto.

---

## 📊 REGLAS DE NEGOCIO

1. Ajustes >20% requieren plan de mitigación adjunto.
2. Módulos obligatorios (sueldos base) no pueden quedar en cero.
3. No se permiten dependencias circulares entre centros de costo.

---

## 🗄️ ENTIDADES RELACIONADAS

- `access_control.services.resolve_sheet_permissions`
- `notifications.models.AlertRule`
- `audit.models.AuditEvent`

---

## 📈 MÉTRICAS

- Tiempo de ciclo por solicitud.
- % solicitudes aprobadas vs rechazadas.
- Desviación mensual frente a presupuesto original.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Cada cambio de celda sensible queda firmado por rol aprobador.
- Acceso restringido por filtros automáticos.

---

**FIN DEL CASO DE USO UC-003**
