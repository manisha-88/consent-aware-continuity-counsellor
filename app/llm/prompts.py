from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROMPT_PATH = (
    PROJECT_ROOT
    / "prompts"
    / "information_extraction.txt"
)


def load_extraction_prompt() -> str:
    return PROMPT_PATH.read_text(
        encoding="utf-8"
    )