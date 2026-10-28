import speech_recognition as sr
import keyboard


def listen(language: str = "id-ID") -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.6

    with sr.Microphone() as source:
        print("Kalibrasi mikrofon...")
        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        print("Voice input aktif! Tekan Q untuk pause/resume.")

        while True:
            if keyboard.is_pressed("q"):
                print("Listening paused. Press Q to resume.")

                keyboard.wait("q", suppress=False)

                while keyboard.is_pressed("q"):
                    pass

                print("Listening resumed...")
                continue

            try:
                audio = recognizer.listen(
                    source,
                    timeout=0.5,
                    phrase_time_limit=None
                )

            except sr.WaitTimeoutError:
                continue

            try:
                text = recognizer.recognize_google(
                    audio,
                    language=language
                ).strip()

                if text:
                    print("You:", text)
                    return text

            except sr.UnknownValueError:
                print("Suara tidak dikenali")

            except sr.RequestError as error:
                print(f"Error pengenalan suara: {error}")
                return ""