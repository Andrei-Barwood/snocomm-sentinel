# Snocomm Sentinel: mirada corporativa

## Resumen ejecutivo

Snocomm Sentinel es un toolkit open source defensivo para privacidad corporativa, auditoría de exposición del sistema, reducción de fingerprinting y preparación frente a riesgo de spyware mercenario. Su valor está en convertir señales locales dispersas en reportes claros, recomendaciones proporcionales y procesos que puedan ser entendidos por TI, seguridad, dirección y área legal.

El proyecto no promete eliminar spyware mercenario ni reemplaza análisis forense profesional. Su enfoque es ordenar evidencia, reducir superficie de ataque y mejorar la toma de decisiones.

## Dolor del cliente

Las organizaciones suelen enfrentar preguntas difíciles con información incompleta:

- ¿Qué tan expuesto está el equipo de una persona sensible?
- ¿Existen servicios remotos activos que no deberían estar disponibles?
- ¿Hay perfiles de configuración o MDM que no están suficientemente documentados?
- ¿Se comparten capturas, reportes o tickets con build number, seriales o rutas internas?
- ¿Cómo se prepara un análisis con MVT sin improvisar?
- ¿Cómo se informa a dirección sin alarmismo ni lenguaje forense inapropiado?

Snocomm Sentinel entrega un marco inicial para responder estas preguntas con evidencia local, lenguaje conservador y recomendaciones accionables.

## Riesgo reputacional de spyware corporativo

El riesgo no se limita a una infección técnica. Una organización también puede sufrir daño reputacional por:

- uso invasivo de herramientas administrativas;
- falta de consentimiento en revisiones de dispositivos;
- ejecución de herramientas ofensivas en equipos institucionales;
- manejo deficiente de evidencia;
- comunicaciones imprecisas sobre Pegasus u otras amenazas;
- filtración de datos técnicos internos en tickets o proveedores;
- confusión entre spyware mercenario y repositorios públicos con nombres similares.

Una respuesta madura protege a la organización y a las personas. Eso exige trazabilidad, proporcionalidad y control del lenguaje.

## Por qué el build number importa como parte del fingerprint

El build number ayuda a describir con precisión el estado del sistema operativo. En soporte técnico y seguridad defensiva es útil para saber si un equipo está actualizado, qué rama de sistema ejecuta y qué compatibilidades pueden aplicar.

También puede formar parte del fingerprint: junto con hostname, modelo, zona horaria, locale, navegador, perfiles, servicios y capturas de pantalla, permite correlacionar un equipo con mayor precisión. Por eso conviene minimizar su exposición cuando no sea necesario, especialmente en tickets externos, capturas públicas o reportes compartidos con proveedores.

## Por qué ocultar el build number no basta

Ocultar o recortar el build number en una captura no bloquea spyware mercenario, no neutraliza exploits y no sustituye actualizaciones. El build number es una señal dentro de un conjunto más amplio. La defensa requiere reducir superficie de ataque, aplicar parches, revisar servicios, controlar perfiles, proteger backups y elevar controles para usuarios sensibles.

Snocomm Sentinel trata el build number como contexto de fingerprint, no como causa única de infección ni como palanca mágica de protección.

## Defensa combinada

Una defensa corporativa razonable combina:

- actualización permanente de sistema operativo y aplicaciones;
- hardening de servicios remotos, firewall, FileVault, Gatekeeper y SIP;
- evaluación de Lockdown Mode para usuarios de alto riesgo;
- análisis forense consensual cuando hay sospecha fundada;
- uso de MVT de Amnesty International para flujos móviles compatibles;
- gobernanza de MDM transparente y auditable;
- políticas de minimización de datos en reportes y soporte;
- documentación de consentimiento, alcance y cadena de custodia.

## Modelo de servicio

1. **Community Edition:** toolkit open source para auditoría local, reportes básicos, documentación y recomendaciones defensivas.
2. **Corporate Assessment:** revisión puntual de exposición, perfiles, MDM, servicios remotos, fingerprinting y reportes ejecutivos.
3. **Incident Readiness:** preparación de flujos ante sospecha de spyware, documentación de consentimiento, checklist MVT y escalamiento forense.
4. **Executive Privacy Program:** programa continuo para directivos, equipos legales, comunicaciones, periodistas internos o personas con exposición elevada.

## Entregables

- Reporte técnico con hallazgos, evidencia local y recomendaciones.
- Reporte ejecutivo para dirección o gerencia.
- Matriz de riesgo con severidad, impacto, probabilidad y responsable.
- Recomendaciones priorizadas de hardening y minimización de exposición.
- Plan de 30 días con acciones técnicas, políticas y documentales.

Las plantillas base están disponibles en `templates/corporate/` para facilitar uso recurrente por equipos TI, dirección y área legal.

## Plan de 30 días sugerido

- Días 1 a 5: inventario de perfiles, MDM, servicios remotos y exposición de soporte.
- Días 6 a 10: revisión de equipos sensibles y generación de reportes ejecutivos.
- Días 11 a 15: hardening de servicios, actualización y políticas de mínimos datos.
- Días 16 a 20: preparación de flujos MVT y documentación de consentimiento.
- Días 21 a 30: capacitación, revisión legal, playbooks y métricas de continuidad.
