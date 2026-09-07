import json
from datetime import date
from pathlib import Path
from unittest.mock import patch

from app.models import (
    CaseContext,
    ConsentChoice,
    ConsentStatus,
    ExtractionResult,
    Session,
)

from app.services.handover_service import (
    generate_safe_handover,
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]


FAILURE_CASES_FILE = (
    BASE_DIR
    / "data"
    / "test_cases"
    / "failure_cases.json"
)


# =====================================================
# LOAD FAILURE CASES
# =====================================================

def load_failure_cases():

    with open(
        FAILURE_CASES_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# =====================================================
# CREATE CASE
# =====================================================

def create_case(
    case_id,
    session_summary,
    failure_type,
):

    consent_choices = []


    # ---------------------------------------------
    # NORMAL CONSENT
    # ---------------------------------------------

    if failure_type != "missing_consent":

        consent_choices = [

            ConsentChoice(
                category="exam_stress",
                status=ConsentStatus.ALLOWED,
            ),

            ConsentChoice(
                category="sleep_difficulty",
                status=ConsentStatus.ALLOWED,
            ),

            ConsentChoice(
                category="family_information",
                status=ConsentStatus.RESTRICTED,
            ),

            ConsentChoice(
                category="ambiguous_statement",
                status=ConsentStatus.RESTRICTED,
            ),
        ]


    # ---------------------------------------------
    # SESSION
    # ---------------------------------------------

    session = Session(

        session_id=(
            f"{case_id}_SESSION"
        ),

        client_id=case_id,

        session_date=date.today(),

        session_summary=session_summary,
    )


    # ---------------------------------------------
    # CASE CONTEXT
    # ---------------------------------------------

    case = CaseContext(

        session=session,

        goals=[
            "Provide appropriate support"
        ],

        consent_choices=consent_choices,

        pending_actions=[
            "Professional follow-up"
        ],
    )


    return case


# =====================================================
# FAILURE TEST: LLM UNAVAILABLE
# =====================================================

def test_llm_unavailable(case):

    with patch(
        "app.services.safe_extraction_service.extract_with_llm"
    ) as mock_llm:

        mock_llm.side_effect = (
            ConnectionError(
                "Ollama service unavailable"
            )
        )

        return generate_safe_handover(
            case
        )


# =====================================================
# FAILURE TEST: EMPTY LLM EXTRACTION
# =====================================================

def test_empty_extraction(case):

    with patch(
        "app.services.safe_extraction_service.extract_with_llm"
    ) as mock_llm:

        mock_llm.return_value = (
            ExtractionResult(
                information=[]
            )
        )

        return generate_safe_handover(
            case
        )


# =====================================================
# NORMAL FAILURE CASE
# =====================================================

def test_normal_failure_case(case):

    return generate_safe_handover(
        case
    )


# =====================================================
# RUN ONE FAILURE TEST
# =====================================================

def run_test(failure_case):

    failure_type = (
        failure_case[
            "failure_type"
        ]
    )


    case = create_case(

        case_id=(
            failure_case[
                "case_id"
            ]
        ),

        session_summary=(
            failure_case[
                "session_summary"
            ]
        ),

        failure_type=failure_type,
    )


    # ---------------------------------------------
    # RUN FAILURE SCENARIO
    # ---------------------------------------------

    try:

        # -----------------------------------------
        # F001
        # -----------------------------------------

        if (
            failure_type
            == "llm_unavailable"
        ):

            handover = (
                test_llm_unavailable(
                    case
                )
            )


        # -----------------------------------------
        # F002
        # -----------------------------------------

        elif (
            failure_type
            == "empty_extraction"
        ):

            handover = (
                test_empty_extraction(
                    case
                )
            )


        # -----------------------------------------
        # OTHER CASES
        # -----------------------------------------

        else:

            handover = (
                test_normal_failure_case(
                    case
                )
            )


        success = True

        error_message = None


    except Exception as error:

        success = False

        handover = None

        error_message = str(
            error
        )


    # ---------------------------------------------
    # DISPLAY CASE INFORMATION
    # ---------------------------------------------

    print("\n")

    print(
        "=" * 60
    )

    print(
        f"CASE: "
        f"{failure_case['case_id']}"
    )

    print(
        f"DESCRIPTION: "
        f"{failure_case['description']}"
    )

    print(
        f"FAILURE TYPE: "
        f"{failure_type}"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # SYSTEM FAILED COMPLETELY
    # ---------------------------------------------

    if not success:

        print(
            "\nSYSTEM FAILURE:"
        )

        print(
            error_message
        )


        print(
            "\nRESULT:"
        )

        print(
            "The system could not safely "
            "complete the handover for "
            "this failure state."
        )

        return


    # ---------------------------------------------
    # RISK
    # ---------------------------------------------

    print(
        "\nRisk:"
    )

    print(
        handover
        .risk_assessment
        .level
        .value
    )


    # ---------------------------------------------
    # HUMAN REVIEW
    # ---------------------------------------------

    print(
        "\nHuman Review Required:"
    )

    print(
        handover
        .human_review_required
    )


    # ---------------------------------------------
    # RELEVANT INFORMATION
    # ---------------------------------------------

    print(
        "\nRelevant Information:"
    )


    if (
        handover
        .relevant_information
    ):

        for item in (
            handover
            .relevant_information
        ):

            print(
                f"- {item}"
            )

    else:

        print(
            "- None"
        )


    # ---------------------------------------------
    # RESTRICTED INFORMATION
    # ---------------------------------------------

    print(
        "\nRestricted Information:"
    )


    if (
        handover
        .restricted_information
    ):

        for item in (
            handover
            .restricted_information
        ):

            print(
                f"- {item}"
            )

    else:

        print(
            "- None"
        )


    # ---------------------------------------------
    # ESCALATION GUIDANCE
    # ---------------------------------------------

    print(
        "\nEscalation Guidance:"
    )

    print(
        handover
        .escalation_message
    )


# =====================================================
# MAIN
# =====================================================

def main():

    failure_cases = (
        load_failure_cases()
    )


    print("\n")

    print(
        "=" * 60
    )

    print(
        "OPERATIONAL FAILURE STATE TESTING"
    )

    print(
        "=" * 60
    )


    # ---------------------------------------------
    # RUN ALL CASES
    # ---------------------------------------------

    for failure_case in failure_cases:

        run_test(
            failure_case
        )


    print("\n")

    print(
        "=" * 60
    )

    print(
        "FAILURE-STATE TESTING COMPLETED"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    main()