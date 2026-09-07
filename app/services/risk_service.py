from app.models import CaseContext
from app.models.risk import RiskAssessment, RiskLevel

from app.rules.risk_rules import (
    contains_ambiguous_indicator,
    contains_urgent_indicator,
)


def assess_risk(case: CaseContext) -> RiskAssessment:
    text = case.session.session_summary

    if contains_urgent_indicator(text):
        return RiskAssessment(
            level=RiskLevel.URGENT,
            reason=(
                "Potential urgent safety concern detected. "
                "Professional assessment is required."
            ),
            human_review_required=True,
            escalation_required=True,
        )

    if contains_ambiguous_indicator(text):
        return RiskAssessment(
            level=RiskLevel.AMBIGUOUS,
            reason=(
                "Ambiguous statement detected. "
                "The meaning cannot be safely determined automatically."
            ),
            human_review_required=True,
            escalation_required=False,
        )

    return RiskAssessment(
        level=RiskLevel.LOW,
        reason="No predefined urgent or ambiguous indicator detected.",
        human_review_required=False,
        escalation_required=False,
    )