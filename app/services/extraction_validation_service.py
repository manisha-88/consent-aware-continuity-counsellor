from app.models import ExtractedInformation, InformationCategory


KEYWORD_CATEGORY_MAP = {
    InformationCategory.FAMILY_INFORMATION: [
        "family",
        "parents",
        "parent",
    ],
    InformationCategory.SLEEP_DIFFICULTY: [
        "sleep",
        "sleeping",
        "insomnia",
    ],
    InformationCategory.SOCIAL_SUPPORT: [
        "isolated",
        "lonely",
        "social support",
    ],
    InformationCategory.EXAM_STRESS: [
        "exam",
        "examination",
    ],
}


def find_possible_omissions(
    session_summary: str,
    extracted: list[ExtractedInformation],
) -> list[InformationCategory]:

    text = session_summary.lower()

    extracted_categories = {
        item.category
        for item in extracted
    }

    possible_omissions = []

    for category, keywords in KEYWORD_CATEGORY_MAP.items():

        keyword_found = any(
            keyword in text
            for keyword in keywords
        )

        if (
            keyword_found
            and category not in extracted_categories
        ):
            possible_omissions.append(category)

    return possible_omissions


def find_possible_hallucinations(
    session_summary: str,
    extracted: list[ExtractedInformation],
) -> list[ExtractedInformation]:

    text = session_summary.lower()

    hallucinated = []

    for item in extracted:

        category = item.category

        if category == InformationCategory.FAMILY_INFORMATION:
            if not any(
                word in text
                for word in ["family", "parent", "parents"]
            ):
                hallucinated.append(item)

        elif category == InformationCategory.SLEEP_DIFFICULTY:
            if not any(
                word in text
                for word in ["sleep", "sleeping", "insomnia"]
            ):
                hallucinated.append(item)

        elif category == InformationCategory.AMBIGUOUS_STATEMENT:
            if not any(
                phrase in text
                for phrase in [
                    "do not know how much longer",
                    "cannot continue",
                    "can't continue",
                    "cannot go on",
                    "can't go on",
                    "give up",
                ]
            ):
                hallucinated.append(item)

    return hallucinated