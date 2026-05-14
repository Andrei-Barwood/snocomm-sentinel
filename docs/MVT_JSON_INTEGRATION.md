# Integración JSON de MVT

## Objetivo

La integración JSON de MVT permite que Snocomm Sentinel lea resultados entregados por el usuario, normalice coincidencias de alto nivel y genere resúmenes corporativos conservadores. No ejecuta MVT, no reemplaza MVT y no convierte una coincidencia en conclusión forense automática.

## Comandos

```bash
snocomm-sentinel mvt-import --input mvt-results.json --format json
snocomm-sentinel mvt-import --input mvt-results.json --format md
snocomm-sentinel scan --profile high-risk --mvt-results mvt-results.json
```

## Formas JSON soportadas

La versión inicial acepta estructuras comunes con listas en claves como:

- `results`
- `findings`
- `detections`
- `matches`
- `iocs`
- `indicators`
- `records`

También acepta una lista raíz de objetos. Si recibe un objeto único, lo trata como un registro.

## Campos normalizados

Cada coincidencia de alto nivel se normaliza con:

- `index`: posición del registro normalizado.
- `indicator`: indicador o descripción mínima.
- `raw_type`: tipo original si está disponible.
- `source_file`: archivo JSON importado.
- `interpretation`: explicación conservadora para reporte corporativo.

## Criterio de coincidencia

Un registro se considera coincidencia cuando:

- `matched`, `match` o `detected` son verdaderos;
- `matches` contiene elementos;
- `status` indica `match`, `matched`, `detected` o `positive`;
- existe `indicator` o `ioc` y no hay campo explícito que indique resultado negativo.

Este criterio favorece compatibilidad inicial, no certeza forense. Los equipos que usen MVT en incidentes críticos deben conservar el JSON original y escalar resultados relevantes a especialistas.

## Salida

El comando dedicado genera:

- resumen JSON auditable;
- resumen Markdown ejecutivo;
- cautela forense explícita;
- conteo de registros y coincidencias.

## Límites

- No valida autenticidad del archivo JSON.
- No verifica cadena de custodia.
- No descarga indicadores.
- No ejecuta análisis móvil.
- No afirma compromiso.
- No sustituye interpretación forense profesional.

## Roadmap técnico

- Validación opcional contra esquemas de salida conocidos de MVT.
- Importación de metadatos de ejecución cuando estén disponibles.
- Redacción automática de campos sensibles.
- Vinculación con plantillas corporativas.
- Pruebas con corpus sintético de resultados MVT no sensibles.

