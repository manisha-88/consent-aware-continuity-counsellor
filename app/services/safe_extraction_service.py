from app.models import ExtractionResult

from app.llm.extractor import (
    extract_with_llm,
)

from app.services.fallback_extractor import (
    extract_with_fallback,
)


def safe_extract_information(
    session_summary: str,
):
    """
    Safely extract information.

    Returns:

    extraction_result
    failure_reason

    If the LLM fails, the system uses
    a rule-based fallback extractor and
    requires human review.
    """

    try:

        extraction = extract_with_llm(
            session_summary
        )


        # -----------------------------------------
        # EMPTY LLM RESPONSE
        # -----------------------------------------

        if (
            not extraction.information
        ):

            fallback_information = (
                extract_with_fallback(
                    session_summary
                )
            )


            return (
                ExtractionResult(
                    information=(
                        fallback_information
                    )
                ),
                (
                    "LLM returned no useful "
                    "information. A fallback "
                    "extraction method was used."
                ),
            )


        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        return (
            extraction,
            None,
        )


    # ---------------------------------------------
    # LLM FAILURE
    # ---------------------------------------------

    except Exception:

        fallback_information = (
            extract_with_fallback(
                session_summary
            )
        )


        return (
            ExtractionResult(
                information=(
                    fallback_information
                )
            ),
            (
                "Automated extraction was "
                "unavailable. A safe fallback "
                "method was used."
            ),
        )