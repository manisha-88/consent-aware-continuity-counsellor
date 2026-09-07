from app.services.case_service import build_case_context
from app.services.handover_service import generate_safe_handover


def main():

    client_id = "C003"

    case = build_case_context(client_id)

    handover = generate_safe_handover(case)

    print("\n====================================")
    print("SAFE CONTINUITY HANDOVER")
    print("====================================")

    print("\nCurrent Concern:")
    print(handover.current_concern)

    print("\nClient Goals:")
    for goal in handover.client_goals:
        print(f"• {goal}")

    print("\nRelevant Information:")
    for information in handover.relevant_information:
        print(f"• {information}")

    print("\nPending Actions:")
    for action in handover.pending_actions:
        print(f"• {action}")

    print("\nRestricted Information:")
    for category in handover.restricted_information:
        print(f"• {category}")

    print("\nRisk:")
    print(handover.risk_assessment.level.value)

    print(
        "\nHuman Review Required:",
        handover.human_review_required,
    )

    print("\nEscalation:")
    print(handover.escalation_message)


if __name__ == "__main__":
    main()