import ollama


MODEL_NAME = "qwen2.5:3b"


def generate_response(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response["message"]["content"]