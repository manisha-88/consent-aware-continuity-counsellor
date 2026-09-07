from datetime import datetime

from pydantic import BaseModel


class HandoverReview(BaseModel):
    status: str
    reviewer_notes: str = ""
    edited_handover: str = ""
    reviewed_at: datetime | None = None