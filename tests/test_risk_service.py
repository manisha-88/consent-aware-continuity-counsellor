from app.services.case_service import build_case_context
from app.services.risk_service import assess_risk
from app.models.risk import RiskLevel
from app.rules.escalation_rules import get_escalation_message

def test_low_risk_case():
    case = build_case_context("C001")

    result = assess_risk(case)

    assert result.level == RiskLevel.LOW
    assert result.human_review_required is False
    assert result.escalation_required is False


def test_ambiguous_case():
    case = build_case_context("C006")

    result = assess_risk(case)

    assert result.level == RiskLevel.AMBIGUOUS
    assert result.human_review_required is True
    assert result.escalation_required is False


def test_urgent_case():
    case = build_case_context("C007")

    result = assess_risk(case)

    assert result.level == RiskLevel.URGENT
    assert result.human_review_required is True
    assert result.escalation_required is True


def test_urgent_escalation_message():
    message = get_escalation_message(RiskLevel.URGENT)

    assert "URGENT HUMAN REVIEW REQUIRED" in message


def test_ambiguous_escalation_message():
    message = get_escalation_message(RiskLevel.AMBIGUOUS)

    assert "HUMAN REVIEW REQUIRED" in message