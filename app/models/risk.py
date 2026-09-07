from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "low"
    AMBIGUOUS = "ambiguous"
    URGENT = "urgent"


class RiskAssessment(BaseModel):
    level: RiskLevel
    reason: str
    human_review_required: bool
    escalation_required: bool