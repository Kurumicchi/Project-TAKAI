import speech_recognition as sr
import keyboard
import time

r = sr.Recognizer()
mic = sr.Microphone()

# Kalibrasi mikrofon sekali di awal
with mic as source:
    print("Kalibrasi mikrofon...")
    r.adjust_for_ambient_noise(source, duration=1)

def callback(recognizer, audio):
    try:
        teks = recognizer.recognize_google(
            audio, language="id-ID"
        )
        print("User:", teks)

    except sr.UnknownValueError:
        print("Suara tidak dikenali")

    except sr.RequestError as e:
        print("Error:", e)

print("Klik kotak teks yang ingin diisi.")
time.sleep(3)

print("Voice typing aktif! Tekan Q untuk berhenti.")

stop = r.listen_in_background(mic, callback)

try:
    while not keyboard.is_pressed("q"):
        time.sleep(0.1)
finally:
    stop(wait_for_stop=True)
    print("Tutup")
