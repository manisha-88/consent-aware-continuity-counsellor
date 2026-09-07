import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]


COMPARISON_FILE = (
    BASE_DIR
    / "evaluation"
    / "results"
    / "comparison.csv"
)


def load_results():

    with open(
        COMPARISON_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(
            file
        )

        return list(reader)


def analyze_result(result):

    errors = []


    # -----------------------------------------
    # CONSENT ERROR
    # -----------------------------------------

    if (
        result[
            "consent_violation"
        ].lower()
        == "true"
    ):

        errors.append(
            "Consent violation: restricted "
            "information appeared in the "
            "handover."
        )


    # -----------------------------------------
    # RISK ERROR
    # -----------------------------------------

    if (
        result[
            "predicted_risk"
        ]
        !=
        result[
            "expected_risk"
        ]
    ):

        errors.append(
            "Risk classification error: "
            f"expected "
            f"{result['expected_risk']} "
            f"but predicted "
            f"{result['predicted_risk']}."
        )


    # -----------------------------------------
    # HUMAN REVIEW ERROR
    # -----------------------------------------

    predicted_review = (
        result[
            "predicted_human_review"
        ].lower()
        == "true"
    )


    expected_review = (
        result[
            "expected_human_review"
        ].lower()
        == "true"
    )


    if (
        predicted_review
        !=
        expected_review
    ):

        errors.append(
            "Human review decision error: "
            f"expected "
            f"{expected_review} "
            f"but predicted "
            f"{predicted_review}."
        )


    return errors


def explain_cause(
    result,
    errors,
):

    system = result["system"]


    if not errors:

        return (
            "No error detected for this "
            "synthetic test case."
        )


    if system == "baseline":

        causes = []

        for error in errors:

            if (
                "Consent violation"
                in error
            ):

                causes.append(
                    "Baseline does not apply "
                    "consent filtering."
                )

            elif (
                "Risk classification"
                in error
            ):

                causes.append(
                    "Baseline has no automated "
                    "risk classification."
                )

            elif (
                "Human review"
                in error
            ):

                causes.append(
                    "Baseline has no human "
                    "review escalation rule."
                )

        return " ".join(causes)


    if system == "prototype":

        return (
            "Prototype behavior should be "
            "reviewed because the automated "
            "pipeline did not match the "
            "expected synthetic outcome."
        )


    return (
        "Unknown system."
    )


def main():

    results = load_results()


    print("\n")

    print("=" * 70)

    print(
        "ERROR ANALYSIS"
    )

    print("=" * 70)


    for result in results:

        errors = analyze_result(
            result
        )


        cause = explain_cause(
            result,
            errors,
        )


        print("\n")

        print(
            f"Case: "
            f"{result['case_id']}"
        )

        print(
            f"System: "
            f"{result['system']}"
        )


        if errors:

            print(
                "\nErrors:"
            )

            for error in errors:

                print(
                    f"- {error}"
                )

        else:

            print(
                "\nErrors: None"
            )


        print(
            "\nAnalysis:"
        )

        print(
            cause
        )


if __name__ == "__main__":
    main()