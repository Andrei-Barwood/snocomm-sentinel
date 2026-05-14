"""Bridge for user-supplied MVT results."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from snocomm_sentinel.checks.ios_backup import parse_mvt_json


def normalize_mvt_match(match: dict[str, Any], index: int) -> dict[str, Any]:
    """Normalize a user-supplied MVT match for corporate reporting."""
    indicator = str(match.get("indicator", "mvt_record"))
    return {
        "index": index,
        "indicator": indicator,
        "raw_type": str(match.get("raw_type", "unknown")),
        "source_file": str(match.get("source_file", "")),
        "interpretation": (
            "Coincidencia importada desde MVT. Requiere revisión con contexto, "
            "cadena de custodia y criterio forense."
        ),
    }


def build_mvt_import_document(path: str | Path) -> dict[str, Any]:
    """Build a stable import document for CLI output and future integrations."""
    parsed = parse_mvt_json(path)
    normalized_matches = [
        normalize_mvt_match(match, index)
        for index, match in enumerate(parsed.get("matches", []), start=1)
        if isinstance(match, dict)
    ]
    return {
        "tool": "snocomm-sentinel",
        "integration": "mvt-json-import",
        "source": parsed["source"],
        "record_count": parsed["record_count"],
        "matched_count": parsed["matched_count"],
        "matches": normalized_matches,
        "forensic_caution": (
            "Este resumen no confirma compromiso. Los resultados importados desde MVT "
            "deben interpretarse con cuidado y escalarse a especialistas en casos críticos."
        ),
    }


def import_mvt_results(path: str | Path) -> dict[str, Any]:
    document = build_mvt_import_document(path)
    findings = []
    if document["matched_count"]:
        findings.append(
            {
                "id": "MVT_IMPORTED_MATCHES_PRESENT",
                "severity": "critical",
                "title": "Resultados importados de MVT contienen coincidencias",
                "explanation": (
                    "El archivo JSON entregado por el usuario contiene coincidencias de alto nivel. "
                    "Esto requiere revisión cuidadosa y no debe traducirse automáticamente en una "
                    "conclusión forense sobre spyware mercenario."
                ),
                "recommendation": (
                    "Preservar evidencia, documentar cadena de custodia y escalar a especialistas forenses "
                    "si el contexto es crítico."
                ),
                "source": "mvt",
                "evidence": {
                    "source": document["source"],
                    "matched_count": document["matched_count"],
                },
            }
        )
    return {"summary": document, "findings": findings}


def generate_mvt_markdown_summary(document: dict[str, Any]) -> str:
    """Generate a concise Markdown summary for imported MVT JSON."""
    lines = [
        "# Resumen de importación MVT",
        "",
        f"- Integración: `{document.get('integration', 'mvt-json-import')}`",
        f"- Fuente: `{document.get('source', '')}`",
        f"- Registros procesados: `{document.get('record_count', 0)}`",
        f"- Coincidencias de alto nivel: `{document.get('matched_count', 0)}`",
        "",
        "## Cautela forense",
        "",
        str(
            document.get(
                "forensic_caution",
                "Los resultados deben interpretarse con cuidado y no equivalen a una conclusión forense automática.",
            )
        ),
        "",
        "## Coincidencias",
        "",
    ]
    matches = document.get("matches", [])
    if not matches:
        lines.append("No se observaron coincidencias de alto nivel en el JSON importado.")
    else:
        lines.extend(["| Índice | Indicador | Tipo | Interpretación |", "| --- | --- | --- | --- |"])
        for match in matches:
            lines.append(
                "| {index} | {indicator} | {raw_type} | {interpretation} |".format(
                    index=match.get("index", ""),
                    indicator=str(match.get("indicator", "")).replace("|", "\\|"),
                    raw_type=str(match.get("raw_type", "")).replace("|", "\\|"),
                    interpretation=str(match.get("interpretation", "")).replace("|", "\\|"),
                )
            )
    lines.append("")
    return "\n".join(lines)
