import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "data" / "database"

DATABASE_PATH = (
    DATABASE_DIR / "continuity.db"
)


def get_connection():

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            client_id TEXT NOT NULL,

            risk_level TEXT NOT NULL,

            human_review_required INTEGER NOT NULL,

            decision TEXT NOT NULL,

            reviewer_notes TEXT,

            final_handover TEXT,

            restricted_information TEXT,

            reviewed_at TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()