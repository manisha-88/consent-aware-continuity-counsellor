from app.database.audit_service import (
    save_audit_record,
    get_audit_records,
)


def main():

    save_audit_record(
        client_id="TEST001",
        risk_level="low",
        human_review_required=False,
        decision="approved",
        reviewer_notes="Test audit record",
        final_handover=(
            "Synthetic test handover."
        ),
        restricted_information=[
            "family_information"
        ],
    )

    records = get_audit_records()

    print("\nAUDIT RECORDS\n")

    for record in records:

        print(dict(record))


if __name__ == "__main__":
    main()