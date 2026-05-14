import json

from typer.testing import CliRunner

from snocomm_sentinel.checks.mvt_bridge import (
    build_mvt_import_document,
    generate_mvt_markdown_summary,
    import_mvt_results,
)
from snocomm_sentinel.checks.nebrix_indicators import is_suspicious_tool_name
from snocomm_sentinel.cli import app
from snocomm_sentinel.report import generate_markdown_report, load_results_json


def test_markdown_report_generation_is_conservative() -> None:
    report = generate_markdown_report(
        {
            "tool": "snocomm-sentinel",
            "version": "0.1.0",
            "platform": "macos",
            "profile": "default",
            "findings": [
                {
                    "id": "TEST",
                    "severity": "medium",
                    "title": "Hallazgo compatible con exposición",
                    "recommendation": "Revisar sin afirmar infección.",
                }
            ],
        }
    )
    assert "# Reporte Snocomm Sentinel" in report
    assert "Riesgo general: **MODERATE**" in report
    assert ("infectado con " + "Pegasus") not in report


def test_load_results_json(tmp_path) -> None:
    path = tmp_path / "results.json"
    path.write_text(json.dumps({"findings": []}), encoding="utf-8")
    assert load_results_json(path)["findings"] == []


def test_basic_mvt_import_parses_matches_without_claiming_infection(tmp_path) -> None:
    path = tmp_path / "mvt.json"
    path.write_text(
        json.dumps({"results": [{"indicator": "example-indicator", "matched": True}]}),
        encoding="utf-8",
    )
    imported = import_mvt_results(path)
    assert imported["summary"]["matched_count"] == 1
    assert imported["findings"][0]["source"] == "mvt"
    assert "infección por Pegasus" not in imported["findings"][0]["explanation"]


def test_mvt_import_document_and_markdown(tmp_path) -> None:
    path = tmp_path / "mvt.json"
    path.write_text(
        json.dumps({"detections": [{"ioc": "example.invalid", "type": "domain", "status": "matched"}]}),
        encoding="utf-8",
    )
    document = build_mvt_import_document(path)
    markdown = generate_mvt_markdown_summary(document)
    assert document["matched_count"] == 1
    assert document["matches"][0]["indicator"] == "example.invalid"
    assert "# Resumen de importación MVT" in markdown
    assert "confirma compromiso" in markdown


def test_mvt_import_cli_outputs_markdown(tmp_path) -> None:
    path = tmp_path / "mvt.json"
    path.write_text(
        json.dumps({"matches": [{"indicator": "example.invalid", "matched": True}]}),
        encoding="utf-8",
    )
    runner = CliRunner()
    result = runner.invoke(app, ["mvt-import", "--input", str(path), "--format", "md"])
    assert result.exit_code == 0
    assert "Resumen de importación MVT" in result.output


def test_nebrix_indicator_avoids_defensive_documentation_false_positive() -> None:
    assert is_suspicious_tool_name("nebrix-pegasus")
    assert not is_suspicious_tool_name("NEBRIX_PEGASUS_DISTINCTION.md")
