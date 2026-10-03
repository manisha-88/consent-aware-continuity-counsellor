from concurrent.futures import ThreadPoolExecutor
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

    # Execute independent LLM calls concurrently
    with ThreadPoolExecutor() as executor:
        # Step 1 & 5 in parallel
        future_extraction = executor.submit(
            safe_extract_information, case.session.session_summary
        )
        future_risk = executor.submit(
            assess_risk, case
        )

        extraction, extraction_failure = future_extraction.result()
        risk_assessment = future_risk.result()

        # Step 2 validation in parallel after extraction completes
        future_omissions = executor.submit(
            find_possible_omissions,
            case.session.session_summary,
            extraction.information,
        )
        future_hallucinations = executor.submit(
            find_possible_hallucinations,
            case.session.session_summary,
            extraction.information,
        )

        possible_omissions = future_omissions.result()
        possible_hallucinations = future_hallucinations.result()

    # Step 3: Check missing consent
    missing_consent_categories = find_missing_consent_categories(
        case,
        extraction.information,
    )

    # Step 4: Apply consent filter
    allowed, restricted = filter_information(
        case,
        extraction.information,
    )

    # Step 6: Build relevant information
    relevant_information = [item.content for item in allowed]
    restricted_information = [item.category.value for item in restricted]

    # Step 7: Current concern
    if relevant_information:
        current_concern = " ".join(relevant_information)
    else:
        current_concern = (
            "No information is available for handover under the current consent settings."
        )

    # Step 8: Escalation guidance
    escalation_message = get_escalation_message(risk_assessment.level)

    # Step 9: Operational warnings
    operational_warnings = []
    if extraction_failure:
        operational_warnings.append(extraction_failure)
    if missing_consent_categories:
        operational_warnings.append(
            "Consent information is missing for one or more extracted categories. Information without explicit permission was excluded."
        )
    if possible_omissions:
        operational_warnings.append(
            "Possible information omission detected during automated extraction."
        )
    if possible_hallucinations:
        operational_warnings.append(
            "Possible unsupported information detected during automated extraction."
        )

    # Step 10: Human review decision
    human_review_required = (
        risk_assessment.human_review_required
        or extraction_failure is not None
        or len(missing_consent_categories) > 0
        or len(possible_omissions) > 0
        or len(possible_hallucinations) > 0
    )

    # Step 11: Add warning messages
    if operational_warnings:
        warning_text = " ".join(operational_warnings)
        escalation_message = (
            f"{escalation_message} Operational safeguard: {warning_text} "
            f"Human review is required before using this handover."
        )

    # Step 12: Return summary
    return HandoverSummary(
        current_concern=current_concern,
        client_goals=case.goals,
        relevant_information=relevant_information,
        pending_actions=case.pending_actions,
        restricted_information=restricted_information,
        risk_assessment=risk_assessment,
        escalation_message=escalation_message,
        human_review_required=human_review_required,
    )