from app.services.case_service import build_case_context
from app.services.extraction_service import extract_information
from app.services.filter_service import filter_information


def test_family_information_is_filtered():
    case = build_case_context("C003")

    extracted = extract_information(
        case.session.session_summary
    )

    allowed, restricted = filter_information(
        case,
        extracted,
    )

    allowed_categories = [
        item.category
        for item in allowed
    ]

    restricted_categories = [
        item.category
        for item in restricted
    ]

    assert "family_information" not in allowed_categories
    assert "family_information" in restricted_categories