"""Read-only local indicators for public tools named Pegasus or Nebrix/Pegasus."""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from pathlib import Path

DEFAULT_SUSPICIOUS_NAMES = (
    "nebrix",
    "nebrix-pegasus",
    "pegasus-shell",
    "pegasus.py",
    "pegasus.sh",
    "pegasus-master",
    "pegasus-main",
    "public-pegasus",
)


def is_suspicious_tool_name(name: str, patterns: Iterable[str] = DEFAULT_SUSPICIOUS_NAMES) -> bool:
    lowered = name.lower().strip()
    stem = Path(lowered).stem
    normalized = re.sub(r"[\s_]+", "-", stem)
    pattern_set = {pattern.lower() for pattern in patterns}
    return lowered in pattern_set or stem in pattern_set or normalized in pattern_set


def candidate_search_roots() -> list[Path]:
    home = Path.home()
    roots = [
        Path.cwd(),
        home / "Desktop",
        home / "Downloads",
        home / "Documents",
        home / "Projects",
        home / "Developer",
        home / "Public",
    ]
    return [root for root in roots if root.exists()]


def scan_local_tool_names(
    roots: Iterable[Path] | None = None,
    *,
    max_depth: int = 3,
    max_entries: int = 5000,
) -> list[dict[str, str]]:
    """Scan local file and directory names without executing or opening candidates."""
    findings: list[dict[str, str]] = []
    queue: list[tuple[Path, int]] = [(root, 0) for root in (roots or candidate_search_roots())]
    visited = 0

    while queue and visited < max_entries:
        current, depth = queue.pop(0)
        visited += 1
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    if is_suspicious_tool_name(entry.name):
                        findings.append({"path": str(path), "name": entry.name})
                    if entry.is_dir(follow_symlinks=False) and depth < max_depth:
                        queue.append((path, depth + 1))
        except (OSError, PermissionError):
            continue
    return findings


def findings_from_candidates(candidates: list[dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "id": "LOCAL_PUBLIC_PEGASUS_TOOL_NAME",
            "severity": "high",
            "title": "Nombre local compatible con herramienta pública llamada Pegasus o Nebrix/Pegasus",
            "explanation": (
                "Se observó una ruta local cuyo nombre coincide con patrones de herramientas públicas "
                "o repositorios de terceros. Esto no equivale a compromiso por spyware mercenario."
            ),
            "recommendation": (
                "No ejecutar el contenido. Revisar procedencia, propósito, permisos y necesidad; "
                "documentar el hallazgo y retirar repositorios ofensivos de equipos institucionales."
            ),
            "evidence": candidate,
            "source": "local_name_scan",
        }
        for candidate in candidates
    ]
