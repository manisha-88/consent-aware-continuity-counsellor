from app.models.risk import RiskLevel
from app.services.case_service import build_case_context
from app.services.handover_service import generate_safe_handover


def test_normal_handover():
    case = build_case_context("C001")

    handover = generate_safe_handover(case)

    assert handover.current_concern != ""
    assert len(handover.client_goals) > 0
    assert len(handover.pending_actions) > 0
    assert handover.risk_assessment.level == RiskLevel.LOW
    assert handover.human_review_required is False


def test_restricted_information():
    case = build_case_context("C003")

    handover = generate_safe_handover(case)

    assert "family_information" in handover.restricted_information


def test_urgent_handover():
    case = build_case_context("C007")

    handover = generate_safe_handover(case)

    assert handover.risk_assessment.level == RiskLevel.URGENT
    assert handover.human_review_required is True
    assert handover.risk_assessment.escalation_required is True


def test_ambiguous_handover():
    case = build_case_context("C006")

    handover = generate_safe_handover(case)

    assert handover.risk_assessment.level == RiskLevel.AMBIGUOUS
    assert handover.human_review_required is True