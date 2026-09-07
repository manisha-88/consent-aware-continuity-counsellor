from app.models import CaseContext, ExtractedInformation
from app.services.consent_service import is_allowed


def filter_information(
    case: CaseContext,
    information: list[ExtractedInformation],
) -> tuple[list[ExtractedInformation], list[ExtractedInformation]]:

    allowed = []
    restricted = []

    for item in information:

        if is_allowed(case, item.category):
            allowed.append(item)
        else:
            restricted.append(item)

    return allowed, restricted