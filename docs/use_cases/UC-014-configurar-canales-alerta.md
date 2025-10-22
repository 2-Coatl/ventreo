# UC-014: CONFIGURAR CANALES DE ALERTA

## Sistema financiero Ventreo - Caso de Uso Completo

---

## 📋 INFORMACIÓN GENERAL

|Atributo|Valor|
|---|---|
|**Código**|UC-014|
|**Nombre**|Configurar canales de alerta|
|**Prioridad**|🟡 MEDIA|
|**Categoría**|Infraestructura de Notificaciones|
|**Actores**|Super Admin (R001), Equipo IT (externo)|
|**Precondiciones**|Canales registrados; reglas asociadas|
|**Postcondiciones**|Canales validados, pruebas exitosas|
|**Frecuencia de Uso**|Al habilitar nuevo canal o proveedor|

---

## 🎯 DESCRIPCIÓN

`notifications.views.AlertChannelViewSet` centraliza la configuración de email, Slack y webhooks que entregan las alertas financieras. El caso de uso asegura que la distribución sea confiable, segura y auditable.

**Objetivo:** Mantener canales operativos y correctamente enlazados a las reglas de alerta vigentes.

---

## 👥 ACTORES

- **Super Admin:** Gestiona la configuración desde el panel.
- **Equipo IT:** Valida conectividad con servicios externos (SMTP, Slack webhook).

---

## 📝 PRECONDICIONES

1. Existen registros en `notifications_alertchannel`.
2. Cada canal tiene `configuration` con credenciales o endpoints.
3. Al menos una regla asociada a cada canal.

---

## 🔄 FLUJO PRINCIPAL

### Paso 1: Consultar canales

```pseudocode
channels = GET /api/notifications/alert-channels/
validar_status(channels.status_code)
lista = channels.json()
```

### Paso 2: Validar configuración

```pseudocode
PARA canal EN lista
    verificar_tipo(canal['channel_type'])
    validar_configuracion(canal['configuration'])
    asegurar_reglas(canal['rules'])
FIN_PARA
```

### Paso 3: Ejecutar prueba de entrega

```pseudocode
resultado = POST /api/notifications/alert-channels/{canal['id']}/test {
    'rule_code': canal['rules'][0]['code'],
    'destino_prueba': correo_operaciones
}
SI resultado.status != 200 ENTONCES registrar_error()
```

### Paso 4: Actualizar configuración (si aplica)

```pseudocode
PATCH /api/notifications/alert-channels/{id}/ {
    'configuration': actualizar_tokens(canal['configuration'])
}
```

### Paso 5: Documentar en auditoría

```pseudocode
audit_log.record(AuditEntry(
    timestamp=ahora(),
    user=super_admin.email,
    role='super_admin',
    sheet='ALERT_CHANNELS',
    action='edit',
    description="Actualización canal " + canal['name']
))
```

---

## 🔀 FLUJOS ALTERNATIVOS

- **FA-001:** Canal sin reglas → se marca como inactivo y se notifica al CFO.
- **FA-002:** Prueba de envío falla → se hace rollback de configuración y se abre ticket con IT.
- **FA-003:** Token expirado → se genera alerta `alert_channel_expired_token`.

---

## ✅ POSTCONDICIONES

1. Canales operativos con pruebas recientes.
2. Configuración versionada (`configuration` cifrada en vault).
3. SecurityRAT requisito `ASVS V9` actualizado.

---

## 📊 REGLAS DE NEGOCIO

1. Webhooks deben firmarse con secreto compartido.
2. Correos se envían desde dominio corporativo verificado.
3. Slack requiere canal privado con historial retenido mínimo 90 días.

---

## 🗄️ CONSULTAS

```sql
SELECT name, channel_type, JSON_LENGTH(configuration) AS campos
FROM notifications_alertchannel;
```

---

## 📈 MÉTRICAS

- Tiempo promedio para recuperar un canal caído.
- Número de reglas por canal.

---

## 🔐 SEGURIDAD

- Configuración almacenada cifrada (KMS interno).
- Rotación de tokens cada 90 días.

---

## 💡 EJEMPLO

- Se agrega canal `Slack Ops`; se asocia a reglas `runway_critical` y `burn_over_budget`, se envía mensaje de prueba y se registra auditoría.

---

## ✅ CRITERIOS DE ACEPTACIÓN

1. Endpoint devuelve canales con reglas embebidas.
2. Prueba de entrega exitosa para cada canal activo.
3. Auditoría registra cambios.
4. SecurityRAT refleja estado actualizado.

---

**FIN DEL CASO DE USO UC-014**
