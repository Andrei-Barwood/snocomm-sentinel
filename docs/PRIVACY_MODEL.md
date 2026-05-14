# Modelo de privacidad

## Principios

### Minimización de datos

Snocomm Sentinel debe recopilar solo la información necesaria para evaluar exposición local. Los reportes deben evitar seriales, UUIDs, rutas internas, nombres personales y datos sensibles salvo que sean estrictamente necesarios.

### Ejecución local

El toolkit está diseñado para ejecutarse localmente. No requiere subir backups, reportes ni resultados a servicios externos.

### No telemetría por defecto

La herramienta no envía telemetría por defecto. Cualquier funcionalidad futura que implique red deberá ser explícita, documentada, desactivada por defecto y revisable por la comunidad.

### No subida de backups

Los backups de iOS o iPadOS pueden contener datos extremadamente sensibles. No deben subirse a proveedores externos ni compartirse sin autorización formal.

### Consentimiento explícito

Toda revisión debe contar con autorización del dueño del dispositivo o con un proceso corporativo legítimo, documentado y consentido.

### Outputs auditables

Los resultados JSON y Markdown deben ser legibles, versionables y auditables. La organización debe poder explicar qué se recolectó, por qué y con qué límite.

### Reportes redactados con cuidado

Los reportes no deben usar lenguaje alarmista ni afirmar infección sin evidencia forense. Deben distinguir exposición, mala configuración, coincidencias importadas y conclusiones especializadas.

### Separación entre hallazgo técnico y conclusión forense

Un servicio remoto activo, un perfil desconocido o una coincidencia de nombre no son una conclusión forense. Son señales que pueden requerir revisión, hardening o escalamiento.

## Datos tratados

- Versión del sistema operativo y build number.
- Hostname, zona horaria, locale y modelo de hardware cuando estén disponibles.
- Estado de servicios remotos y sharing en macOS.
- Metadata básica de perfiles de configuración.
- Señales generales de posible enrolamiento MDM.
- Nombres de LaunchAgents y LaunchDaemons que requieren revisión.
- Rutas locales con nombres compatibles con herramientas públicas sospechosas.
- Resultados JSON de MVT solo cuando el usuario los entrega explícitamente.

## Datos que no deben recopilarse por defecto

- Contenido de mensajes, correos o documentos personales.
- Credenciales, tokens, cookies o llaveros.
- Historial de shell, salvo activación explícita con consentimiento.
- Backups completos para subida o procesamiento remoto.
- Información de terceros no autorizados.

## Retención

Cada organización debe definir retención de reportes, evidencia y backups según su marco legal. Como criterio general, retenga lo mínimo necesario, limite acceso y elimine material sensible cuando termine su finalidad legítima.

