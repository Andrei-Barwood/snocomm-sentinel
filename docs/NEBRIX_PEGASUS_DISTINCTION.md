# Distinción entre NSO Pegasus y Nebrix/Pegasus

## Pegasus de NSO Group

Pegasus de NSO Group es spyware mercenario móvil de alta sofisticación, asociado a vigilancia avanzada. Su análisis requiere procedimientos forenses especializados, interpretación cuidadosa y evidencia verificable.

Snocomm Sentinel no afirma detectar, eliminar ni neutralizar Pegasus de NSO Group. Su aporte es defensivo: evaluar exposición, ordenar evidencia, recomendar hardening y preparar flujos con herramientas reconocidas como MVT.

## Nebrix/Pegasus

Nebrix/Pegasus se entiende aquí como una herramienta pública o repositorio de terceros con nombre similar. El nombre puede generar confusión, pero no debe asociarse automáticamente con Pegasus de NSO Group.

En entornos corporativos, la presencia local de una shell ofensiva, repositorio sospechoso o herramienta pública llamada “Pegasus” puede ser un hallazgo relevante. Sin embargo, el hallazgo debe redactarse con precisión: “presencia de herramienta pública con nombre compatible”, no “compromiso por spyware mercenario”.

## Riesgos de herramientas llamadas “Pegasus”

- Ejecución de código no auditado en equipos institucionales.
- Introducción de dependencias inseguras.
- Confusión en reportes ejecutivos.
- Riesgo reputacional por manejo impreciso del lenguaje.
- Posible violación de políticas internas sobre herramientas ofensivas.
- Exposición accidental de credenciales, llaves o datos locales.

## Por qué no se deben ejecutar shells ofensivas

Las shells ofensivas, incluso si son públicas, pueden contener payloads, persistencia, robo de datos o código engañoso. Ejecutarlas en equipos institucionales puede comprometer evidencia, privacidad y cumplimiento. La revisión inicial debe limitarse a nombres, rutas, metadata y procedencia, sin ejecutar contenido.

## Cómo detectar clones locales sin ejecutar nada

Snocomm Sentinel busca nombres de rutas y archivos compatibles con herramientas públicas sospechosas. La detección se realiza en modo lectura y sin interacción con infraestructura externa.

Ejemplos de señales defensivas:

- directorios con nombres como `nebrix`, `nebrix-pegasus` o `pegasus-shell`;
- archivos como `pegasus.py` o `pegasus.sh`;
- LaunchAgents o LaunchDaemons con nombres que ameritan revisión;
- referencias en historial de shell solo cuando se activa el flag explícito y con consentimiento.

Estas señales son indicios de revisión, no conclusiones forenses.

## Política recomendada

- Prohibir ejecución de herramientas ofensivas no aprobadas en equipos corporativos.
- Definir laboratorio aislado para investigación autorizada.
- Mantener inventario de herramientas de seguridad permitidas.
- Exigir revisión de origen, licencia, propósito y responsable.
- Separar investigación defensiva de equipos productivos.
- Documentar hallazgos con lenguaje conservador.

## Redacción correcta de hallazgos

Redacción recomendada:

- “Se observó una ruta local compatible con una herramienta pública llamada Pegasus.”
- “El hallazgo no equivale a compromiso por Pegasus de NSO Group.”
- “Se recomienda revisar procedencia, autorización y necesidad.”
- “No ejecutar el contenido hasta completar revisión.”

Redacción a evitar:

- “Equipo infectado por Pegasus.”
- “Confirmación de Pegasus sin evidencia forense verificable.”
- “Se eliminó Pegasus.”
- “Bypass de vigilancia.”
