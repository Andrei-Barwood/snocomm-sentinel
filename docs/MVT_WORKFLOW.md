# Flujo defensivo con MVT de Amnesty International

## Qué es MVT

Mobile Verification Toolkit, conocido como MVT, es una herramienta open source reconocida para análisis forense consensual de dispositivos iOS y Android frente a indicadores asociados a spyware mercenario.

Snocomm Sentinel no reemplaza MVT. Su función es complementar el flujo corporativo: preparar documentación, ordenar consentimiento, registrar contexto, importar resultados JSON entregados por el usuario y generar reportes ejecutivos conservadores.

## Para qué sirve

MVT puede ayudar a revisar backups o artefactos móviles en busca de indicadores conocidos. Su uso debe entenderse como parte de un proceso forense, no como una garantía de detección total.

## Cuándo usarlo

- Sospecha fundada de spyware mercenario.
- Notificación de amenaza de una fuente confiable.
- Revisión autorizada de una persona con riesgo elevado.
- Preparación de respuesta corporativa ante incidente sensible.
- Solicitud de especialistas forenses dentro de un proceso documentado.

## Límites

- MVT no garantiza detección de todas las amenazas.
- Los indicadores pueden cambiar, caducar o requerir interpretación experta.
- Una coincidencia debe evaluarse con contexto, cadena de custodia y alcance.
- La ausencia de hallazgos no prueba ausencia de compromiso.
- Snocomm Sentinel no debe afirmar infección por Pegasus sin evidencia verificable.

## Cómo preparar un backup

1. Documente autorización del dueño del dispositivo o del proceso corporativo legítimo.
2. Defina alcance, responsables, herramientas, fecha y lugar de análisis.
3. Prepare el entorno de análisis en un equipo controlado.
4. Genere el backup según la documentación oficial de MVT y las políticas de la organización.
5. Proteja el backup como dato altamente sensible.
6. Registre quién accede al material y por qué.

Snocomm Sentinel no accede directamente al iPhone, no rompe sandbox y no intenta extraer datos sin autorización. Puede verificar si un directorio entregado por el usuario parece tener estructura de backup, pero no sustituye el proceso MVT.

## Cómo interpretar resultados

Interprete resultados con cuidado:

- “Coincidencia” no significa automáticamente compromiso.
- “Sin coincidencias” no significa seguridad absoluta.
- Revise fuente del indicador, fecha, contexto y artefacto.
- Mantenga una separación clara entre señal técnica, hipótesis y conclusión forense.
- En reportes ejecutivos use lenguaje como “compatible con”, “requiere revisión” o “no concluyente”.

## Importación en Snocomm Sentinel

La versión inicial puede leer resultados JSON entregados por el usuario y resumir coincidencias de alto nivel mediante `mvt-import` o `scan --mvt-results`. La integración preserva el mismo principio: no inventar infección, no exagerar conclusiones y escalar cuando sea necesario.

Ejemplo de uso previsto:

```bash
snocomm-sentinel mvt-import --input mvt-results.json --format md
snocomm-sentinel scan --mvt-results mvt-results.json --profile high-risk
snocomm-sentinel report --input sentinel-output/results.json --format md
```

## Cuándo escalar a especialistas

Escalamiento recomendado cuando exista:

- notificación de amenaza de Apple u otra fuente confiable;
- coincidencias MVT relevantes;
- riesgo físico, legal, periodístico o político;
- posible afectación a personas vulnerables;
- evidencia que requiere cadena de custodia;
- necesidad de comunicación pública o notificación regulatoria.

## Documentar consentimiento

Un registro mínimo debería incluir:

- persona dueña o responsable del dispositivo;
- fundamento de autorización;
- alcance del análisis;
- herramientas utilizadas;
- fecha y responsables;
- tratamiento de backups;
- retención y eliminación;
- límites del reporte;
- punto de contacto para preguntas.
