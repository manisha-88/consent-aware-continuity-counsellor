import json

from app.llm.client import generate_response
from app.llm.prompts import load_extraction_prompt
from app.models import ExtractionResult


def extract_with_llm(
    session_summary: str,
) -> ExtractionResult:

    system_prompt = load_extraction_prompt()

    response = generate_response(
        system_prompt=system_prompt,
        user_prompt=session_summary,
    )

    try:
        data = json.loads(response)

    except json.JSONDecodeError as exc:
        print(f"\n[LLM PARSE ERROR] Raw response from Ollama:\n{response}\n")
        raise ValueError(
            "LLM returned invalid JSON."
        ) from exc

    return ExtractionResult.model_validate(data)