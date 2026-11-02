"""Central configuration for TAKAI.

Every tunable lives here and is driven by environment variables (loaded from
`.env` if present), so no module needs to hardcode paths, models or keys.

Copy `.env.example` to `.env` and edit it to change behaviour.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Anchor every path to the repository root rather than the current working
# directory, so TAKAI can be launched from anywhere.
BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def _flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)

    if raw is None:
        return default

    return raw.strip().lower() in ("1", "true", "yes", "on", "ya")


# --- LLM provider ------------------------------------------------------------

PROVIDER = os.getenv("TAKAI_PROVIDER", "ollama").strip().lower()

SYSTEM_PROMPT_PATH = BASE_DIR / os.getenv(
    "TAKAI_SYSTEM_PROMPT", "TAKAI_SYSTEM.md"
)

TEMPERATURE = float(os.getenv("TAKAI_TEMPERATURE", "0.5"))
MAX_TOKENS = int(os.getenv("TAKAI_MAX_TOKENS", "1024"))

# How many *pairs* of (user, assistant) turns to keep in context.
HISTORY_TURNS = int(os.getenv("TAKAI_HISTORY_TURNS", "8"))

# Ollama (local, default)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))

# Cloud providers (optional; require their own SDK + API key)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")


# --- Interaction mode --------------------------------------------------------

# "text"  -> type to TAKAI, replies printed (and spoken if TTS is on)
# "voice" -> push-to-talk microphone input
MODE = os.getenv("TAKAI_MODE", "text").strip().lower()


# --- Speech ------------------------------------------------------------------

# BCP-47 tag handed to the speech recogniser. Indonesian by default, which is
# the whole point of TAKAI -- do not leave this unset or it falls back to
# en-US and transcribes Indonesian as garbled English.
LANGUAGE = os.getenv("TAKAI_LANGUAGE", "id-ID")

TTS_ENABLED = _flag("TAKAI_TTS", True)

# Indonesian neural voices available via edge-tts:
#   id-ID-ArdiNeural  (male)
#   id-ID-GadisNeural (female)
TTS_VOICE = os.getenv("TAKAI_TTS_VOICE", "id-ID-ArdiNeural")
TTS_RATE = os.getenv("TAKAI_TTS_RATE", "+0%")
TTS_PITCH = os.getenv("TAKAI_TTS_PITCH", "+0Hz")

# Microphone capture
STT_SAMPLE_RATE = int(os.getenv("TAKAI_STT_SAMPLE_RATE", "16000"))

# Input device index, or None for the system default. Run
# `python -m audio.stt --devices` to list the options.
_device = os.getenv("TAKAI_STT_DEVICE", "").strip()

try:
    STT_DEVICE = int(_device) if _device else None

except ValueError:
    # A typo here should not stop TAKAI from starting.
    print(
        f"[CONFIG] TAKAI_STT_DEVICE={_device!r} bukan angka; "
        "memakai perangkat default."
    )
    STT_DEVICE = None

# Seconds of silence that ends an utterance.
STT_SILENCE_SECONDS = float(os.getenv("TAKAI_STT_SILENCE_SECONDS", "1.0"))

# Give up if the user never starts talking.
STT_START_TIMEOUT = float(os.getenv("TAKAI_STT_START_TIMEOUT", "8.0"))

# Hard ceiling on a single utterance.
STT_MAX_SECONDS = float(os.getenv("TAKAI_STT_MAX_SECONDS", "20.0"))

# Energy multiplier over the measured noise floor that counts as speech.
STT_THRESHOLD_FACTOR = float(os.getenv("TAKAI_STT_THRESHOLD_FACTOR", "3.0"))


def load_system_prompt() -> str:
    """Read the system prompt.

    Called lazily so a missing or unreadable prompt file surfaces as a clear
    message at runtime instead of an import-time traceback.
    """
    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        raise FileNotFoundError(
            f"System prompt tidak ditemukan: {SYSTEM_PROMPT_PATH}\n"
            "Pastikan TAKAI_SYSTEM.md ada di root repositori, atau set "
            "TAKAI_SYSTEM_PROMPT di .env."
        ) from None
