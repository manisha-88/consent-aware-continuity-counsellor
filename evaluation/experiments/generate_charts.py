import json
from pathlib import Path

import matplotlib.pyplot as plt


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


METRICS_FILE = (
    BASE_DIR
    / "evaluation"
    / "results"
    / "metrics.json"
)


CHARTS_DIR = (
    BASE_DIR
    / "evaluation"
    / "results"
    / "charts"
)


# =========================================================
# LOAD METRICS
# =========================================================

def load_metrics():

    with open(
        METRICS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# =========================================================
# CREATE BAR CHART
# =========================================================

def create_chart(
    title,
    metric_name,
    baseline_value,
    prototype_value,
    filename,
):

    systems = [
        "Baseline",
        "Prototype",
    ]

    values = [
        baseline_value,
        prototype_value,
    ]


    plt.figure(
        figsize=(7, 5)
    )

    bars = plt.bar(
        systems,
        values,
    )


    plt.title(title)

    plt.ylabel(
        "Percentage (%)"
    )

    plt.ylim(
        0,
        110,
    )


    # Add values above bars
    for bar, value in zip(
        bars,
        values,
    ):

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 2,
            f"{value:.1f}%",
            ha="center",
        )


    plt.tight_layout()


    output_file = (
        CHARTS_DIR
        / filename
    )


    plt.savefig(
        output_file
    )


    plt.close()


    print(
        f"Chart saved: "
        f"{output_file}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    metrics = load_metrics()


    CHARTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    baseline = (
        metrics["baseline"]
    )


    prototype = (
        metrics["prototype"]
    )


    # ---------------------------------------------
    # CONSENT VIOLATION RATE
    # ---------------------------------------------

    create_chart(
        title=(
            "Consent Violation Rate"
        ),

        metric_name=(
            "consent_violation_rate"
        ),

        baseline_value=(
            baseline[
                "consent_violation_rate"
            ]
        ),

        prototype_value=(
            prototype[
                "consent_violation_rate"
            ]
        ),

        filename=(
            "consent_violation_rate.png"
        ),
    )


    # ---------------------------------------------
    # RISK ACCURACY
    # ---------------------------------------------

    create_chart(
        title=(
            "Risk Classification Accuracy"
        ),

        metric_name=(
            "risk_accuracy"
        ),

        baseline_value=(
            baseline[
                "risk_accuracy"
            ]
        ),

        prototype_value=(
            prototype[
                "risk_accuracy"
            ]
        ),

        filename=(
            "risk_accuracy.png"
        ),
    )


    # ---------------------------------------------
    # HUMAN REVIEW ACCURACY
    # ---------------------------------------------

    create_chart(
        title=(
            "Human Review Decision Accuracy"
        ),

        metric_name=(
            "human_review_accuracy"
        ),

        baseline_value=(
            baseline[
                "human_review_accuracy"
            ]
        ),

        prototype_value=(
            prototype[
                "human_review_accuracy"
            ]
        ),

        filename=(
            "human_review_accuracy.png"
        ),
    )


    print(
        "\nAll charts generated successfully."
    )


if __name__ == "__main__":
    main()