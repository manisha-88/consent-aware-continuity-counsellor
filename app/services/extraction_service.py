from app.models import ExtractedInformation, InformationCategory


def extract_information(session_summary: str) -> list[ExtractedInformation]:
    """
    Temporary rule-based extractor.

    This will later be replaced by the LLM.
    """

    text = session_summary.lower()

    information = []

    if "exam" in text or "examination" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.EXAM_STRESS,
                content="Student reports examination-related stress.",
            )
        )

    if "academic" in text or "grade" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.ACADEMIC_CONCERN,
                content="Student reports an academic-related concern.",
            )
        )

    if "family" in text or "parents" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.FAMILY_INFORMATION,
                content="Student reports family-related concerns.",
            )
        )

    if "sleep" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.SLEEP_DIFFICULTY,
                content="Student reports difficulty with sleep.",
            )
        )

    if "social support" in text or "isolated" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.SOCIAL_SUPPORT,
                content="Student reports concerns related to social support.",
            )
        )

    if "unsafe" in text:
        information.append(
            ExtractedInformation(
                category=InformationCategory.SAFETY_CONCERN,
                content="Student reports feeling unsafe.",
            )
        )

    return information