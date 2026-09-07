from app.services.case_service import build_case_context
from app.services.consent_service import (
    get_restricted_categories,
    get_unknown_categories,
    is_allowed,
)


def test_allowed_information():
    case = build_case_context("C003")

    assert is_allowed(case, "exam_stress") is True


def test_restricted_information():
    case = build_case_context("C003")

    assert is_allowed(case, "family_information") is False


def test_restricted_category_list():
    case = build_case_context("C003")

    restricted = get_restricted_categories(case)

    assert "family_information" in restricted


def test_unknown_consent():
    case = build_case_context("C006")

    unknown = get_unknown_categories(case)

    assert "ambiguous_statement" in unknown