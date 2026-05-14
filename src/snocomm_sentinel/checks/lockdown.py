"""Lockdown Mode guidance without pretending to verify every platform state."""

from __future__ import annotations


def lockdown_recommendations(profile: str) -> list[str]:
    base = [
        "Evaluar Lockdown Mode para usuarios con exposición elevada, después de explicar impacto funcional.",
        "Documentar quién aprueba la activación, qué aplicaciones pueden verse afectadas y cómo revertir la decisión.",
    ]
    if profile == "high-risk":
        base.insert(
            0,
            "Para perfiles de alto riesgo, Lockdown Mode debe considerarse una medida defensiva prioritaria.",
        )
    return base


def lockdown_finding(profile: str) -> dict[str, object] | None:
    if profile != "high-risk":
        return None
    return {
        "id": "LOCKDOWN_MODE_RECOMMENDED_FOR_HIGH_RISK_PROFILE",
        "severity": "medium",
        "title": "Lockdown Mode recomendado para perfil de riesgo elevado",
        "explanation": (
            "El perfil seleccionado corresponde a usuarios con mayor exposición potencial. "
            "Snocomm Sentinel no verifica de forma concluyente el estado de Lockdown Mode en todos los casos."
        ),
        "recommendation": (
            "Evaluar activación de Lockdown Mode con el usuario, TI y responsables legales, "
            "documentando consentimiento e impacto operativo."
        ),
        "source": "policy",
    }

