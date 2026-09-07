from app.services.case_service import build_case_context
from app.services.handover_service import (
    generate_safe_handover,
)


def print_separator():
    print("\n")
    print("=" * 65)
    print("\n")


def display_handover(handover):

    print("CURRENT CONCERN")
    print("-" * 40)
    print(handover.current_concern)


    print("\nRELEVANT INFORMATION")
    print("-" * 40)

    if handover.relevant_information:

        for item in handover.relevant_information:

            print(f"✓ {item}")

    else:

        print("None")


    print("\nRESTRICTED INFORMATION")
    print("-" * 40)

    if handover.restricted_information:

        for item in handover.restricted_information:

            print(f"🔒 {item}")

    else:

        print("None")


    print("\nCLIENT GOALS")
    print("-" * 40)

    for goal in handover.client_goals:

        print(f"• {goal}")


    print("\nPENDING ACTIONS")
    print("-" * 40)

    for action in handover.pending_actions:

        print(f"• {action}")


    print("\nRISK ASSESSMENT")
    print("-" * 40)

    print(
        "Risk Level:",
        handover.risk_assessment.level.value,
    )

    print(
        "Human Review:",
        handover.human_review_required,
    )


    print("\nESCALATION GUIDANCE")
    print("-" * 40)

    print(handover.escalation_message)


def run_journey(
    client_id,
    journey_title,
):

    print_separator()

    print(journey_title)

    print_separator()


    # ============================================
    # HUMAN REVIEW POINT 1
    # Original session is recorded
    # ============================================

    print(
        "STEP 1: SESSION INFORMATION AVAILABLE"
    )


    case = build_case_context(
        client_id
    )


    print(
        "Human review point: "
        "Counsellor records and verifies "
        "the original session information."
    )


    # ============================================
    # AUTOMATED HANDOVER GENERATION
    # ============================================

    print(
        "\nSTEP 2: AUTOMATED EXTRACTION "
        "AND CONSENT FILTERING"
    )


    handover = (
        generate_safe_handover(
            case
        )
    )


    # ============================================
    # HUMAN REVIEW POINT 2
    # ============================================

    print(
        "\nSTEP 3: HANDOVER REVIEW DECISION"
    )


    if handover.human_review_required:

        print(
            "⚠ HUMAN REVIEW REQUIRED"
        )

        print(
            "A qualified professional must "
            "review the original session "
            "information before relying on "
            "the handover."
        )

    else:

        print(
            "✓ No automatic review flag."
        )

        print(
            "The receiving professional "
            "continues with normal "
            "professional review."
        )


    # ============================================
    # FINAL HANDOVER
    # ============================================

    print(
        "\nSTEP 4: GENERATED CONTINUITY HANDOVER"
    )


    display_handover(
        handover
    )


def main():

    # =================================================
    # JOURNEY 1
    # =================================================

    run_journey(

        client_id="C003",

        journey_title=(
            "CLIENT JOURNEY 1: "
            "NORMAL EXAMINATION STRESS"
        ),
    )


    # =================================================
    # JOURNEY 2
    # =================================================

    run_journey(

        client_id="C007",

        journey_title=(
            "CLIENT JOURNEY 2: "
            "URGENT SAFETY CONCERN"
        ),
    )


if __name__ == "__main__":

    main()