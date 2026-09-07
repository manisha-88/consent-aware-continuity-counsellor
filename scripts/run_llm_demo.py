from app.llm.extractor import extract_with_llm


def main():
    session_summary = (
        "Student reports exam stress and mentions conflict "
        "with family regarding grades. Student also reports "
        "difficulty sleeping."
    )

    result = extract_with_llm(session_summary)

    print("\nLLM EXTRACTION RESULT\n")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()