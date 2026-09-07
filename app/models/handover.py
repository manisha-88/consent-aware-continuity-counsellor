from pydantic import BaseModel

from .risk import RiskAssessment


class HandoverSummary(BaseModel):
    current_concern: str
    client_goals: list[str]
    relevant_information: list[str]
    pending_actions: list[str]
    restricted_information: list[str]
    risk_assessment: RiskAssessment
    escalation_message: str
    human_review_required: bool