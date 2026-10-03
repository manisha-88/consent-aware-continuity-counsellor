import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
AUDIT_LOG_FILE = BASE_DIR / "data" / "audit" / "audit_records.json"

def log_handover_access(user_id: str, role: str, client_id: str, action: str, consent_verified: bool):
    """
    Logs sensitive record access and handover events for compliance auditing.
    """
    AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "role": role,
        "client_id": client_id,
        "action": action,
        "consent_verified": consent_verified,
    }

    records = []
    if AUDIT_LOG_FILE.exists() and AUDIT_LOG_FILE.stat().st_size > 0:
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except json.JSONDecodeError:
            records = []

    records.append(log_entry)

    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    return log_entry