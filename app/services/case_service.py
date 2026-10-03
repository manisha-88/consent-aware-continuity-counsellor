from datetime import date
from app.models import CaseContext, ConsentChoice, ConsentStatus, Session
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

    clean_input_id = str(client_id).strip().replace('"', "").replace("'", "")
    
    # Debug what is loaded
    print(f"Searching for client: {clean_input_id}")
    print(f"Sessions count: {len(sessions)}, Goals count: {len(goals)}, Consent count: {len(consent)}, Actions count: {len(pending_actions)}")

    # Normalize dataframe client_ids
    for df_name, df in [("sessions", sessions), ("goals", goals), ("consent", consent), ("pending_actions", pending_actions)]:
        if "client_id" in df.columns:
            df["client_id"] = df["client_id"].astype(str).str.strip().str.replace('"', "").str.replace("'", "")
        else:
            print(f"ERROR: 'client_id' column missing in {df_name}!")

    session_row = sessions[sessions["client_id"].str.lower() == clean_input_id.lower()]
    if session_row.empty:
        print(f"FAIL: Client {clean_input_id} not found in sessions.csv! Available sessions IDs: {sessions['client_id'].unique().tolist()}")
        raise ValueError(f"No session found for client {client_id}")
    
    

    session_data = session_row.iloc[0]
    matched_id = session_data["client_id"]

    session = Session(
        session_id=str(session_data["session_id"]).strip(),
        client_id=matched_id,
        session_date=date.fromisoformat(str(session_data["session_date"]).strip()),
        session_summary=str(session_data["session_summary"]),
    )

    goal_rows = goals[
        (goals["client_id"] == matched_id)
        & (goals["goal"].notna())
        & (goals["goal"].str.strip() != "")
    ]
    client_goals = goal_rows["goal"].tolist()

    consent_rows = consent[consent["client_id"] == matched_id]
    consent_choices = [
        ConsentChoice(
            category=str(row["category"]).strip(),
            status=ConsentStatus(str(row["status"]).strip()),
        )
        for _, row in consent_rows.iterrows()
    ]

    action_rows = pending_actions[
        (pending_actions["client_id"] == matched_id)
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