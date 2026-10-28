import providers.ollama as ollama

from audio.STT import listen

from memory.chat_history import add_message, load_history

PROVIDER = "ollama"

def get_reply(history):
    if PROVIDER == "ollama":
        return ollama.get_reply(history)

    raise ValueError(f"Unknown provider: {PROVIDER}")

def main():
    print(f"TAKAI is using {PROVIDER}.")

    while True:
        user_input = input("You: ")

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


if __name__ == "__main__":
    main()