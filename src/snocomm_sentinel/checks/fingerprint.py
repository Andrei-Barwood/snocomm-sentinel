"""Local fingerprint exposure collection and recommendations."""

from __future__ import annotations

import locale
import platform
import socket
import subprocess
import time
from typing import Any


def _run(command: list[str], timeout: int = 5) -> str | None:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (completed.stdout or completed.stderr or "").strip()
    return output or None


def _macos_sharing_services() -> list[str]:
    if platform.system() != "Darwin":
        return []
    output = _run(["/usr/sbin/sharing", "-l"], timeout=6)
    if not output:
        return []
    services: list[str] = []
    for line in output.splitlines():
        cleaned = line.strip()
        if cleaned and not cleaned.startswith("Name") and "On" in cleaned:
            services.append(cleaned)
    return services


def collect_os_fingerprint() -> dict[str, Any]:
    """Collect read-only operating-system attributes commonly exposed in support flows."""
    system_name = platform.system()
    fingerprint: dict[str, Any] = {
        "os_name": system_name,
        "os_version": platform.version(),
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "timezone": time.tzname[0] if time.tzname else None,
        "locale": locale.getlocale(),
        "hardware_model": None,
        "build_number": None,
        "sharing_services": [],
    }

    if system_name == "Darwin":
        fingerprint["os_version"] = _run(["/usr/bin/sw_vers", "-productVersion"]) or platform.mac_ver()[0]
        fingerprint["build_number"] = _run(["/usr/bin/sw_vers", "-buildVersion"])
        fingerprint["hardware_model"] = _run(["/usr/sbin/sysctl", "-n", "hw.model"])
        fingerprint["sharing_services"] = _macos_sharing_services()
    elif system_name == "Linux":
        fingerprint["hardware_model"] = _run(["/usr/bin/uname", "-m"])

    return fingerprint


def score_fingerprint_exposure(fingerprint: dict[str, Any]) -> dict[str, Any]:
    """Score exposure from small, legitimate OS attributes without overstating impact."""
    score = 0
    factors: list[str] = []
    if fingerprint.get("build_number"):
        score += 1
        factors.append("build_number_visible")
    if fingerprint.get("hostname"):
        score += 1
        factors.append("hostname_visible")
    if fingerprint.get("locale") or fingerprint.get("timezone"):
        score += 1
        factors.append("locale_timezone_visible")
    if fingerprint.get("sharing_services"):
        score += 2
        factors.append("sharing_services_visible")

    if score >= 5:
        level = "HIGH"
    elif score >= 3:
        level = "MODERATE"
    else:
        level = "LOW"
    return {"score": score, "level": level, "factors": factors}


def recommendations_for_fingerprint_minimization(
    fingerprint: dict[str, Any] | None = None,
    *,
    high_risk: bool = False,
) -> list[str]:
    """Return safe minimization guidance that avoids system patching."""
    recommendations = [
        "Mantener el sistema operativo, el navegador y las aplicaciones críticas actualizadas.",
        "Reducir servicios de sharing innecesarios y revisar accesos remotos con trazabilidad.",
        "Evitar perfiles de configuración desconocidos o no documentados.",
        "Usar navegadores con protección anti-fingerprinting cuando el riesgo lo justifique.",
        "Separar perfiles corporativos y personales para reducir correlación de identidad.",
        "Evitar publicar capturas con build number, seriales, UUIDs, rutas internas o datos sensibles.",
        "Usar MDM corporativo transparente, documentado y auditable.",
        "Crear políticas de mínimos datos expuestos en tickets de soporte.",
        "Revisar reportes técnicos antes de compartirlos con proveedores externos.",
    ]
    if high_risk:
        recommendations.insert(
            1,
            "Evaluar Lockdown Mode en dispositivos de personas con riesgo elevado, considerando impacto operativo.",
        )
    if fingerprint and fingerprint.get("sharing_services"):
        recommendations.insert(
            1,
            "Priorizar la revisión de servicios de sharing visibles porque aumentan la superficie remota.",
        )
    return recommendations

