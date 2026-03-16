import requests

GROQ_API_KEY = "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"

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def rewrite_text(text):
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Rewrite the user's text into a clear, professional, "
                    "and polite LinkedIn-style message. Do not add extra information."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.3,
        "max_tokens": 120
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    text = "hey team i was late today because traffic was very bad"
    print(rewrite_text(text))
