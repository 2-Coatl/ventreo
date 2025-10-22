# UC-006: CUMPLIR OBLIGACIONES FISCALES Y CIERRE CONTABLE

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-006|
|**Nombre**|Preparar y aprobar declaraciones fiscales|
|**Prioridad**|🔴 CRÍTICA|
|**Categoría**|Compliance|
|**Actores**|Contador (R004), CFO (R002), CEO (R003), Auditor (R008)|
|**Precondiciones**|Hojas `26_Calculadora_Impuestos` y `27_Depreciacion_Equipamiento` disponibles|
|**Postcondiciones**|Declaración aprobada y registrada|
|**Frecuencia de Uso**|Mensual / Bimestral|

---

## 🎯 DESCRIPCIÓN

Documenta el proceso de cálculo, validación y aprobación de impuestos (IVA, ISR, IMSS). Deriva de `finance/domain.py::TAX_COMPLIANCE`.

**Objetivo:** Garantizar que cada declaración sea revisada por Contador y CFO, con aprobación ejecutiva cuando aplique y registro completo en auditoría.

---

## 👥 ACTORES

- **Contador:** Calcula y llena formatos, adjunta soportes.
- **CFO:** Valida resultados y autoriza pagos.
- **CEO:** Aprueba montos extraordinarios.
- **Auditor:** Acceso de solo lectura para control interno/externo.

---

## 📝 PRECONDICIONES

1. Nóminas y costos actualizados en hojas previas.
2. Recordatorios generados por `CASH_FLOW.alert_rules['tax_deadline']`.
3. Permisos `RWA` exclusivos para Contador en `26` y `27`.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Preparación de cálculos

```pseudocode
contabilidad = recolectar_datos(
    ventas=hoja10.total,
    compras=hoja05.deducibles,
    nomina=hoja07.total
)
hoja26.actualizar(contabilidad)
```

### Paso 2: Captura Contador

```pseudocode
contabilizar():
    completar_campos_formulario()
    adjuntar_comprobantes()
    estado='PENDIENTE_CFO'
    registrar_auditoria('TAX_DRAFTED')
```

### Paso 3: Revisión CFO

```pseudocode
validar = CFO.revisar(hoja26)
SI validar.aprobado
    estado='APROBADO_CFO'
    if validar.monto > limite_ceo:
        notificar(CEO)
SINO
    estado='CORRECCIONES'
```

### Paso 4: Firma CEO (si aplica)

```pseudocode
if monto_total > limite_ceo:
    CEO.aprobar()
    estado='APROBADO_FINAL'
```

### Paso 5: Registro y cierre

```pseudocode
registrar_pago(fecha_pago, folio)
notificar('tax_filed', destinatarios=[CFO, Contador])
audit.register('TAX_FILED', detalles={folio, montos})
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Ajustes solicitados por CFO → estado `CORRECCIONES` vuelve al Contador.
- **FA-002:** Declaración fuera de plazo → alerta crítica "tax_overdue".
- **FA-003:** Auditor requiere evidencia → se habilita exportación readonly.

---

## ✅ POSTCONDICIONES

- Declaración marcada como "DECLARADO" con folio.
- Dashboards `31` y `32` reflejan estatus actualizado.
- Auditoría contiene detalle de cálculos y aprobaciones.

---

## 📊 REGLAS DE NEGOCIO

1. Todas las celdas fiscales bloqueadas tras aprobación final.
2. Folios oficiales deben registrarse antes de cerrar periodo.
3. Ajustes posteriores requieren nota de crédito documentada.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.domain.TAX_COMPLIANCE`
- `audit.models.AuditEvent`
- `notifications.AlertRule` ("tax_deadline", "tax_overdue")

---

## 📈 MÉTRICAS

- Tiempo desde borrador a aprobación final.
- Diferencia entre impuestos calculados y pagados.
- Número de incidencias por periodo.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Solo Contador puede editar; CFO y CEO firman digitalmente.
- Auditor tiene permisos `READ` y exportación controlada.

---

**FIN DEL CASO DE USO UC-006**
