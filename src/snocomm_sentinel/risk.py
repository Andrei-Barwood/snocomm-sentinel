"""Conservative risk scoring for defensive exposure findings."""

from __future__ import annotations

from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


SEVERITY_WEIGHTS = {
    "info": 0,
    "low": 1,
    "medium": 3,
    "moderate": 3,
    "high": 6,
    "critical": 10,
}

FORENSIC_SOURCE_KEYS = {"mvt", "mobile_verification_toolkit", "forensic"}
FORBIDDEN_ABSOLUTE_PHRASES = (
    "infectado con " + "pegasus",
    "infected with " + "pegasus",
    "pegasus " + "confirmado",
    "confirmed " + "pegasus infection",
    "eliminaci" + "ón total",
    "inmunidad contra " + "pegasus",
    "anti-" + "pegasus definitivo",
)


def normalize_severity(severity: str | None) -> str:
    """Return a known severity label without raising on unknown input."""
    if not severity:
        return "info"
    lowered = severity.strip().lower()
    return lowered if lowered in SEVERITY_WEIGHTS else "info"


def finding_weight(finding: dict[str, Any]) -> int:
    """Map a finding to a conservative numeric weight."""
    return SEVERITY_WEIGHTS[normalize_severity(str(finding.get("severity", "info")))]


def score_findings(findings: list[dict[str, Any]]) -> RiskLevel:
    """Calculate a conservative overall risk level.

    The model intentionally separates technical exposure from forensic conclusions.
    A critical score requires either multiple strong technical findings or an explicit
    forensic source supplied by the user, such as imported MVT results.
    """
    if not findings:
        return RiskLevel.LOW

    total = sum(finding_weight(item) for item in findings)
    high_or_above = [
        item
        for item in findings
        if normalize_severity(str(item.get("severity", "info"))) in {"high", "critical"}
    ]
    forensic_critical = any(
        normalize_severity(str(item.get("severity", ""))) == "critical"
        and str(item.get("source", "")).lower() in FORENSIC_SOURCE_KEYS
        for item in findings
    )

    if forensic_critical or total >= 16 or len(high_or_above) >= 3:
        return RiskLevel.CRITICAL
    if total >= 6 or high_or_above:
        return RiskLevel.HIGH
    if total >= 2:
        return RiskLevel.MODERATE
    return RiskLevel.LOW


def sanitize_forensic_language(text: str) -> str:
    """Remove absolute claims that are inappropriate without verified evidence."""
    sanitized = text
    replacements = {
        "infectado con " + "Pegasus": "con hallazgos compatibles que requieren revisión",
        "Infectado con " + "Pegasus": "Hallazgos compatibles que requieren revisión",
        "infected with " + "Pegasus": "findings compatible with risk that require review",
        "Pegasus " + "confirmado": "hallazgo no concluyente que requiere revisión forense",
        "confirmed " + "Pegasus infection": "non-conclusive finding requiring forensic review",
        "eliminaci" + "ón total": "reducción de exposición",
        "inmunidad contra " + "Pegasus": "mejora de postura defensiva",
        "anti-" + "Pegasus definitivo": "flujo defensivo complementario",
    }
    for unsafe, safe in replacements.items():
        sanitized = sanitized.replace(unsafe, safe)
    return sanitized


def contains_forbidden_absolute_claim(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in FORBIDDEN_ABSOLUTE_PHRASES)


def build_risk_summary(findings: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a serializable risk summary for reports and CLI output."""
    risk = score_findings(findings)
    return {
        "risk": risk.value,
        "finding_count": len(findings),
        "high_or_critical_count": sum(
            1
            for item in findings
            if normalize_severity(str(item.get("severity", ""))) in {"high", "critical"}
        ),
        "forensic_caution": (
            "Los hallazgos técnicos no equivalen por sí solos a una conclusión forense. "
            "Use expresiones como compatible con, requiere revisión o no concluyente."
        ),
    }
