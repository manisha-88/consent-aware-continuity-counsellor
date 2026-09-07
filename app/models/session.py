from datetime import date

from pydantic import BaseModel, Field


class Session(BaseModel):
    session_id: str
    client_id: str
    session_date: date
    session_summary: str = Field(min_length=1)