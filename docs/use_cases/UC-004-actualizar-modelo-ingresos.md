# UC-004: ACTUALIZAR MODELO DE INGRESOS Y PRECIOS

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-004|
|**Nombre**|Actualizar precios y proyecciones de ingresos|
|**Prioridad**|🟠 ALTA|
|**Categoría**|Revenue Management|
|**Actores**|CFO (R002), CEO (R003), Analista Financiero (R007)|
|**Precondiciones**|Acceso a `09_Modelo_Precios` y `10_Proyeccion_Ventas`|
|**Postcondiciones**|Precios aplicados con aprobación, dashboards actualizados|
|**Frecuencia de Uso**|Trimestral|

---

## 🎯 DESCRIPCIÓN

Define cómo se proponen y aprueban cambios en precios, planes y proyecciones de ventas. Se apoya en `finance/domain.py::REVENUE_MODEL` para conectar hojas y roles de aprobación.

**Objetivo:** Mantener coherencia entre precios publicados, previsiones de MRR/LTV y visibilidad ejecutiva.

---

## 👥 ACTORES

### Actor Principal: CFO (R002)
- Propone nuevos precios.
- Evalúa sensibilidad y churn estimado.

### Actor de Soporte: Analista Financiero (R007)
- Modela escenarios alternos y documentación.

### Actor Decisor: CEO (R003)
- Aprueba incrementos superiores al 10%.

---

## 📝 PRECONDICIONES

1. Permisos `WRITE` en `09`, `10`, `11` para CFO/Analista.
2. Dashboards configurados con métricas `MRR`, `Churn`, `Runway`.
3. Alertas "pricing_change_pending" activas en `notifications`.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Propuesta de cambio

```pseudocode
nuevos_precios = analista.calcular_propuesta()
registrar_cambios('09_Modelo_Precios', nuevos_precios)
estado = 'PROPUESTO'
registrar_auditoria('PRICING_PROPOSED', detalles)
```

### Paso 2: Evaluación CFO

```pseudocode
impacto = calcular_metricas(nuevos_precios)
SI impacto.variacion_precio > 0.10
    requerir_aprobacion(CEO)
SINO
    aprobar_cfo()
```

### Paso 3: Aprobación CEO (si aplica)

```pseudocode
SI CEO.aprueba()
    estado = 'APROBADO_FINAL'
SINO
    estado = 'RECHAZADO'
```

### Paso 4: Aplicación y sincronización

```pseudocode
actualizar_hoja('09', nuevos_precios)
recalcular('10', '11', '13')
actualizar_dashboards()
notificar_equipo_comercial()
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Variación <5% → Solo CFO aprueba, CEO informado.
- **FA-002:** CEO pide ajustes → estado `REVISION_CEO` vuelve a CFO.
- **FA-003:** Test A/B → se crean columnas adicionales sin aplicar a proyecciones.

---

## ✅ POSTCONDICIONES

- Precios vigentes reflejados en todas las hojas dependientes.
- Dashboards ejecutivos actualizados con nuevas métricas.
- Registro de aprobación guardado en auditoría.

---

## 📊 REGLAS DE NEGOCIO

1. Ningún plan puede quedar con margen <30% sin aprobación especial.
2. Cambios deben comunicarse mínimo 14 días antes a clientes existentes.
3. Proyecciones deben incluir análisis de churn.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.domain.REVENUE_MODEL`
- `dashboards.models.DashboardKPI`
- `notifications.AlertRule` ("pricing_decision_pending")

---

## 📈 MÉTRICAS

- Incremento de MRR.
- Churn posterior al cambio.
- Tiempo de aprobación por cambio.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Cambios solo editables por CFO/Analista.
- CEO firma electrónicamente aprobaciones >10%.

---

**FIN DEL CASO DE USO UC-004**
