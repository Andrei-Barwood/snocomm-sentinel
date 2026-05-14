"""Read-only macOS checks for defensive exposure assessment."""

from __future__ import annotations

import platform
import subprocess
from pathlib import Path
from typing import Any

from snocomm_sentinel.checks.nebrix_indicators import (
    findings_from_candidates,
    scan_local_tool_names,
)


def safe_run(command: list[str], timeout: int = 8) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return {"ok": False, "stdout": "", "stderr": "command not found", "returncode": 127}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "timeout", "returncode": 124}
    return {
        "ok": completed.returncode == 0,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "returncode": completed.returncode,
    }


def _finding(
    finding_id: str,
    severity: str,
    title: str,
    explanation: str,
    recommendation: str,
    *,
    evidence: Any | None = None,
    source: str = "macos",
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": finding_id,
        "severity": severity,
        "title": title,
        "explanation": explanation,
        "recommendation": recommendation,
        "source": source,
    }
    if evidence is not None:
        item["evidence"] = evidence
    return item


def collect_system_metadata() -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "platform": platform.system().lower(),
        "os_version": platform.mac_ver()[0] if platform.system() == "Darwin" else platform.version(),
        "build_number": None,
        "hardware_model": None,
    }
    if platform.system() != "Darwin":
        return metadata

    version = safe_run(["/usr/bin/sw_vers", "-productVersion"])
    build = safe_run(["/usr/bin/sw_vers", "-buildVersion"])
    model = safe_run(["/usr/sbin/sysctl", "-n", "hw.model"])
    metadata["os_version"] = version["stdout"] or metadata["os_version"]
    metadata["build_number"] = build["stdout"] or None
    metadata["hardware_model"] = model["stdout"] or None
    return metadata


def check_sip() -> list[dict[str, Any]]:
    result = safe_run(["/usr/bin/csrutil", "status"])
    output = f"{result['stdout']} {result['stderr']}".lower()
    if "disabled" in output:
        return [
            _finding(
                "MACOS_SIP_DISABLED",
                "high",
                "System Integrity Protection appears disabled",
                "SIP deshabilitado aumenta el riesgo de modificaciones no autorizadas del sistema.",
                "Revisar la razón operativa y reactivar SIP cuando sea posible.",
                evidence=result,
            )
        ]
    return []


def check_gatekeeper() -> list[dict[str, Any]]:
    result = safe_run(["/usr/sbin/spctl", "--status"])
    output = f"{result['stdout']} {result['stderr']}".lower()
    if "disabled" in output:
        return [
            _finding(
                "MACOS_GATEKEEPER_DISABLED",
                "high",
                "Gatekeeper appears disabled",
                "Gatekeeper deshabilitado reduce controles preventivos frente a software no confiable.",
                "Reactivar Gatekeeper salvo que exista una excepción documentada y temporal.",
                evidence=result,
            )
        ]
    return []


def check_filevault() -> list[dict[str, Any]]:
    result = safe_run(["/usr/bin/fdesetup", "status"])
    output = f"{result['stdout']} {result['stderr']}".lower()
    if "off" in output:
        return [
            _finding(
                "MACOS_FILEVAULT_DISABLED",
                "high",
                "FileVault appears disabled",
                "El cifrado de disco deshabilitado aumenta exposición ante pérdida o robo del equipo.",
                "Activar FileVault mediante un proceso corporativo documentado y con recuperación de claves.",
                evidence=result,
            )
        ]
    return []


def check_firewall() -> list[dict[str, Any]]:
    result = safe_run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"])
    output = f"{result['stdout']} {result['stderr']}".lower()
    if "disabled" in output or "off" in output:
        return [
            _finding(
                "MACOS_FIREWALL_DISABLED",
                "medium",
                "macOS firewall appears disabled",
                "El firewall deshabilitado puede aumentar la exposición de servicios locales.",
                "Activar el firewall si no existe una razón operacional para mantenerlo apagado.",
                evidence=result,
            )
        ]
    return []


def check_remote_login() -> list[dict[str, Any]]:
    result = safe_run(["/usr/sbin/systemsetup", "-getremotelogin"])
    output = f"{result['stdout']} {result['stderr']}".lower()
    if "on" in output:
        return [
            _finding(
                "MACOS_REMOTE_LOGIN_ENABLED",
                "medium",
                "Remote Login appears enabled",
                "SSH aumenta la superficie de acceso remoto del equipo.",
                "Deshabilitar Remote Login si no es necesario o restringir acceso por usuarios, red y claves.",
                evidence=result,
            )
        ]
    return []


def check_screen_sharing() -> list[dict[str, Any]]:
    sharing = safe_run(["/usr/sbin/sharing", "-l"], timeout=6)
    output = sharing["stdout"].lower()
    if "screen sharing" in output and " on " in f" {output} ":
        return [
            _finding(
                "MACOS_SCREEN_SHARING_ENABLED",
                "medium",
                "Screen Sharing appears enabled",
                "Screen Sharing incrementa la superficie de administración remota.",
                "Deshabilitarlo si no es requerido o restringirlo a procesos de soporte autorizados.",
                evidence=sharing,
            )
        ]
    return []


