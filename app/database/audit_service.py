from datetime import datetime

from app.database.connection import (
    get_connection,
    initialize_database,
)


def save_audit_record(
    client_id: str,
    risk_level: str,
    human_review_required: bool,
    decision: str,
    reviewer_notes: str,
    final_handover: str,
    restricted_information: list[str],
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO audit_records (

            client_id,
            risk_level,
            human_review_required,
            decision,
            reviewer_notes,
            final_handover,
            restricted_information,
            reviewed_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            client_id,
            risk_level,
            int(human_review_required),
            decision,
            reviewer_notes,
            final_handover,
            ",".join(
                restricted_information
            ),
            datetime.now().isoformat(),
        ),
    )

    connection.commit()

    connection.close()


def get_audit_records():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM audit_records
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    connection.close()

    return records