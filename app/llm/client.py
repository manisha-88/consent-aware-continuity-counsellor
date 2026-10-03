import ollama

MODEL_NAME = "qwen2.5:3b"


def generate_response(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = ollama.chat(
        model=MODEL_NAME,
        format="json",  # Forces Ollama to produce valid JSON directly
        messages=[
            {
                "role": "system",
                "content": system_prompt + "\nOutput strictly valid JSON. Do not include thinking steps or markdown backticks.",
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "num_predict": 256,  # Limits token generation to keep CPU execution fast
            "temperature": 0.1,  # Keeps output deterministic
        },
    )

    content = response["message"]["content"].strip()

    # Strip markdown backticks if present
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        content = content.rsplit("```", 1)[0].strip()

    return content