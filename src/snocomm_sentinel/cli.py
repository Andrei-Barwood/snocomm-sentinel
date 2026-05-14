"""Command-line interface for Snocomm Sentinel."""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Annotated

import typer

from snocomm_sentinel import __version__
from snocomm_sentinel.checks.fingerprint import (
    collect_os_fingerprint,
    recommendations_for_fingerprint_minimization,
    score_fingerprint_exposure,
)
from snocomm_sentinel.checks.ios_backup import mvt_usage_guidance, verify_backup_directory
from snocomm_sentinel.checks.lockdown import lockdown_finding, lockdown_recommendations
from snocomm_sentinel.checks.macos import collect_macos_checks
from snocomm_sentinel.checks.mvt_bridge import (
    build_mvt_import_document,
    generate_mvt_markdown_summary,
    import_mvt_results,
)
from snocomm_sentinel.config import ensure_shell_history_is_explicit, get_profile, load_config
from snocomm_sentinel.report import (
    generate_markdown_report,
    load_results_json,
    normalize_result_document,
    write_json_report,
    write_markdown_report,
)

app = typer.Typer(
    help=(
        "Toolkit defensivo para privacidad corporativa, exposición del sistema, "
        "hardening y preparación frente a spyware mercenario."
    ),
    no_args_is_help=True,
)


def _echo_json(data: dict[str, object]) -> None:
    typer.echo(json.dumps(data, indent=2, ensure_ascii=False))


def build_scan_results(
    profile_name: str,
    profile_config: dict[str, object],
    *,
    ios_backup: Path | None = None,
    mvt_results: Path | None = None,
) -> dict[str, object]:
    platform_name = platform.system().lower() or "unknown"
    findings: list[dict[str, object]] = []
    metadata: dict[str, object] = {}

    if platform.system() == "Darwin":
        macos_results = collect_macos_checks(
            include_shell_history=bool(profile_config.get("include_shell_history", False)),
            check_profiles_enabled=bool(profile_config.get("check_profiles", True)),
            check_mdm_enabled=bool(profile_config.get("check_mdm", True)),
            check_services_enabled=bool(profile_config.get("check_macos_services", True)),
        )
        metadata["macos"] = macos_results.get("metadata", {})
        findings.extend(macos_results.get("findings", []))

    if profile_config.get("check_fingerprint", True):
        fp = collect_os_fingerprint()
        exposure = score_fingerprint_exposure(fp)
        metadata["fingerprint"] = fp
        metadata["fingerprint_exposure"] = exposure
        if exposure["level"] in {"MODERATE", "HIGH"}:
            findings.append(
                {
                    "id": "FINGERPRINT_EXPOSURE_REVIEW_RECOMMENDED",
                    "severity": "low" if exposure["level"] == "MODERATE" else "medium",
                    "title": "Fingerprint exposure requires review",
                    "explanation": (
                        "Se observaron atributos locales que pueden aumentar la correlación de identidad "
                        "o la exposición operativa en reportes y flujos de soporte."
                    ),
                    "recommendation": "Aplicar minimización de fingerprinting sin modificar archivos del sistema.",
                    "source": "fingerprint",
                    "evidence": exposure,
                }
            )

    if ios_backup:
        metadata["ios_backup"] = verify_backup_directory(ios_backup)
        if not metadata["ios_backup"]["looks_like_ios_backup"]:
            findings.append(
                {
                    "id": "IOS_BACKUP_STRUCTURE_NOT_RECOGNIZED",
                    "severity": "low",
                    "title": "iOS backup directory structure was not recognized",
                    "explanation": "El directorio entregado no contiene los archivos típicos esperados de un backup iOS.",
                    "recommendation": "Verificar ruta, consentimiento y procedimiento de preparación antes de usar MVT.",
                    "source": "ios_backup",
                }
            )

    mvt_path = mvt_results or profile_config.get("mvt_import_path")
    if mvt_path:
        imported = import_mvt_results(Path(str(mvt_path)))
        metadata["mvt"] = imported["summary"]
        findings.extend(imported["findings"])

    lockdown = lockdown_finding(profile_name)
    if lockdown:
        findings.append(lockdown)

    recommendations = recommendations_for_fingerprint_minimization(
        metadata.get("fingerprint") if isinstance(metadata.get("fingerprint"), dict) else None,
        high_risk=profile_name == "high-risk",
    )
    if profile_name in {"corporate", "high-risk"}:
        recommendations.extend(lockdown_recommendations(profile_name))

    results: dict[str, object] = {
        "tool": "snocomm-sentinel",
        "version": __version__,
        "platform": "macos" if platform.system() == "Darwin" else platform_name,
        "profile": profile_name,
        "metadata": metadata,
        "findings": findings,
        "recommendations": recommendations,
    }
    return normalize_result_document(results)


