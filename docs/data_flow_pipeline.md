# 3.5 SecurityRAT

> **Nota:** La integración específica para el modelo financiero se detalla en [`docs/security/securityrat.md`](security/securityrat.md), donde se enlazan los requisitos ASVS con los casos de uso UC-001–UC-022.

El ==[OWASP SecurityRAT]== (Requirement Automation Tool - Herramienta de Automatización de Requisitos) se utiliza para generar y gestionar requisitos de seguridad usando información del proyecto ==[OWASP ASVS]==. También proporciona un enfoque automatizado para la gestión de requisitos durante el desarrollo de aplicaciones frontend, de servidor y móviles.

> Nota contextual importante: SecurityRAT es una herramienta complementaria del ASVS que facilita la gestión práctica de los más de 280 requisitos de seguridad que propone el estándar ASVS, haciéndolos más manejables para equipos de desarrollo.

Actualmente es un proyecto Incubador de OWASP, pero es probable que pronto sea actualizado a estado de Laboratorio.

---

## ¿QUÉ ES SECURITYRAT?

[_SecurityRAT es una herramienta complementaria para el conjunto de requisitos del ASVS; puede utilizarse para generar un conjunto inicial de requisitos del ASVS y luego realizar un seguimiento del estado y las actualizaciones de estos requisitos._] Viene con [documentación e instrucciones](https://securityrat.github.io/) sobre cómo instalar y ejecutar SecurityRAT.

Para generar la lista inicial de requisitos, SecurityRAT necesita que se le proporcionen tres atributos definidos por el ASVS:

- **ID del capítulo del Application Security Verification Standard (Estándar de Verificación de Seguridad de Aplicaciones)** - por ejemplo 'V2 - Autenticación'
- **Nivel de Verificación de Seguridad de Aplicaciones** - el nivel de cumplimiento, por ejemplo 'L2'
- **Autenticación** - si se utiliza o no autenticación de inicio de sesión único (SSO)

> Concepto Clave: SecurityRAT transforma los 280+ requisitos del ASVS en un subconjunto manejable y específico para cada proyecto, basándose en tres parámetros clave: capítulo ASVS, nivel de verificación requerido (L1/L2/L3) y tipo de autenticación.

SecurityRAT luego genera una lista inicial de requisitos recomendados. Esta lista puede almacenarse en una base de datos de SecurityRAT que permite el seguimiento y actualización del conjunto de requisitos. SecurityRAT también proporciona integración con Atlassian JIRA para registrar y rastrear problemas de software.

La serie OWASP Spotlight proporciona una descripción general de lo que puede hacer Security Rat y cómo usarlo: 'Proyecto 5 - [OWASP SecurityRAT](https://youtu.be/ythaa6nRa0Y)'.

---

## ¿POR QUÉ USARLO?

Al momento de escribir esto, el ASVS tiene más de 280 requisitos sugeridos para el desarrollo seguro de software. Este número de requisitos lleva tiempo revisarlos y determinar si son aplicables o no a un proyecto de desarrollo determinado.

[_El uso de SecurityRAT para crear un subconjunto más manejable de los requisitos del ASVS es un beneficio directo tanto para los arquitectos de seguridad como para el equipo de desarrollo._] Además, SecurityRAT proporciona el seguimiento y actualización de este conjunto de requisitos a lo largo del ciclo de desarrollo, agregando seguridad a la aplicación al ayudar a garantizar que se cumplan los requisitos de seguridad.

---

## CÓMO USAR SECURITYRAT

Instale tanto las aplicaciones SecurityRAT de Producción como de Desarrollo descargando una versión e instalándola en el Java Development Kit JDK11. Alternativamente, descargue y ejecute la [imagen de docker](https://hub.docker.com/r/securityrat/securityrat) desde DockerHub. Configure SecurityRAT consultando la [documentación de implementación](https://securityrat.github.io/); esto no es tan sencillo, así que para comenzar hay una [demostración en línea](https://securityrat.github.io/#/demo) disponible.

#### Pasos recomendados para el entorno Ventreo

1. **Preparar el entorno local:**
   - Instalar JDK 11 (`sudo apt install openjdk-11-jdk`) o habilitar Docker según la política de la organización.
   - Clonar este repositorio y ubicar la carpeta `docs/use_cases/`, que servirá como insumo para etiquetar requisitos por caso de uso.
2. **Levantar SecurityRAT:**
   - Opción Docker: `docker run -p 8080:8080 securityrat/securityrat:latest`.
   - Opción local: descargar el `.war`, ejecutar `java -jar securityrat.war` y verificar disponibilidad en `http://localhost:8080`.
3. **Importar contexto del modelo financiero:**
   - Crear un proyecto SecurityRAT llamado `ventreo-rbac`.
   - Registrar como atributos personalizados los slugs de roles definidos en `identity/models.py`.
   - Cargar como "artefactos previos" los tableros y fases descritos en `finance/domain.py` para mantener trazabilidad con los casos de uso.
4. **Generar el primer set de requisitos:**
   - Ejecutar el asistente de SecurityRAT indicando capítulo del ASVS, nivel objetivo (L2 recomendado) y uso de SSO.
   - Para cada requisito generado, asociar etiquetas que vinculen el caso de uso correspondiente (por ejemplo, `UC-006` para obligaciones fiscales).
5. **Sincronizar con el ciclo de desarrollo:**
   - Configurar la integración con JIRA o la herramienta de seguimiento vigente para crear issues automáticamente.
   - Exportar los requisitos activos y adjuntar el reporte resultante al repositorio (`docs/security/` sugerido) durante cada liberación.

> Nota contextual importante: Para equipos que están comenzando con SecurityRAT, se recomienda usar primero la demostración en línea para familiarizarse con la herramienta antes de invertir tiempo en la instalación completa, que puede ser compleja.

### Iniciando sesión y creando requisitos

Inicie sesión en el sitio de demostración, usando las credenciales de la [página del proyecto](https://owasp.org/www-project-securityrat/), se le presentará la opción de definir un conjunto de requisitos o importar un conjunto existente. Asumiendo que queremos un nuevo conjunto de requisitos, asigne un nombre al artefacto de requisitos y luego seleccione secciones/capítulos específicos del ASVS de la lista:

- V1 - Arquitectura, Diseño y Modelado de Amenazas
- V2 - Autenticación
- V3 - Gestión de Sesiones
- V4 - Control de Acceso
- V5 - Validación, Sanitización y Codificación
- V6 - Criptografía Almacenada
- V7 - Manejo de Errores y Registro
- V8 - Protección de Datos
- V9 - Comunicación
- V10 - Código Malicioso
- V11 - Lógica de Negocio
- V12 - Archivos y Recursos
- V13 - API y Servicio Web
- V14 - Configuración

o deje en blanco para incluir todos los requisitos de verificación.

### Selección de nivel y generación

Seleccione el nivel usando los niveles de cumplimiento de seguridad definidos por ASVS:

- **Nivel 1** es para niveles de aseguramiento bajo y es completamente comprobable mediante pruebas de penetración
- **Nivel 2** es para aplicaciones que contienen datos sensibles y requieren protección; es el nivel recomendado para la mayoría de las aplicaciones
- **Nivel 3** es para las aplicaciones más críticas

Finalmente, seleccione si se está utilizando autenticación SSO y genere una lista de requisitos. Este artefacto de requisitos ahora está almacenado en SecurityRAT y puede recuperarse en sesiones posteriores.

### Gestión y seguimiento

SecurityRAT luego presenta una pantalla de administración que permite el seguimiento y edición de los requisitos de verificación del ASVS. Consulte el [OWASP Spotlight sobre SecurityRAT](https://youtu.be/ythaa6nRa0Y) para obtener una explicación de cómo integrar con Atlassian JIRA.

---

## ¿QUÉ ES SECURITYCAT?

[SecurityCAT](https://github.com/SecurityRAT/SecurityCAT) (Compliance Automation Tool - Herramienta de Automatización de Cumplimiento) es una extensión para SecurityRAT destinada a pruebas automáticas de requisitos. No hay una implementación real de SecurityCAT, SecurityRAT proporciona una API que permite crear una herramienta de cumplimiento, por lo que este puede ser un desarrollo futuro para SecurityRAT.

> Concepto Clave: SecurityCAT representa la visión de automatización completa del cumplimiento de requisitos, donde no solo se gestionan sino que también se verifican automáticamente. Aunque aún no está implementado, la API de SecurityRAT está diseñada para soportar este tipo de herramientas.

---

## REFERENCIAS

- OWASP [SecurityRAT](https://owasp.org/www-project-securityrat/)
- OWASP [documentación de SecurityRAT](https://securityrat.github.io/)
- OWASP [SecurityCAT](https://github.com/SecurityRAT/SecurityCAT)
- OWASP [Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) (ASVS)

---

> **📋 RECUADRO INFORMATIVO**
>
> **La Guía para Desarrolladores de OWASP es un esfuerzo comunitario**
> 
> Si hay algo que necesite cambiarse, [envíe un problema (issue)](https://github.com/OWASP/www-project-developer-guide/issues) o [edite en GitHub](https://github.com/OWASP/www-project-developer-guide/edit/main/draft/03-requirements/05-security-rat.md).

---

## Terminología Clave Aplicada

**Términos NO traducidos (preservados del original):**
- OWASP SecurityRAT
- ASVS (Application Security Verification Standard)
- JIRA
- Docker/DockerHub
- JDK (Java Development Kit)
- API
- SSO (Single Sign-On)
- SecurityCAT

**Términos traducidos con referencia:**
- Requirement Automation Tool → Herramienta de Automatización de Requisitos
- Compliance Automation Tool → Herramienta de Automatización de Cumplimiento

**Conceptos completamente traducidos:**
- Authentication → Autenticación
- Session Management → Gestión de Sesiones
- Access Control → Control de Acceso
- Error Handling → Manejo de Errores
- Business Logic → Lógica de Negocio

**Formato aplicado consistentemente:**
- Primera mención: "Application Security Verification Standard (Estándar de Verificación de Seguridad de Aplicaciones)"
- Menciones posteriores: "ASVS" o "el estándar"
