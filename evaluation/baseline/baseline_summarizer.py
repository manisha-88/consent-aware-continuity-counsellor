"""
Simple baseline handover generator.

This baseline intentionally does not apply:

- consent filtering
- risk escalation
- human review rules

It represents a simple AI-assisted summarisation approach.
"""


def generate_baseline_handover(
    session_summary: str,
    consent: dict,
):
    """
    Generate a simple baseline handover.

    The baseline uses the session summary directly
    and does not remove restricted information.
    """

    categories = []

    category_keywords = {
        "exam_stress": [
            "exam",
            "examination",
            "stress",
        ],
        "sleep_difficulty": [
            "sleep",
            "sleeping",
        ],
        "family_information": [
            "family",
            "family problems",
        ],
        "safety_concern": [
            "unsafe",
            "safety concern",
            "immediate safety",
        ],
        "ambiguous_statement": [
            "unclear",
            "something may be seriously wrong",
        ],
    }

    text = session_summary.lower()

    for category, keywords in (
        category_keywords.items()
    ):

        for keyword in keywords:

            if keyword in text:

                categories.append(
                    category
                )

                break

    return {
        "handover_text": session_summary,
        "categories": categories,
        "human_review_required": False,
        "consent_filter_applied": False,
    }