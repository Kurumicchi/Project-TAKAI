import requests


MODEL = "qwen3:8b"
URL = "http://localhost:11434/api/chat"

with open("TAKAI_SYSTEM.md", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

def get_reply(history):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    response = requests.post(
        URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.5
            }
        },
        timeout=300
    )

    response.raise_for_status()

    content = response.json()["message"]["content"]

    # Buang bahagian "berfikir" model, ambil jawapan selepas </think>
    if "</think>" in content:
        content = content.split("</think>")[-1]

    return content.strip()
