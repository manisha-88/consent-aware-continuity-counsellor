from datetime import date

from app.models import (
    CaseContext,
    ConsentChoice,
    ConsentStatus,
    Session,
)

from app.utils.data_loader import (
    load_consent_choices,
    load_goals,
    load_pending_actions,
    load_sessions,
)


def build_case_context(client_id: str) -> CaseContext:
    sessions = load_sessions()
    goals = load_goals()
    consent = load_consent_choices()
    pending_actions = load_pending_actions()

    session_row = sessions[sessions["client_id"] == client_id]

    if session_row.empty:
        raise ValueError(f"No session found for client {client_id}")

    session_data = session_row.iloc[0]

    session = Session(
        session_id=session_data["session_id"],
        client_id=session_data["client_id"],
        session_date=date.fromisoformat(session_data["session_date"]),
        session_summary=session_data["session_summary"],
    )

    goal_rows = goals[
        (goals["client_id"] == client_id)
        & (goals["goal"].notna())
        & (goals["goal"].str.strip() != "")
    ]

    client_goals = goal_rows["goal"].tolist()

    consent_rows = consent[consent["client_id"] == client_id]

    consent_choices = [
        ConsentChoice(
            category=row["category"],
            status=ConsentStatus(row["status"]),
        )
        for _, row in consent_rows.iterrows()
    ]

    action_rows = pending_actions[
        (pending_actions["client_id"] == client_id)
        & (pending_actions["action"].notna())
        & (pending_actions["action"].str.strip() != "")
    ]

    actions = action_rows["action"].tolist()

    return CaseContext(
        session=session,
        goals=client_goals,
        consent_choices=consent_choices,
        pending_actions=actions,
    )