from enum import Enum

from pydantic import BaseModel


class ConsentStatus(str, Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"


class ConsentChoice(BaseModel):
    category: str
    status: ConsentStatus