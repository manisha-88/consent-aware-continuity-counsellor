from pathlib import Path
from datetime import datetime
import json


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

AUDIT_DIR = BASE_DIR / "data" / "audit"
AUDIT_FILE = AUDIT_DIR / "audit_records.json"


# ============================================================
# INITIALIZE AUDIT STORAGE
# ============================================================

def initialize_audit_file():

    AUDIT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not AUDIT_FILE.exists():

        with open(
            AUDIT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# ============================================================
# READ AUDIT RECORDS
# ============================================================

def get_audit_records():

    initialize_audit_file()

    try:

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            records = json.load(file)

            if isinstance(records, list):
                return records

            return []

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


# ============================================================
# SAVE AUDIT RECORD
# ============================================================

def save_audit_record(
    client_id,
    risk_level,
    human_review_required,
    allowed_count,
    restricted_count
):

    initialize_audit_file()

    records = get_audit_records()

    record = {

        "audit_id": (
            f"AUDIT-{len(records) + 1:04d}"
        ),

        "timestamp": (
            datetime.now().isoformat(
                timespec="seconds"
            )
        ),

        "client_id": client_id,

        "event": "Safe Handover Generated",

        "risk_level": risk_level,

        "human_review_required": (
            human_review_required
        ),

        "allowed_information": (
            allowed_count
        ),

        "restricted_information": (
            restricted_count
        ),

        "status": "Completed",

    }

    records.insert(
        0,
        record
    )

    with open(
        AUDIT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4
        )

    return record