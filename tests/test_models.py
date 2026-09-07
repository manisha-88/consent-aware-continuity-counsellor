from datetime import date

from app.models import (
    Client,
    ConsentChoice,
    ConsentStatus,
    RiskAssessment,
    RiskLevel,
    Session,
)


def test_client():
    client = Client(client_id="C001")

    assert client.client_id == "C001"


def test_session():
    session = Session(
        session_id="SS001",
        client_id="C001",
        session_date=date(2026, 8, 26),
        session_summary="Student reports exam-related stress.",
    )

    assert session.session_id == "SS001"


def test_consent():
    consent = ConsentChoice(
        category="family_information",
        status=ConsentStatus.RESTRICTED,
    )

    assert consent.status == ConsentStatus.RESTRICTED


def test_risk():
    risk = RiskAssessment(
        level=RiskLevel.URGENT,
        reason="Potential safety concern requires human assessment.",
        human_review_required=True,
        escalation_required=True,
    )

    assert risk.human_review_required is True
    assert risk.escalation_required is True