def check_profiles() -> list[dict[str, Any]]:
    result = safe_run(["/usr/bin/profiles", "list", "-output", "stdout"], timeout=10)
    output = result["stdout"]
    if result["returncode"] != 0:
        return []
    if "There are no configuration profiles installed" in output:
        return []
    if output.strip():
        return [
            _finding(
                "MACOS_CONFIGURATION_PROFILES_PRESENT",
                "low",
                "Configuration profiles are present",
                "Los perfiles de configuración pueden ser legítimos, pero deben estar inventariados.",
                "Revisar metadata, origen y aprobación de los perfiles instalados.",
                evidence={"lines": output.splitlines()[:20]},
            )
        ]
    return []


def check_mdm() -> list[dict[str, Any]]:
    result = safe_run(["/usr/bin/profiles", "status", "-type", "enrollment"], timeout=10)
    output = f"{result['stdout']} {result['stderr']}"
    lowered = output.lower()
    if "enrolled" in lowered and "no" not in lowered:
        return [
            _finding(
                "MACOS_POSSIBLE_MDM_ENROLLMENT",
                "medium",
                "Possible MDM enrollment detected",
                "La inscripción MDM puede ser legítima, pero requiere transparencia, documentación y alcance claro.",
                "Confirmar proveedor, políticas aplicadas, aprobación interna y consentimiento corporativo.",
                evidence=result,
            )
        ]
    return []


def check_launch_items() -> list[dict[str, Any]]:
    roots = [
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
        Path.home() / "Library" / "LaunchAgents",
    ]
    suspicious_terms = ("pegasus", "nebrix", "nso", "spyware", "shell")
    findings: list[dict[str, Any]] = []
    for root in roots:
        if not root.exists():
            continue
        try:
            for item in root.iterdir():
                lowered = item.name.lower()
                if any(term in lowered for term in suspicious_terms):
                    findings.append(
                        _finding(
                            "MACOS_SUSPICIOUS_LAUNCH_ITEM_NAME",
                            "high",
                            "LaunchAgent or LaunchDaemon name requires review",
                            "El nombre del elemento coincide con patrones que ameritan revisión local.",
                            "No borrar automáticamente. Preservar evidencia y revisar firma, origen y necesidad.",
                            evidence={"path": str(item)},
                        )
                    )
        except (OSError, PermissionError):
            continue
    return findings


def check_shell_history_for_local_tooling() -> list[dict[str, Any]]:
    history_files = [Path.home() / ".zsh_history", Path.home() / ".bash_history"]
    findings: list[dict[str, Any]] = [
        _finding(
            "SHELL_HISTORY_SCAN_EXPLICITLY_ENABLED",
            "info",
            "Shell history scan was explicitly enabled",
            "El historial de shell puede contener información sensible y se procesa solo localmente.",
            "Usar esta opción únicamente con consentimiento documentado y necesidad proporcional.",
            source="local_shell_history",
        )
    ]
    terms = ("nebrix", "pegasus")
    for history_file in history_files:
        if not history_file.exists():
            continue
        try:
            with history_file.open("r", encoding="utf-8", errors="ignore") as handle:
                for line_number, line in enumerate(handle, start=1):
                    lowered = line.lower()
                    if any(term in lowered for term in terms):
                        findings.append(
                            _finding(
                                "SHELL_HISTORY_PUBLIC_PEGASUS_REFERENCE",
                                "medium",
                                "Shell history references Pegasus or Nebrix terms",
                                "Se observaron referencias locales a términos compatibles con herramientas públicas o repositorios.",
                                "Revisar contexto con el usuario. No asumir compromiso ni ejecutar artefactos relacionados.",
                                evidence={"file": str(history_file), "line": line_number},
                                source="local_shell_history",
                            )
                        )
                        break
        except (OSError, PermissionError):
            continue
    return findings


def collect_macos_checks(
    *,
    include_shell_history: bool = False,
    check_profiles_enabled: bool = True,
    check_mdm_enabled: bool = True,
    check_services_enabled: bool = True,
) -> dict[str, Any]:
    """Run read-only checks. No command uses shell=True or privilege escalation."""
    metadata = collect_system_metadata()
    findings: list[dict[str, Any]] = []

    if platform.system() != "Darwin":
        return {"metadata": metadata, "findings": findings}

    findings.extend(check_sip())
    findings.extend(check_gatekeeper())
    findings.extend(check_filevault())
    if check_services_enabled:
        findings.extend(check_firewall())
        findings.extend(check_remote_login())
        findings.extend(check_screen_sharing())
    if check_profiles_enabled:
        findings.extend(check_profiles())
    if check_mdm_enabled:
        findings.extend(check_mdm())
    findings.extend(check_launch_items())

    candidates = scan_local_tool_names()
    findings.extend(findings_from_candidates(candidates))

    if include_shell_history:
        findings.extend(check_shell_history_for_local_tooling())

    if metadata.get("build_number"):
        findings.append(
            _finding(
                "MACOS_BUILD_NUMBER_RECORDED_FOR_FINGERPRINT_CONTEXT",
                "info",
                "Build number recorded as fingerprint context",
                "El build number ayuda a contextualizar versión y exposición, pero no es por sí solo una causa de compromiso.",
                "Minimizar su exposición en capturas, tickets y reportes externos cuando no sea necesario.",
                evidence={"build_number": metadata["build_number"]},
            )
        )

    return {"metadata": metadata, "findings": findings}

