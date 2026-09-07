def calculate_metrics(results: list):
    """
    Calculate evaluation metrics from
    baseline or prototype results.
    """

    total_cases = len(results)

    consent_violations = 0
    correct_risk_predictions = 0
    correct_human_review_predictions = 0
    allowed_information_found = 0
    allowed_information_expected = 0

    for result in results:

        # Consent violations
        if result["consent_violation"]:
            consent_violations += 1

        # Risk accuracy
        if (
            result["predicted_risk"]
            == result["expected_risk"]
        ):
            correct_risk_predictions += 1

        # Human review accuracy
        if (
            result["predicted_human_review"]
            == result["expected_human_review"]
        ):
            correct_human_review_predictions += 1

        # Allowed information retention
        predicted_categories = set(
            result["predicted_categories"]
        )

        expected_allowed = set(
            result["expected_allowed"]
        )

        allowed_information_found += len(
            predicted_categories
            & expected_allowed
        )

        allowed_information_expected += len(
            expected_allowed
        )

    # Prevent division by zero
    if total_cases == 0:
        return {}

    if allowed_information_expected == 0:
        retention_rate = 0
    else:
        retention_rate = (
            allowed_information_found
            / allowed_information_expected
        ) * 100

    return {
        "total_cases": total_cases,
        "consent_violations": consent_violations,
        "consent_violation_rate": (
            consent_violations / total_cases
        ) * 100,
        "risk_accuracy": (
            correct_risk_predictions / total_cases
        ) * 100,
        "human_review_accuracy": (
            correct_human_review_predictions / total_cases
        ) * 100,
        "allowed_information_retention": retention_rate,
    }