"""Configuration loading for Snocomm Sentinel."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "profiles": {
        "default": {
            "check_macos_services": True,
            "check_profiles": True,
            "check_mdm": True,
            "check_fingerprint": True,
            "include_shell_history": False,
            "mvt_import_path": None,
            "report_format": "json",
        },
        "corporate": {
            "check_macos_services": True,
            "check_profiles": True,
            "check_mdm": True,
            "check_fingerprint": True,
            "include_shell_history": False,
            "mvt_import_path": None,
            "report_format": "md",
            "recommend_lockdown_mode": "case-by-case",
        },
        "high-risk": {
            "check_macos_services": True,
            "check_profiles": True,
            "check_mdm": True,
            "check_fingerprint": True,
            "include_shell_history": False,
            "mvt_import_path": None,
            "report_format": "md",
            "recommend_lockdown_mode": True,
        },
    }
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge dictionaries without mutating either input."""
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load YAML configuration and merge it over safe defaults."""
    if path is None:
        return deepcopy(DEFAULT_CONFIG)

    config_path = Path(path).expanduser()
    with config_path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    if not isinstance(loaded, dict):
        raise ValueError("La configuración YAML debe contener un objeto raíz.")
    return deep_merge(DEFAULT_CONFIG, loaded)


def get_profile(config: dict[str, Any], profile: str) -> dict[str, Any]:
    """Return a profile merged over the default profile."""
    profiles = config.get("profiles", {})
    if profile not in profiles:
        available = ", ".join(sorted(profiles)) or "ninguno"
        raise KeyError(f"Perfil desconocido: {profile}. Perfiles disponibles: {available}.")
    default_profile = profiles.get("default", {})
    return deep_merge(default_profile, profiles[profile])


def ensure_shell_history_is_explicit(profile_config: dict[str, Any], cli_flag: bool) -> dict[str, Any]:
    """Keep shell history scanning disabled unless the user passes an explicit flag."""
    normalized = deepcopy(profile_config)
    normalized["include_shell_history"] = bool(cli_flag)
    return normalized

