import requests


MODEL = "hf.co/ge525/Qwen3.8-9B-Distill-uncensored-heretic-Q4_K_M-GGUF:Q4_K_M"
URL = "http://localhost:11434/api/chat"

with open("TAKAI_SYSTEM.md", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

def get_reply(user_input):
    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.5
            }
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["message"]["content"].strip()