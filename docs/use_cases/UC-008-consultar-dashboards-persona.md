# UC-008: CONSULTAR DASHBOARDS PERSONALIZADOS POR PERSONA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-008|
|**Nombre**|Consultar dashboards por rol|
|**Prioridad**|🟢 MEDIA|
|**Categoría**|Business Intelligence|
|**Actores**|CEO (R003), CFO (R002), Contador (R004), Gerente (R006), Super Admin (R001)|
|**Precondiciones**|Dashboards `30`–`33` generados; RBAC aplicado|
|**Postcondiciones**|Indicadores consumidos según rol|
|**Frecuencia de Uso**|Diaria|

---

## 🎯 DESCRIPCIÓN

Establece cómo cada persona accede a su dashboard con métricas y acciones relevantes. Se apoya en `finance/domain.py::DASHBOARD_VIEWS`.

**Objetivo:** Entregar información accionable acorde al rol sin exponer datos innecesarios.

---

## 👥 ACTORES

- **CEO:** Dashboard 30 con runway, decisiones pendientes.
- **CFO:** Dashboard 31 con liquidez e impuestos.
- **Contador:** Dashboard 32 con obligaciones fiscales.
- **Gerente:** Dashboard 33 con costos de su área.
- **Super Admin:** Acceso total para soporte.

---

## 📝 PRECONDICIONES

1. Caso UC-001 ejecutado (permisos aplicados).
2. Dashboards alimentados por cálculos actualizados.
3. Definiciones en `dashboards.configs` sincronizadas.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Redirección post login

```pseudocode
dashboard = dashboards.services.resolve_home_dashboard(usuario.roles)
libro.ir_a(dashboard.sheet)
```

### Paso 2: Render de métricas

```pseudocode
para cada widget en dashboard.highlighted_metrics:
    valor = obtener_metricas(widget)
    mostrar_card(widget, valor)
```

### Paso 3: Acciones sugeridas

```pseudocode
acciones = dashboards.services.resolve_actions(rol)
mostrar_lista(acciones)
```

### Paso 4: Exportación opcional

```pseudocode
si usuario.permite_exportar:
    habilitar_boton('Exportar PDF/CSV')
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Rol sin dashboard asignado → fallback a dashboard ejecutivo.
- **FA-002:** Métrica no disponible → se muestra badge "Dato en actualización".
- **FA-003:** Usuario solicita dashboard de otra persona → acceso denegado, se registra intento.

---

## ✅ POSTCONDICIONES

- Usuario visualiza indicadores correspondientes.
- No se exponen métricas fuera del alcance.
- Auditoría registra acceso `DASHBOARD_VIEWED`.

---

## 📊 REGLAS DE NEGOCIO

1. Solo dashboards enumerados en `DASHBOARD_VIEWS` son válidos.
2. Exportación restringida a roles CFO, CEO, Contador.
3. Actualización automática cada recálculo de pipeline.

---

## 🗄️ ENTIDADES RELACIONADAS

- `finance.domain.DASHBOARD_VIEWS`
- `dashboards.models.Dashboard`
- `audit.models.AuditEvent`

---

## 📈 MÉTRICAS

- Frecuencia de acceso por rol.
- Tiempo promedio en dashboard.
- Número de exportaciones realizadas.

---

## 🔐 SEGURIDAD Y AUDITORÍA

- Registro de intentos de acceso no autorizado.
- Contenido sensible enmascarado según rol.

---

**FIN DEL CASO DE USO UC-008**
