import asyncio
import os
import re
import tempfile
import uuid

import edge_tts

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

VOICE = "id-ID-GadisNeural"   # lelaki. Perempuan: "id-ID-GadisNeural"
RATE = "+15%"                 # laju cakap, contoh "+10%" atau "-10%"


def _clean(text):
    # Buang bahagian "berfikir" model dan simbol Markdown
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"[*_#`>]", "", text)
    return text.strip()


async def _save(text, path):
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)


def speak(text):
    text = _clean(text)
    if not text:
        return

    path = os.path.join(tempfile.gettempdir(), f"takai_tts_{uuid.uuid4().hex}.mp3")

    try:
        asyncio.run(_save(text, path))
    except Exception as error:
        print(f"Error TTS: {error}")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    try:
        os.remove(path)
    except OSError:
        pass


if __name__ == "__main__":
    speak("Halo, saya TAKAI. Selamat datang di Lab B201.")
