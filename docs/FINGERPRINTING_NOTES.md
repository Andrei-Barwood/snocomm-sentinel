# Notas sobre fingerprinting

## Qué es fingerprinting

Fingerprinting es la correlación de atributos técnicos y contextuales para distinguir o perfilar un dispositivo, usuario o entorno. Un dato aislado rara vez basta. El riesgo aparece cuando múltiples señales se combinan: versión del sistema, build number, hostname, zona horaria, locale, modelo de hardware, navegador, extensiones, perfiles, servicios, rutas internas y patrones de uso.

## Qué es el build number

El build number identifica una compilación específica del sistema operativo. En macOS, iOS y iPadOS puede ayudar a saber con precisión qué versión ejecuta un dispositivo. Para soporte y seguridad defensiva es información útil; para privacidad, debe compartirse solo cuando sea necesario.

## Por qué puede ayudar a seleccionar exploits

Un adversario puede usar versión y build number para estimar si un dispositivo podría ser vulnerable a una familia de fallos conocida. Esto no significa que el build number cause infección ni que ocultarlo bloquee spyware. Significa que forma parte de un contexto que puede ayudar a priorizar objetivos.

## Por qué ocultarlo no es defensa suficiente

Ocultar el build number no reemplaza parches, hardening, reducción de servicios, revisión de perfiles ni análisis forense. Un atacante puede inferir versión por otros medios o explotar vectores que no dependen de esa señal. La minimización de fingerprinting es una capa, no una solución total.

## Cómo reducir exposición sin romper el sistema

- Mantenga sistema operativo y aplicaciones actualizadas.
- Reduzca servicios remotos y sharing innecesarios.
- Evite publicar capturas con build number, seriales, UUIDs o rutas internas.
- Revise reportes antes de enviarlos a proveedores externos.
- Separe perfiles personales y corporativos.
- Use navegadores con protecciones anti-fingerprinting cuando el riesgo lo amerite.
- Mantenga MDM transparente, auditable y limitado.
- Defina qué datos puede pedir soporte y bajo qué justificación.

## Checklist corporativo

- ¿Los tickets de soporte minimizan datos técnicos sensibles?
- ¿Las capturas se revisan antes de compartirse?
- ¿Los reportes ejecutivos omiten seriales y UUIDs salvo necesidad?
- ¿Los equipos sensibles tienen servicios remotos deshabilitados?
- ¿Los perfiles de configuración están inventariados?
- ¿La política MDM explica alcance y límites?
- ¿Existe flujo MVT documentado para casos críticos?
- ¿Se evalúa Lockdown Mode para personas de alto riesgo?

## Buenas prácticas para tickets y capturas

- Recorte datos que no sean necesarios.
- Evite mostrar rutas internas, nombres de usuario, dominios privados o identificadores únicos.
- Sustituya valores sensibles por marcadores descriptivos.
- Mantenga una versión completa solo cuando exista necesidad técnica y control de acceso.
- Indique en el ticket si un dato fue omitido deliberadamente por privacidad.

