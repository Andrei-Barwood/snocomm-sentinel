# Modelo de amenazas

## Alcance

Este modelo describe amenazas defensivas relevantes para privacidad corporativa, exposición del sistema y preparación frente a spyware mercenario. No contiene instrucciones ofensivas, explotación de vulnerabilidades ni interacción con infraestructura de atacantes.

## Activos protegidos

- Dispositivos macOS, iOS y iPadOS de usuarios autorizados.
- Backups entregados voluntariamente para análisis.
- Reportes técnicos y ejecutivos.
- Evidencia local y metadata de configuración.
- Privacidad de directivos, equipos legales, investigadores y personal sensible.
- Reputación corporativa y confianza interna.

## Amenazas principales

### Spyware mercenario

Pegasus de NSO Group y amenazas similares representan un nivel de sofisticación que excede una auditoría local básica. Snocomm Sentinel no afirma detectar ni eliminar estas amenazas. Su contribución es preparar flujos, reducir exposición y ordenar evidencia para escalamiento.

### MDM abusivo

Un MDM puede ser legítimo y necesario, pero también puede volverse invasivo si no existe transparencia, consentimiento corporativo, documentación de políticas y control de permisos.

### Soporte técnico invasivo

Herramientas de soporte remoto mal gobernadas pueden exponer pantallas, archivos, logs o credenciales. La amenaza incluye exceso de privilegios, sesiones no documentadas y recopilación innecesaria de datos.

### Herramientas públicas tipo hacking shell

Repositorios llamados “Pegasus”, “Nebrix/Pegasus” u otros nombres similares pueden introducir riesgo operativo si se clonan o ejecutan en equipos institucionales. La presencia local de esos nombres no equivale a compromiso por spyware mercenario.

### Exfiltración vía backups

Backups móviles pueden contener datos sensibles. Subirlos a servicios externos o compartirlos sin consentimiento crea riesgo legal, reputacional y personal.

### Ingeniería social

Usuarios sensibles pueden recibir enlaces, documentos, mensajes o solicitudes de soporte diseñadas para inducir acciones riesgosas. El hardening técnico debe acompañarse de preparación humana.

### Fingerprinting

Build number, versión del sistema, hostname, zona horaria, locale, navegador, extensiones y servicios visibles pueden facilitar correlación, priorización de exploits o perfilamiento operacional.

### Dispositivos desactualizados

Sistemas sin parches aumentan exposición a vulnerabilidades conocidas. Mantener actualización es una medida más importante que ocultar un dato aislado del fingerprint.

### Perfiles de configuración maliciosos

Perfiles no autorizados pueden alterar confianza, certificados, VPN, proxies, restricciones o enrolamiento. Deben revisarse con cuidado y sin borrar evidencia de manera impulsiva.

### Publicación accidental de datos técnicos internos

Capturas de pantalla, tickets y reportes pueden revelar build number, seriales, UUIDs, rutas internas, nombres de usuario, dominios, proveedores y configuraciones.

### Abuso de herramientas administrativas

Herramientas legítimas pueden usarse de forma desproporcionada. La mitigación requiere políticas, auditoría, control de acceso y trazabilidad.

## Supuestos

- El análisis se realiza sobre equipos propios o autorizados.
- No hay explotación activa ni interacción con terceros.
- Los hallazgos técnicos se interpretan como señales de riesgo, no como conclusiones forenses automáticas.
- Los casos críticos se escalan a especialistas.

## Controles defensivos

- Actualización de sistema y aplicaciones.
- FileVault, firewall, Gatekeeper y SIP correctamente configurados.
- MDM documentado y transparente.
- Revisión de perfiles de configuración.
- Reducción de servicios remotos.
- Lockdown Mode para perfiles de alto riesgo.
- Uso consensual de MVT en dispositivos móviles.
- Reportes con minimización de datos.
- Separación entre evidencia técnica y conclusiones ejecutivas.
