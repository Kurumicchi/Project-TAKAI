import sys

import providers.ollama as ollama

from audio.stt import listen
from audio.tts import speak

from memory.chat_history import add_message, load_history

# Konsol Windows guna cp1252. Kalau model hantar emoji, print() akan crash
# dengan UnicodeEncodeError, jadi paksa stdout jadi UTF-8.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROVIDER = "ollama"

def get_reply(history):
    if PROVIDER == "ollama":
        return ollama.get_reply(history)

    raise ValueError(f"Unknown provider: {PROVIDER}")

def main():
    print(f"TAKAI is using {PROVIDER}.")

    while True:
        user_input = listen()

        if not user_input:
            continue

        if user_input.strip().lower() == "dadah":
            print("Goodbye!")
            break

        add_message("user", user_input)

        history = load_history()
        response = get_reply(history)

        add_message("assistant", response)

        print("TAKAI:", response)
        speak(response)

if __name__ == "__main__":
    main()
