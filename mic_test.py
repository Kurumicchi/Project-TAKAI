import speech_recognition as sr

from audio.stt import Mic

r = sr.Recognizer()

with Mic() as source:
    print("\n1. Diam 2 saat, tengah ukur bunyi bilik...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("   Tahap bising:", round(r.energy_threshold))

    print("2. Cakap sekarang!")
    audio = r.listen(source, timeout=5, phrase_time_limit=5)

    with open("rakaman.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("   Audio disimpan: rakaman.wav")

    print("3. Dapat audio, hantar ke Google...")
    print("4. Hasil:", r.recognize_google(audio, language="id-ID"))
