from snocomm_sentinel.risk import (
    RiskLevel,
    contains_forbidden_absolute_claim,
    sanitize_forensic_language,
    score_findings,
)


def test_scoring_low() -> None:
    assert score_findings([]) == RiskLevel.LOW
    assert score_findings([{"severity": "low"}]) == RiskLevel.LOW


def test_scoring_moderate() -> None:
    findings = [{"severity": "low"}, {"severity": "low"}]
    assert score_findings(findings) == RiskLevel.MODERATE


def test_scoring_high() -> None:
    assert score_findings([{"severity": "high"}]) == RiskLevel.HIGH


def test_scoring_critical_from_forensic_source() -> None:
    findings = [{"severity": "critical", "source": "mvt"}]
    assert score_findings(findings) == RiskLevel.CRITICAL


def test_sanitizer_removes_absolute_pegasus_claims() -> None:
    unsafe_claim = "infectado con " + "Pegasus"
    unsafe_marketing = "anti-" + "Pegasus definitivo"
    text = f"Equipo {unsafe_claim} y {unsafe_marketing}."
    sanitized = sanitize_forensic_language(text)
    assert unsafe_claim not in sanitized
    assert unsafe_marketing not in sanitized
    assert not contains_forbidden_absolute_claim(sanitized)
