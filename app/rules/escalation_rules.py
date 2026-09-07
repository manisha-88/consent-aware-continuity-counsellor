from app.models.risk import RiskLevel


def get_escalation_message(level: RiskLevel) -> str:
    if level == RiskLevel.URGENT:
        return (
            "URGENT HUMAN REVIEW REQUIRED. "
            "Do not rely solely on the automated summary. "
            "Review the original session information and follow "
            "the university counselling centre's established "
            "safety and escalation procedure."
        )

    if level == RiskLevel.AMBIGUOUS:
        return (
            "HUMAN REVIEW REQUIRED. "
            "The available information is ambiguous. "
            "Review the original session information before "
            "continuing the handover."
        )

    return (
        "No escalation indicated by the automated screening. "
        "Continue normal professional review."
    )