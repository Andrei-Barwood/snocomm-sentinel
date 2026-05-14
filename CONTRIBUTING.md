# Guía de contribución

Gracias por contribuir a Snocomm Sentinel. Este proyecto acepta mejoras defensivas, documentación, pruebas, reportes de errores y propuestas de integración que respeten privacidad, consentimiento y proporcionalidad.

## Principios de contribución

- Mantenga el proyecto estrictamente defensivo.
- No incluya exploits, payloads, shells ofensivas, persistencia, evasión, robo de credenciales ni instrucciones de intrusión.
- No agregue infraestructura real de atacantes ni indicadores que faciliten ataque.
- Use lenguaje conservador: “compatible con”, “requiere revisión”, “no concluyente”, “hallazgo de riesgo”.
- Separe hallazgos técnicos de conclusiones forenses.
- Priorice ejecución local, minimización de datos y reportes auditables.

## Preparación del entorno

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
```

## Flujo recomendado

1. Abra un issue o describa el cambio en el pull request.
2. Mantenga el cambio acotado.
3. Agregue pruebas cuando modifique scoring, parser, CLI o generación de reportes.
4. Revise documentación y tono editorial en español.
5. Ejecute `ruff check .` y `pytest` antes de enviar.

## Estilo de código

- Python 3.11 o superior.
- Funciones pequeñas y testeables.
- `subprocess.run` sin `shell=True`, con timeout y manejo de errores.
- Sin elevación automática de privilegios.
- Sin escritura en rutas del sistema.
- Sin modificación de configuración crítica por defecto.
- Comentarios breves solo cuando aclaren decisiones no obvias.

## Estilo editorial

La documentación principal está en español formal, claro y corporativo. Evite traducciones literales, anglicismos innecesarios y promesas exageradas. Antes de proponer cambios al README o a `docs/`, revise tildes, puntuación, concordancia, precisión técnica y tono.

## Cambios no aceptados

No se aceptarán contribuciones que:

- automaticen intrusión o escaneo no autorizado;
- permitan evadir controles de seguridad;
- prometan detección absoluta de spyware;
- manipulen el sistema operativo de forma riesgosa;
- recopilen datos sensibles sin consentimiento explícito;
- suban backups, reportes o telemetría a servicios externos por defecto.

## Seguridad y privacidad

No abra issues públicos con credenciales, backups, datos personales, resultados forenses sensibles o evidencia de incidentes activos. Use el proceso descrito en [SECURITY.md](SECURITY.md).

