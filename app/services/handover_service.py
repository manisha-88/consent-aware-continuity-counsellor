from app.models import (
    CaseContext,
    HandoverSummary,
)

from app.services.safe_extraction_service import (
    safe_extract_information,
)

from app.services.consent_service import (
    get_restricted_categories,
    find_missing_consent_categories,
)

from app.services.filter_service import (
    filter_information,
)

from app.services.risk_service import (
    assess_risk,
)

from app.rules.escalation_rules import (
    get_escalation_message,
)

from app.services.extraction_validation_service import (
    find_possible_omissions,
    find_possible_hallucinations,
)


def generate_safe_handover(
    case: CaseContext,
) -> HandoverSummary:

    # =====================================================
    # 1. SAFE EXTRACTION
    # =====================================================

    extraction, extraction_failure = (
        safe_extract_information(
            case.session.session_summary
        )
    )


    # =====================================================
    # 2. VALIDATE EXTRACTION
    # =====================================================

    possible_omissions = (
        find_possible_omissions(
            case.session.session_summary,
            extraction.information,
        )
    )


    possible_hallucinations = (
        find_possible_hallucinations(
            case.session.session_summary,
            extraction.information,
        )
    )


    # =====================================================
    # 3. CHECK FOR MISSING CONSENT
    # =====================================================

    missing_consent_categories = (
        find_missing_consent_categories(
            case,
            extraction.information,
        )
    )


    # =====================================================
    # 4. APPLY CONSENT FILTER
    # =====================================================

    allowed, restricted = (
        filter_information(
            case,
            extraction.information,
        )
    )


    # =====================================================
    # 5. INDEPENDENT RISK ASSESSMENT
    # =====================================================

    risk_assessment = assess_risk(
        case
    )


    # =====================================================
    # 6. BUILD RELEVANT INFORMATION
    # =====================================================

    relevant_information = [
        item.content
        for item in allowed
    ]


    restricted_information = [
        item.category.value
        for item in restricted
    ]


    # =====================================================
    # 7. CURRENT CONCERN
    # =====================================================

    if relevant_information:

        current_concern = " ".join(
            relevant_information
        )

    else:

        current_concern = (
            "No information is available "
            "for handover under the current "
            "consent settings."
        )


    # =====================================================
    # 8. ESCALATION GUIDANCE
    # =====================================================

    escalation_message = (
        get_escalation_message(
            risk_assessment.level
        )
    )


    # =====================================================
    # 9. OPERATIONAL FAILURE HANDLING
    # =====================================================

    operational_warnings = []


    # LLM FAILURE

    if extraction_failure:

        operational_warnings.append(
            extraction_failure
        )


    # MISSING CONSENT

    if missing_consent_categories:

        operational_warnings.append(
            "Consent information is missing "
            "for one or more extracted "
            "categories. Information without "
            "explicit permission was excluded."
        )


    # POSSIBLE OMISSIONS

    if possible_omissions:

        operational_warnings.append(
            "Possible information omission "
            "detected during automated "
            "extraction."
        )


    # POSSIBLE HALLUCINATIONS

    if possible_hallucinations:

        operational_warnings.append(
            "Possible unsupported information "
            "detected during automated "
            "extraction."
        )


    # =====================================================
    # 10. HUMAN REVIEW DECISION
    # =====================================================

    human_review_required = (

        risk_assessment.human_review_required

        or extraction_failure is not None

        or len(
            missing_consent_categories
        ) > 0

        or len(
            possible_omissions
        ) > 0

        or len(
            possible_hallucinations
        ) > 0
    )


    # =====================================================
    # 11. ADD FAILURE GUIDANCE
    # =====================================================

    if operational_warnings:

        warning_text = " ".join(
            operational_warnings
        )


        escalation_message = (
            f"{escalation_message} "
            f"Operational safeguard: "
            f"{warning_text} "
            f"Human review is required "
            f"before using this handover."
        )


    # =====================================================
    # 12. RETURN HANDOVER
    # =====================================================

    return HandoverSummary(

        current_concern=(
            current_concern
        ),

        client_goals=(
            case.goals
        ),

        relevant_information=(
            relevant_information
        ),

        pending_actions=(
            case.pending_actions
        ),

        restricted_information=(
            restricted_information
        ),

        risk_assessment=(
            risk_assessment
        ),

        escalation_message=(
            escalation_message
        ),

        human_review_required=(
            human_review_required
        ),
    )