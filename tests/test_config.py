from typer.testing import CliRunner

from snocomm_sentinel.checks.fingerprint import recommendations_for_fingerprint_minimization
from snocomm_sentinel.cli import app
from snocomm_sentinel.config import get_profile, load_config


def test_load_yaml_config_and_profile(tmp_path) -> None:
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        """
profiles:
  corporate:
    check_profiles: false
    report_format: md
""",
        encoding="utf-8",
    )
    config = load_config(config_path)
    profile = get_profile(config, "corporate")
    assert profile["check_profiles"] is False
    assert profile["check_mdm"] is True
    assert profile["include_shell_history"] is False


def test_fingerprinting_recommendations_are_safe() -> None:
    recommendations = recommendations_for_fingerprint_minimization(
        {"build_number": "23A344", "sharing_services": ["Screen Sharing On"]},
        high_risk=True,
    )
    joined = " ".join(recommendations).lower()
    assert "lockdown mode" in joined
    assert "build number" in joined
    assert "modificar archivos del sistema" not in joined


def test_cli_help_is_stable() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "scan" in result.output
    assert "fingerprint" in result.output

