from app.services.case_service import build_case_context


def test_case_context():
    case = build_case_context("C003")

    assert case.session.client_id == "C003"
    assert len(case.goals) > 0
    assert len(case.consent_choices) > 0
    assert len(case.pending_actions) > 0


def test_missing_goal():
    case = build_case_context("C012")

    assert case.goals == []


def test_unknown_client():
    try:
        build_case_context("C999")
        assert False
    except ValueError:
        assert True