@app.command()
def scan(
    profile: Annotated[
        str,
        typer.Option("--profile", help="Perfil de evaluación: default, corporate o high-risk."),
    ] = "default",
    config: Annotated[
        Path | None,
        typer.Option("--config", help="Ruta a configuración YAML opcional."),
    ] = None,
    include_shell_history: Annotated[
        bool,
        typer.Option(
            "--include-shell-history",
            help=(
                "Procesa historial de shell local. Puede contener información sensible; "
                "requiere consentimiento explícito."
            ),
        ),
    ] = False,
    ios_backup: Annotated[
        Path | None,
        typer.Option("--ios-backup", help="Directorio de backup iOS/iPadOS entregado por el usuario."),
    ] = None,
    mvt_results: Annotated[
        Path | None,
        typer.Option("--mvt-results", help="Archivo JSON de resultados MVT entregado por el usuario."),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", help="Directorio local para results.json y report.md."),
    ] = Path("sentinel-output"),
    output_format: Annotated[
        str,
        typer.Option("--format", help="Formato mostrado por stdout: json o md."),
    ] = "json",
) -> None:
    """Ejecuta comprobaciones locales no invasivas y genera resultados JSON y Markdown."""
    loaded = load_config(config)
    profile_config = ensure_shell_history_is_explicit(get_profile(loaded, profile), include_shell_history)
    results = build_scan_results(profile, profile_config, ios_backup=ios_backup, mvt_results=mvt_results)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_report(results, output_dir / "results.json")
    write_markdown_report(results, output_dir / "report.md")

    if output_format == "md":
        typer.echo(generate_markdown_report(results))
    else:
        _echo_json(results)


@app.command()
def fingerprint() -> None:
    """Muestra datos locales de exposición de fingerprint en modo solo lectura."""
    fp = collect_os_fingerprint()
    exposure = score_fingerprint_exposure(fp)
    _echo_json(
        {
            "fingerprint": fp,
            "exposure": exposure,
            "observations": [
                "El build number se registra solo como contexto de fingerprint; no se modifica el sistema.",
                "La minimización debe enfocarse en servicios, reportes, perfiles y flujos de soporte.",
            ],
            "recommendations": recommendations_for_fingerprint_minimization(fp),
        }
    )


@app.command()
def hardening(
    apply_safe: Annotated[
        bool,
        typer.Option(
            "--apply-safe",
            help="Aplica solo cambios seguros, reversibles y documentados cuando existan.",
        ),
    ] = False,
) -> None:
    """Entrega recomendaciones de hardening sin modificar el sistema por defecto."""
    payload: dict[str, object] = {
        "mode": "apply-safe" if apply_safe else "advisory",
        "system_modified": False,
        "actions_applied": [],
        "recommendations": recommendations_for_fingerprint_minimization(high_risk=False)
        + [
            "Revisar FileVault, firewall, Gatekeeper, SIP y servicios remotos mediante políticas TI.",
            "Documentar perfiles de configuración y MDM antes de cambios operativos.",
            "Para usuarios de alto riesgo, evaluar Lockdown Mode con consentimiento y pruebas de impacto.",
        ],
    }
    if apply_safe:
        payload["note"] = (
            "No se aplicaron cambios automáticos porque las acciones disponibles requieren contexto, "
            "privilegios elevados o aprobación operacional. El modo seguro evita cambios ambiguos."
        )
    _echo_json(payload)


@app.command("mvt-guide")
def mvt_guide() -> None:
    """Explica un flujo consensual y defensivo para usar MVT de Amnesty International."""
    typer.echo(
        "\n".join(
            [
                "# Guía defensiva para MVT",
                "",
                mvt_usage_guidance(),
                "",
                "Pasos de alto nivel:",
                "1. Documentar autorización y alcance.",
                "2. Preparar backup de acuerdo con la documentación oficial de MVT.",
                "3. Ejecutar MVT en un entorno controlado por personal autorizado.",
                "4. Conservar resultados JSON sin alterar evidencia.",
                "5. Interpretar coincidencias con cautela y escalar casos críticos a especialistas forenses.",
                "",
                "Snocomm Sentinel puede importar resultados JSON entregados por el usuario, pero no copia MVT, "
                "no simula análisis forense y no afirma infección sin evidencia verificable.",
            ]
        )
    )


@app.command("mvt-import")
def mvt_import(
    input: Annotated[Path, typer.Option("--input", help="Archivo JSON de resultados MVT.")],
    format: Annotated[str, typer.Option("--format", help="Formato de salida: json o md.")] = "json",
    output: Annotated[Path | None, typer.Option("--output", help="Ruta opcional de salida.")] = None,
) -> None:
    """Importa resultados JSON de MVT entregados por el usuario y genera un resumen conservador."""
    document = build_mvt_import_document(input)
    if format == "md":
        content = generate_mvt_markdown_summary(document)
    else:
        content = json.dumps(document, indent=2, ensure_ascii=False) + "\n"

    if output:
        output.write_text(content, encoding="utf-8")
    else:
        typer.echo(content)


@app.command()
def report(
    input: Annotated[Path, typer.Option("--input", help="Archivo results.json generado por scan.")],
    format: Annotated[str, typer.Option("--format", help="Formato de salida: md o json.")] = "md",
    output: Annotated[Path | None, typer.Option("--output", help="Ruta opcional de salida.")] = None,
) -> None:
    """Genera un informe ejecutivo a partir de resultados JSON."""
    results = load_results_json(input)
    if format == "json":
        normalized = normalize_result_document(results)
        content = json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
    else:
        content = generate_markdown_report(results)

    if output:
        output.write_text(content, encoding="utf-8")
    else:
        typer.echo(content)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
