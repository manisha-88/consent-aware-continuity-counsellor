from app.models import (
    ExtractedInformation,
    InformationCategory,
)


def extract_with_fallback(
    session_summary: str,
) -> list[ExtractedInformation]:
    """
    Safe rule-based fallback extractor.

    Used when the LLM is unavailable or
    does not return useful information.
    """

    text = session_summary.lower()

    information = []


    # -----------------------------------------
    # EXAM STRESS
    # -----------------------------------------

    if (
        "exam" in text
        or "examination" in text
    ):

        information.append(
            ExtractedInformation(
                category=InformationCategory.EXAM_STRESS,
                content=(
                    "Student reports "
                    "examination-related stress."
                ),
            )
        )


    # -----------------------------------------
    # ACADEMIC CONCERN
    # -----------------------------------------

    if (
        "academic" in text
        or "grade" in text
    ):

        information.append(
            ExtractedInformation(
                category=InformationCategory.ACADEMIC_CONCERN,
                content=(
                    "Student reports an "
                    "academic-related concern."
                ),
            )
        )


    # -----------------------------------------
    # FAMILY INFORMATION
    # -----------------------------------------

    if (
        "family" in text
        or "parents" in text
    ):

        information.append(
            ExtractedInformation(
                category=(
                    InformationCategory
                    .FAMILY_INFORMATION
                ),
                content=(
                    "Student reports "
                    "family-related concerns."
                ),
            )
        )


    # -----------------------------------------
    # SLEEP DIFFICULTY
    # -----------------------------------------

    if "sleep" in text:

        information.append(
            ExtractedInformation(
                category=(
                    InformationCategory
                    .SLEEP_DIFFICULTY
                ),
                content=(
                    "Student reports "
                    "difficulty with sleep."
                ),
            )
        )


    # -----------------------------------------
    # SOCIAL SUPPORT
    # -----------------------------------------

    if (
        "social support" in text
        or "isolated" in text
    ):

        information.append(
            ExtractedInformation(
                category=(
                    InformationCategory
                    .SOCIAL_SUPPORT
                ),
                content=(
                    "Student reports concerns "
                    "related to social support."
                ),
            )
        )


    # -----------------------------------------
    # SAFETY CONCERN
    # -----------------------------------------

    if (
        "unsafe" in text
        or "immediate danger" in text
    ):

        information.append(
            ExtractedInformation(
                category=(
                    InformationCategory
                    .SAFETY_CONCERN
                ),
                content=(
                    "Student reports a "
                    "potential safety concern."
                ),
            )
        )


    return information