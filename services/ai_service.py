import os
import requests

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def rewrite_message(user_input: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You help rewrite messages into professional, warm, and polite "
                    "workplace gratitude messages. "
                    "If the input is an instruction, write the message. "
                    "If it is a rough draft, improve it. "
                    "Return only the final message."
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "temperature": 0.4,
        "max_tokens": 150
    }

    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
