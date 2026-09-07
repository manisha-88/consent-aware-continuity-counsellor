from app.services.case_service import build_case_context
from app.llm.extractor import extract_with_llm
from app.services.extraction_validation_service import (
    find_possible_omissions,
    find_possible_hallucinations,
)


def main():

    case = build_case_context("C003")

    print("\n========== ORIGINAL SESSION ==========")
    print(case.session.session_summary)

    extraction = extract_with_llm(
        case.session.session_summary
    )

    print("\n========== LLM EXTRACTION ==========")

    for item in extraction.information:
        print(
            f"{item.category.value}: {item.content}"
        )

    omissions = find_possible_omissions(
        case.session.session_summary,
        extraction.information,
    )

    hallucinations = find_possible_hallucinations(
        case.session.session_summary,
        extraction.information,
    )

    print("\n========== POSSIBLE OMISSIONS ==========")

    for item in omissions:
        print(item.value)

    print("\n========== POSSIBLE HALLUCINATIONS ==========")

    for item in hallucinations:
        print(
            f"{item.category.value}: "
            f"{item.content}"
        )


if __name__ == "__main__":
    main()