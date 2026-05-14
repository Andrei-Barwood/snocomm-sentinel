"""Read-only helpers for user-provided iOS/iPadOS backup directories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TYPICAL_BACKUP_FILES = ("Manifest.db", "Manifest.plist", "Info.plist", "Status.plist")
MVT_COLLECTION_KEYS = (
    "results",
    "findings",
    "detections",
    "matches",
    "iocs",
    "indicators",
    "records",
)


def verify_backup_directory(path: str | Path) -> dict[str, Any]:
    backup_path = Path(path).expanduser()
    present = [name for name in TYPICAL_BACKUP_FILES if (backup_path / name).exists()]
    missing = [name for name in TYPICAL_BACKUP_FILES if name not in present]
    return {
        "path": str(backup_path),
        "exists": backup_path.exists(),
        "typical_files_present": present,
        "typical_files_missing": missing,
        "looks_like_ios_backup": backup_path.exists() and "Manifest.db" in present,
    }


def mvt_usage_guidance() -> str:
    return (
        "Use MVT de Amnesty International solo con autorización del dueño del dispositivo "
        "o dentro de un proceso corporativo legítimo, documentado y consentido. "
        "Snocomm Sentinel no reemplaza a MVT ni inventa resultados forenses; puede ayudar a "
        "preparar el flujo, documentar consentimiento y convertir resultados entregados por el usuario "
        "en reportes ejecutivos conservadores."
    )


def extract_json_records(data: Any) -> list[dict[str, Any]]:
    """Extract records from common JSON shapes without assuming a fixed MVT version."""
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    for key in MVT_COLLECTION_KEYS:
        raw_records = data.get(key)
        if isinstance(raw_records, list):
            return [item for item in raw_records if isinstance(item, dict)]
    return [data]


def record_is_match(record: dict[str, Any]) -> bool:
    """Return whether a record should be treated as a high-level match."""
    if "matched" in record:
        return bool(record["matched"])
    if "match" in record:
        return bool(record["match"])
    if "detected" in record:
        return bool(record["detected"])
    if "matches" in record and isinstance(record["matches"], list):
        return bool(record["matches"])
    status = str(record.get("status", "")).lower()
    if status in {"match", "matched", "detected", "positive"}:
        return True
    if status in {"clean", "not_found", "negative", "no_match"}:
        return False
    return bool(record.get("indicator") or record.get("ioc"))


def parse_mvt_json(path: str | Path) -> dict[str, Any]:
    """Parse high-level MVT JSON supplied by the user without asserting infection."""
    json_path = Path(path).expanduser()
    with json_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    records = extract_json_records(data)

    high_level = []
    for record in records:
        indicator = (
            record.get("indicator")
            or record.get("ioc")
            or record.get("name")
            or record.get("description")
            or "mvt_record"
        )
        matched = record_is_match(record)
        if matched:
            high_level.append(
                {
                    "indicator": str(indicator),
                    "source_file": str(json_path),
                    "raw_type": str(record.get("type", "unknown")),
                }
            )

    return {
        "source": str(json_path),
        "record_count": len(records),
        "matched_count": len(high_level),
        "matches": high_level,
    }
