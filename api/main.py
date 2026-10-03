from pathlib import Path
from datetime import datetime
import json

import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.case_service import build_case_context
from app.services.handover_service import generate_safe_handover


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Consent-Aware Continuity Counsellor API",
    description=(
        "Backend API for the Consent-Aware Continuity "
        "Counsellor system."
    ),
    version="2.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "synthetic"

AUDIT_FILE = DATA_DIR / "audit_history.jsonl"


# ============================================================
# HELPER - LOAD CSV
# ============================================================

def load_csv(filename: str) -> pd.DataFrame:

    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}"
        )

    return pd.read_csv(path)


# ============================================================
# HELPER - SAVE AUDIT RECORD
# ============================================================

def save_audit_record(
    client_id: str,
    action: str,
    status: str = "completed",
):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    record = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "client_id": client_id,
        "action": action,
        "status": status,
        "description": (
            "Consent-aware counselling session "
            "processed for handover."
        ),
    }

    with open(
        AUDIT_FILE,
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(record)
            + "\n"
        )


# ============================================================
# HELPER - LOAD AUDIT RECORDS
# ============================================================

def load_audit_records():

    if not AUDIT_FILE.exists():
        return []

    records = []

    try:

        with open(
            AUDIT_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:

                    records.append(
                        json.loads(line)
                    )

                except json.JSONDecodeError:
                    continue

    except Exception:
        return []

    # newest first
    records.reverse()

    return records


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "application": (
            "Consent-Aware Continuity Counsellor"
        ),
        "version": "2.0.0",
    }


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "api": "running",
    }


# ============================================================
# CLIENTS
# ============================================================

