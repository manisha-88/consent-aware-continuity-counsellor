from app.utils.data_loader import (
    load_clients,
    load_consent_choices,
    load_goals,
    load_pending_actions,
    load_sessions,
)


def test_clients():
    df = load_clients()

    assert len(df) == 12
    assert "client_id" in df.columns


def test_sessions():
    df = load_sessions()

    assert len(df) == 12
    assert "session_summary" in df.columns


def test_goals():
    df = load_goals()

    assert len(df) == 12
    assert "goal" in df.columns


def test_consent():
    df = load_consent_choices()

    assert len(df) > 0
    assert "status" in df.columns


def test_pending_actions():
    df = load_pending_actions()

    assert len(df) == 12
    assert "action" in df.columns