from app.models import CaseContext, ConsentStatus


def get_consent_map(case: CaseContext) -> dict[str, ConsentStatus]:
    return {
        choice.category: choice.status
        for choice in case.consent_choices
    }


def is_allowed(case: CaseContext, category: str) -> bool:
    consent_map = get_consent_map(case)

    status = consent_map.get(category, ConsentStatus.UNKNOWN)

    return status == ConsentStatus.ALLOWED


def get_restricted_categories(case: CaseContext) -> list[str]:
    return [
        choice.category
        for choice in case.consent_choices
        if choice.status == ConsentStatus.RESTRICTED
    ]


def get_unknown_categories(case: CaseContext) -> list[str]:
    return [
        choice.category
        for choice in case.consent_choices
        if choice.status == ConsentStatus.UNKNOWN
    ]


def find_missing_consent_categories(
    case: CaseContext,
    information,
) -> list[str]:
    """
    Find extracted information categories
    that do not have an explicit consent
    decision.
    """

    consent_map = get_consent_map(
        case
    )


    missing_categories = []


    for item in information:

        category = item.category.value


        if (
            category
            not in consent_map
        ):

            missing_categories.append(
                category
            )


    return list(
        set(
            missing_categories
        )
    )