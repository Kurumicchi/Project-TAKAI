import providers.ollama as ollama
# import providers.gemini as gemini
# import providers.anthropic as anthropic

# from audio.stt import listen
# from audio.tts import speak

PROVIDER = "ollama"


def get_reply(user_input):
    if PROVIDER == "ollama":
        return ollama.get_reply(user_input)
    """
    if PROVIDER == "gemini":
        return gemini.get_reply(user_input)

    if PROVIDER == "anthropic":
        return anthropic.get_reply(user_input)
    """
    raise ValueError(f"Unknown provider: {PROVIDER}")


def main():
    print(f"TAKAI is using {PROVIDER}.")

    while True:
        user_input = input("You: ")

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("TAKAI:", get_reply(user_input))


if __name__ == "__main__":
    main()