@app.get("/api/clients")
def get_clients():

    try:

        clients = load_csv(
            "clients.csv"
        )

        records = clients.to_dict(
            orient="records"
        )

        return {
            "clients": records,
            "total": len(records),
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# CASE INFORMATION
# ============================================================

@app.get("/api/cases/{client_id}")
def get_case(client_id: str):

    try:

        case = build_case_context(
            client_id
        )

        return {
            "client_id": client_id,

            "session": {
                "session_id": (
                    case.session.session_id
                ),

                "client_id": (
                    case.session.client_id
                ),

                "session_date": str(
                    case.session.session_date
                ),

                "session_summary": (
                    case.session.session_summary
                ),
            },

            "goals": case.goals,

            "consent_choices": [
                {
                    "category": choice.category,
                    "status": choice.status.value,
                }

                for choice in case.consent_choices
            ],

            "pending_actions": (
                case.pending_actions
            ),
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# GENERATE SAFE HANDOVER
# ============================================================

@app.get("/api/handover/{client_id}")
def generate_handover(
    client_id: str
):

    try:

        # Build case
        case = build_case_context(
            client_id
        )

        # Generate safe handover
        handover = generate_safe_handover(
            case
        )

        # Save audit record
        save_audit_record(
            client_id=client_id,
            action="Handover Generated",
            status="completed",
        )

        return {
            "client_id": client_id,

            "current_concern": (
                handover.current_concern
            ),

            "client_goals": (
                handover.client_goals
            ),

            "relevant_information": (
                handover.relevant_information
            ),

            "pending_actions": (
                handover.pending_actions
            ),

            "restricted_information": (
                handover.restricted_information
            ),

            "risk": {
                "level": (
                    handover
                    .risk_assessment
                    .level
                    .value
                ),

                "reason": (
                    handover
                    .risk_assessment
                    .reason
                ),

                "human_review_required": (
                    handover
                    .risk_assessment
                    .human_review_required
                ),

                "escalation_required": (
                    handover
                    .risk_assessment
                    .escalation_required
                ),
            },

            "escalation_message": (
                handover.escalation_message
            ),

            "human_review_required": (
                handover.human_review_required
            ),
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# DASHBOARD
#
# IMPORTANT:
# Do NOT generate an LLM handover for every client here.
#
# The previous implementation did this:
#
#   build_case_context()
#   generate_safe_handover()
#
# for every client.
#
# That caused the dashboard to remain on:
# "Loading dashboard..."
#
# This endpoint only loads CSV data and returns quickly.
# ============================================================

@app.get("/api/dashboard")
def get_dashboard():

    try:

        # ----------------------------------------------------
        # Load datasets
        # ----------------------------------------------------

        clients = load_csv(
            "clients.csv"
        )

        sessions = load_csv(
            "sessions.csv"
        )

        consent = load_csv(
            "consent_choices.csv"
        )

        # ----------------------------------------------------
        # Basic counts
        # ----------------------------------------------------

        total_clients = len(
            clients
        )

        total_sessions = len(
            sessions
        )

        # ----------------------------------------------------
        # Consent statistics
        # ----------------------------------------------------

        allowed_information = 0

        restricted_information = 0

        unknown_information = 0

        if "status" in consent.columns:

            allowed_information = len(
                consent[
                    consent["status"]
                    .astype(str)
                    .str.lower()
                    == "allowed"
                ]
            )

            restricted_information = len(
                consent[
                    consent["status"]
                    .astype(str)
                    .str.lower()
                    == "restricted"
                ]
            )

            unknown_information = len(
                consent[
                    consent["status"]
                    .astype(str)
                    .str.lower()
                    == "unknown"
                ]
            )

        # ----------------------------------------------------
        # Risk distribution
        #
        # Do not call the LLM here.
        #
        # Risk is initially shown as zero until a handover
        # is actually generated.
        #
        # This makes dashboard loading instant.
        # ----------------------------------------------------

        risk_distribution = {
            "low": 0,
            "ambiguous": 0,
            "urgent": 0,
        }

        review_required = 0

        # ----------------------------------------------------
        # Read previously generated audit records
        # ----------------------------------------------------

        audit_records = load_audit_records()

        # ----------------------------------------------------
        # Dashboard can report generated handover activity.
        # ----------------------------------------------------

        generated_handover_count = len(
            [
                record
                for record in audit_records
                if record.get("action")
                == "Handover Generated"
            ]
        )

        # ----------------------------------------------------
        # Return dashboard
        # ----------------------------------------------------

        return {

            "total_clients": (
                total_clients
            ),

            "total_sessions": (
                total_sessions
            ),

            "allowed_information": (
                allowed_information
            ),

            "restricted_information": (
                restricted_information
            ),

            "unknown_information": (
                unknown_information
            ),

            "risk_distribution": (
                risk_distribution
            ),

            "review_required": (
                review_required
            ),

            "no_review_required": (
                total_clients
                - review_required
            ),

            "generated_handovers": (
                generated_handover_count
            ),

            "audit_records": (
                len(audit_records)
            ),
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# AUDIT HISTORY
# ============================================================

@app.get("/api/audit")
def get_audit_history():

    try:

        records = load_audit_records()

        return {
            "records": records,
            "total": len(records),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# AUDIT HISTORY ALIAS
#
# Some frontend versions may use:
# /api/audit-history
#
# Keep both endpoints so the frontend does not break.
# ============================================================

@app.get("/api/audit-history")
def get_audit_history_alias():

    try:

        records = load_audit_records()

        return {
            "records": records,
            "total": len(records),
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# CREATE TEST / SESSION AUDIT RECORD
#
# This is useful if the frontend wants to explicitly
# record that a session was viewed.
# ============================================================

@app.post("/api/audit/session/{client_id}")
def record_session_audit(
    client_id: str
):

    try:

        # Verify that client exists
        clients = load_csv(
            "clients.csv"
        )

        client_ids = (
            clients["client_id"]
            .astype(str)
            .tolist()
        )

        if str(client_id) not in client_ids:

            raise HTTPException(
                status_code=404,
                detail=(
                    f"Client '{client_id}' "
                    "not found."
                ),
            )

        save_audit_record(
            client_id=client_id,
            action="Session Recorded",
            status="completed",
        )

        return {
            "status": "success",
            "message": (
                "Session audit record created."
            ),
            "client_id": client_id,
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
def api_information():

    return {
        "application": (
            "Consent-Aware Continuity Counsellor"
        ),

        "version": "2.0.0",

        "endpoints": [
            "/",
            "/api",
            "/api/health",
            "/api/clients",
            "/api/cases/{client_id}",
            "/api/handover/{client_id}",
            "/api/dashboard",
            "/api/audit",
            "/api/audit-history",
            "/api/audit/session/{client_id}",
        ],
    }