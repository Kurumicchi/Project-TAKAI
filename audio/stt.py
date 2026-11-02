import sounddevice as sd
import speech_recognition as sr
import keyboard


class Mic(sr.AudioSource):
    """Pengganti sr.Microphone yang guna sounddevice.

    Dua sebab tukar:
      1. sr.Microphone perlukan PyAudio, yang tiada wheel untuk Python 3.14.
      2. PyAudio dan sounddevice bagi nombor device yang berlainan, jadi
         device_index=12 dulu menunjuk mic yang salah (dan yang tak boleh
         dibuka langsung).

    device=None bermakna ikut mic default Windows, jadi mana-mana mic boleh.
    """

    SAMPLE_WIDTH = 2
    CHUNK = 1024

    def __init__(self, device=None, sample_rate=16000):
        self.device = device
        self.SAMPLE_RATE = sample_rate
        self.stream = None

    def __enter__(self):
        raw = sd.RawInputStream(
            device=self.device,
            samplerate=self.SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=self.CHUNK,
        )
        raw.start()
        self.stream = _Stream(raw)
        return self

    def __exit__(self, *args):
        self.stream.raw.stop()
        self.stream.raw.close()
        self.stream = None


class _Stream:
    # sr.Recognizer cuma perlu .read() yang pulangkan bytes
    def __init__(self, raw):
        self.raw = raw

    def read(self, size):
        data, _ = self.raw.read(size)
        return bytes(data)


def listen(language: str = "id-ID") -> str:
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0         # diubah: 0.6 -> 1.0
    recognizer.non_speaking_duration = 0.8   # baru

    with Mic() as source:                    # diubah: ikut mic default
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
                    timeout=3,               # diubah: 0.5 -> 3
                    phrase_time_limit=15     # diubah: None -> 15
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
