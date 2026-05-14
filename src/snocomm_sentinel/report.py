"""Report generation for Snocomm Sentinel."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from snocomm_sentinel.risk import build_risk_summary, sanitize_forensic_language


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def normalize_result_document(results: dict[str, Any]) -> dict[str, Any]:
    """Ensure risk summary and report metadata are present."""
    normalized = dict(results)
    findings = list(normalized.get("findings", []))
    normalized.setdefault("generated_at", now_iso())
    normalized.update(build_risk_summary(findings))
    return normalized


def load_results_json(path: str | Path) -> dict[str, Any]:
    with Path(path).expanduser().open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    if not isinstance(loaded, dict):
        raise ValueError("El archivo de resultados debe contener un objeto JSON.")
    return loaded


def write_json_report(results: dict[str, Any], path: str | Path) -> None:
    normalized = normalize_result_document(results)
    Path(path).expanduser().write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def severity_label(severity: str) -> str:
    labels = {
        "info": "informativo",
        "low": "bajo",
        "medium": "medio",
        "moderate": "medio",
        "high": "alto",
        "critical": "crítico",
    }
    return labels.get(str(severity).lower(), "informativo")


def generate_markdown_report(results: dict[str, Any]) -> str:
    """Create an executive Markdown report with conservative forensic language."""
    normalized = normalize_result_document(results)
    findings = normalized.get("findings", [])
    recommendations = normalized.get("recommendations", [])
    lines = [
        "# Reporte Snocomm Sentinel",
        "",
        f"- Herramienta: `{normalized.get('tool', 'snocomm-sentinel')}`",
        f"- Versión: `{normalized.get('version', 'desconocida')}`",
        f"- Plataforma: `{normalized.get('platform', 'desconocida')}`",
        f"- Perfil: `{normalized.get('profile', 'default')}`",
        f"- Riesgo general: **{normalized.get('risk', 'LOW')}**",
        f"- Fecha de generación: `{normalized.get('generated_at', now_iso())}`",
        "",
        "## Resumen ejecutivo",
        "",
        sanitize_forensic_language(
            "Este reporte resume hallazgos técnicos locales y recomendaciones de hardening. "
            "No constituye, por sí mismo, una atribución forense ni una confirmación de compromiso."
        ),
        "",
        "## Hallazgos",
        "",
    ]

    if not findings:
        lines.append("No se registraron hallazgos de riesgo con la configuración actual.")
    else:
        lines.extend(
            [
                "| ID | Severidad | Hallazgo | Recomendación |",
                "| --- | --- | --- | --- |",
            ]
        )
        for item in findings:
            title = sanitize_forensic_language(str(item.get("title", "Hallazgo sin título")))
            recommendation = sanitize_forensic_language(
                str(item.get("recommendation", "Revisar con el equipo responsable."))
            )
            lines.append(
                "| {id} | {severity} | {title} | {recommendation} |".format(
                    id=str(item.get("id", "UNKNOWN")).replace("|", "\\|"),
                    severity=severity_label(str(item.get("severity", "info"))),
                    title=title.replace("|", "\\|"),
                    recommendation=recommendation.replace("|", "\\|"),
                )
            )

    lines.extend(["", "## Recomendaciones", ""])
    if recommendations:
        for recommendation in recommendations:
            lines.append(f"- {sanitize_forensic_language(str(recommendation))}")
    else:
        lines.extend(
            [
                "- Mantener el sistema operativo y las aplicaciones críticas actualizadas.",
                "- Desactivar servicios remotos que no tengan justificación operativa.",
                "- Revisar perfiles de configuración, MDM y permisos administrativos con trazabilidad.",
                "- Escalar hallazgos críticos a especialistas forenses cuando exista sospecha fundada.",
            ]
        )

    lines.extend(
        [
            "",
            "## Nota forense",
            "",
            sanitize_forensic_language(
                "Snocomm Sentinel separa hallazgos técnicos de conclusiones forenses. "
                "Los resultados deben interpretarse como señales compatibles con exposición, mala configuración "
                "o necesidad de revisión, no como prueba automática de compromiso."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown_report(results: dict[str, Any], path: str | Path) -> None:
    Path(path).expanduser().write_text(generate_markdown_report(results), encoding="utf-8")
