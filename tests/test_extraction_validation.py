from app.models import ExtractedInformation, InformationCategory
from app.services.extraction_validation_service import (
    find_possible_omissions,
    find_possible_hallucinations,
)


def test_detect_missing_sleep_information():

    session = (
        "Student reports exam stress and difficulty sleeping."
    )

    extracted = [
        ExtractedInformation(
            category=InformationCategory.EXAM_STRESS,
            content="Student reports examination-related stress.",
        )
    ]

    omissions = find_possible_omissions(
        session,
        extracted,
    )

    assert InformationCategory.SLEEP_DIFFICULTY in omissions

def test_detect_hallucinated_ambiguous_statement():

    session = (
        "Student reports exam stress and difficulty sleeping."
    )

    extracted = [
        ExtractedInformation(
            category=InformationCategory.EXAM_STRESS,
            content="Student reports examination-related stress.",
        ),
        ExtractedInformation(
            category=InformationCategory.AMBIGUOUS_STATEMENT,
            content="Student makes an ambiguous statement.",
        ),
    ]

    hallucinations = find_possible_hallucinations(
        session,
        extracted,
    )

    assert len(hallucinations) == 1
    assert (
        hallucinations[0].category
        == InformationCategory.AMBIGUOUS_STATEMENT
    )