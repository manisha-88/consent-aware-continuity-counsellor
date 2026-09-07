from pydantic import BaseModel, Field

from .information_category import InformationCategory


class ExtractedInformation(BaseModel):
    category: InformationCategory
    content: str = Field(min_length=1)


class ExtractionResult(BaseModel):
    information: list[ExtractedInformation]