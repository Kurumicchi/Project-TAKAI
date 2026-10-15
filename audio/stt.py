import speech_recognition as sr


def listen() -> str:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return ""

    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return ""