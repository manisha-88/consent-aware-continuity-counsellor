import csv
import json
from pathlib import Path

from evaluation.baseline.baseline_summarizer import (
    generate_baseline_handover,
)

from evaluation.experiments.metrics import (
    calculate_metrics,
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

TEST_CASES_FILE = (
    BASE_DIR
    / "data"
    / "test_cases"
    / "evaluation_cases.json"
)

RESULTS_DIR = (
    BASE_DIR
    / "evaluation"
    / "results"
)

COMPARISON_FILE = (
    RESULTS_DIR
    / "comparison.csv"
)

METRICS_FILE = (
    RESULTS_DIR
    / "metrics.json"
)


# =========================================================
# LOAD TEST CASES
# =========================================================

def load_test_cases():

    with open(
        TEST_CASES_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# =========================================================
# CATEGORY EXTRACTION
# =========================================================

def extract_categories(session_summary: str):

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

                categories.append(category)

                break

    return categories


# =========================================================
# BASELINE PIPELINE
# =========================================================

def run_baseline(case: dict):

    baseline_result = (
        generate_baseline_handover(
            session_summary=case[
                "session_summary"
            ],
            consent=case[
                "consent"
            ],
        )
    )

    predicted_categories = (
        baseline_result["categories"]
    )

    consent_violation = False

    for category in predicted_categories:

        if category in case[
            "expected_restricted"
        ]:

            consent_violation = True

    return {
        "case_id": case["case_id"],
        "system": "baseline",
        "predicted_categories": predicted_categories,
        "restricted_categories": [],
        "predicted_risk": "low",
        "expected_risk": case["expected_risk"],
        "predicted_human_review": False,
        "expected_human_review": case[
            "expected_human_review"
        ],
        "expected_allowed": case[
            "expected_allowed"
        ],
        "expected_restricted": case[
            "expected_restricted"
        ],
        "consent_violation": consent_violation,
    }


# =========================================================
# PROTOTYPE PIPELINE
# =========================================================

def run_prototype(case: dict):

    extracted_categories = extract_categories(
        case["session_summary"]
    )

    allowed_categories = []
    restricted_categories = []

    # Apply consent
    for category in extracted_categories:

        consent_status = (
            case["consent"].get(
                category,
                "restricted",
            )
        )

        if consent_status == "allowed":

            allowed_categories.append(category)

        else:

            restricted_categories.append(category)

    # Risk assessment
    if "safety_concern" in extracted_categories:

        predicted_risk = "urgent"
        human_review_required = True

    elif (
        "ambiguous_statement"
        in extracted_categories
    ):

        predicted_risk = "ambiguous"
        human_review_required = True

    else:

        predicted_risk = "low"
        human_review_required = False

    # Consent violation check
    consent_violation = False

    for category in allowed_categories:

        if category in case[
            "expected_restricted"
        ]:

            consent_violation = True

    return {
        "case_id": case["case_id"],
        "system": "prototype",
        "predicted_categories": allowed_categories,
        "restricted_categories": restricted_categories,
        "predicted_risk": predicted_risk,
        "expected_risk": case["expected_risk"],
        "predicted_human_review": (
            human_review_required
        ),
        "expected_human_review": case[
            "expected_human_review"
        ],
        "expected_allowed": case[
            "expected_allowed"
        ],
        "expected_restricted": case[
            "expected_restricted"
        ],
        "consent_violation": consent_violation,
    }


# =========================================================
# SAVE COMPARISON CSV
# =========================================================

def save_comparison(results: list):

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "case_id",
        "system",
        "predicted_categories",
        "restricted_categories",
        "predicted_risk",
        "expected_risk",
        "predicted_human_review",
        "expected_human_review",
        "consent_violation",
    ]

    with open(
        COMPARISON_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for result in results:

            row = {}

            for key in fieldnames:

                row[key] = result.get(key)

            row["predicted_categories"] = (
                ", ".join(
                    result["predicted_categories"]
                )
            )

            row["restricted_categories"] = (
                ", ".join(
                    result["restricted_categories"]
                )
            )

            writer.writerow(row)


# =========================================================
# MAIN EXPERIMENT
# =========================================================

def main():

    cases = load_test_cases()

    baseline_results = []
    prototype_results = []

    for case in cases:

        baseline_results.append(
            run_baseline(case)
        )

        prototype_results.append(
            run_prototype(case)
        )

    # Calculate metrics
    baseline_metrics = calculate_metrics(
        baseline_results
    )

    prototype_metrics = calculate_metrics(
        prototype_results
    )

    # Save comparison
    all_results = (
        baseline_results
        + prototype_results
    )

    save_comparison(all_results)

    # Save metrics
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_metrics = {
        "baseline": baseline_metrics,
        "prototype": prototype_metrics,
    }

    with open(
        METRICS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            final_metrics,
            file,
            indent=4,
        )

    # Display results
    print("\n")
    print("=" * 60)
    print("BASELINE vs PROTOTYPE EVALUATION")
    print("=" * 60)

    print("\nBASELINE METRICS")

    for key, value in (
        baseline_metrics.items()
    ):

        print(f"{key}: {value}")

    print("\nPROTOTYPE METRICS")

    for key, value in (
        prototype_metrics.items()
    ):

        print(f"{key}: {value}")

    print("\nResults saved successfully.")

    print(
        f"Comparison: {COMPARISON_FILE}"
    )

    print(
        f"Metrics: {METRICS_FILE}"
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()