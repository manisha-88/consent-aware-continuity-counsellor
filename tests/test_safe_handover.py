from app.services.case_service import build_case_context
from app.services.handover_service import generate_safe_handover


def test_restricted_information_does_not_leak():

    case = build_case_context("C003")

    handover = generate_safe_handover(case)

    handover_text = " ".join([
        handover.current_concern,
        *handover.relevant_information,
        *handover.client_goals,
        *handover.pending_actions,
    ]).lower()

    assert "family conflict" not in handover_text
    assert "family-related" not in handover_text
    assert "family information" not in handover_text

    assert "family_information" in (
        handover.restricted_information
    )


def test_normal_case_contains_allowed_information():

    case = build_case_context("C001")

    handover = generate_safe_handover(case)

    assert handover.risk_assessment.level.value == "low"

    assert len(
        handover.relevant_information
    ) > 0

    assert handover.human_review_required is False


def test_urgent_case_requires_human_review():

    case = build_case_context("C007")

    handover = generate_safe_handover(case)

    assert handover.risk_assessment.level.value == "urgent"

    assert handover.human_review_required is True

    assert handover.risk_assessment.escalation_required is True

    assert "URGENT HUMAN REVIEW REQUIRED" in (
        handover.escalation_message
    )

def test_ambiguous_case_requires_human_review():

    case = build_case_context("C006")

    handover = generate_safe_handover(case)

    assert handover.risk_assessment.level.value == "ambiguous"

    assert handover.human_review_required is True

    assert handover.risk_assessment.escalation_required is False