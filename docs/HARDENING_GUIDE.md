# Guía de hardening defensivo

## Enfoque

Esta guía propone medidas defensivas, reversibles y proporcionales. No recomienda manipulación agresiva del sistema, parches no soportados ni cambios que puedan destruir evidencia. Antes de aplicar cambios, documente autorización, impacto y plan de reversión.

## macOS

- Mantenga macOS actualizado.
- Use FileVault con recuperación de claves documentada.
- Mantenga Gatekeeper y SIP activados salvo excepción temporal y aprobada.
- Active el firewall cuando sea compatible con la operación.
- Desactive Remote Login, Screen Sharing y servicios de sharing que no sean necesarios.
- Revise LaunchAgents y LaunchDaemons sospechosos sin borrarlos impulsivamente.
- Revise perfiles de configuración y MDM con inventario, propietario y propósito.
- Evite compartir capturas con build number, seriales, UUIDs o rutas internas cuando no sea necesario.

## iOS/iPadOS

- Mantenga el dispositivo actualizado.
- Use código fuerte, biometría y bloqueo automático.
- Revise perfiles de configuración desconocidos.
- Evite instalar perfiles, certificados o VPN sin validación corporativa.
- Controle backups y cifrado cuando corresponda.
- Para sospechas fundadas, prepare un flujo MVT consensual con documentación.

## Lockdown Mode

Lockdown Mode puede reducir superficie de ataque en usuarios con riesgo elevado, como periodistas, directivos, defensores de derechos humanos, investigadores o equipos legales. Debe evaluarse con consentimiento, explicación de impacto funcional y plan de soporte.

No todos los usuarios necesitan Lockdown Mode. La decisión debe considerar exposición, rol, amenazas probables, productividad y capacidad de soporte.

## Perfiles de configuración

- Mantenga inventario de perfiles instalados.
- Documente origen, propósito, fecha de aprobación y responsable.
- Revise certificados, proxies, VPN, restricciones y permisos.
- No elimine perfiles durante una investigación sin preservar evidencia y entender impacto.

## MDM

- Use MDM corporativo transparente y auditable.
- Publique políticas internas sobre qué puede administrar el MDM y qué no.
- Limite privilegios a necesidades reales.
- Registre cambios de política y excepciones.
- Revise que el MDM no se convierta en vigilancia abusiva.

## Backups

- Trate backups móviles como datos altamente sensibles.
- No suba backups a servicios externos sin autorización.
- Cifre backups cuando el flujo lo requiera.
- Controle acceso, retención y eliminación.
- Documente cadena de custodia en incidentes.

## Navegador

- Mantenga navegador y extensiones actualizados.
- Reduzca extensiones innecesarias.
- Use perfiles separados para trabajo sensible.
- Evalúe protecciones anti-fingerprinting cuando el riesgo lo amerite.
- No instale certificados raíz o proxies sin validación.

## Mensajería

- Use aplicaciones actualizadas.
- Active verificaciones de seguridad disponibles.
- Evite abrir enlaces o archivos inesperados en perfiles de alto riesgo.
- Defina canales de verificación fuera de banda para solicitudes sensibles.

## Separación entre vida personal y corporativa

- Separe cuentas, navegadores y dispositivos cuando sea viable.
- Evite mezclar backups personales y corporativos.
- Defina políticas claras para soporte técnico sobre equipos personales.
- Minimice exposición de datos personales en reportes corporativos.

## Respuesta ante notificaciones de amenaza

Si una persona recibe una notificación de amenaza de Apple u otra fuente confiable:

- No reinicie, borre ni actualice impulsivamente si se requiere preservación forense.
- Documente fecha, hora, contenido y contexto.
- Escale a seguridad, legal y especialistas forenses.
- Evalúe MVT u otros flujos reconocidos con consentimiento.
- Prepare comunicaciones internas sobrias y protegidas.

## Política de actualizaciones

- Defina ventanas de actualización y excepciones.
- Priorice parches de seguridad críticos.
- Mida equipos desactualizados.
- Mantenga comunicación clara con usuarios sensibles.
- Registre bloqueos operativos que impidan actualizar.

