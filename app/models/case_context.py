from datetime import date

from pydantic import BaseModel

from .consent import ConsentChoice
from .session import Session


class CaseContext(BaseModel):
    session: Session
    goals: list[str]
    consent_choices: list[ConsentChoice]
    pending_actions: list[str]