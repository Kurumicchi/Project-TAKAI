"""Google Gemini adapter -- optional cloud provider.

Requires `pip install google-genai` and a GEMINI_API_KEY.
"""

import os

from google import genai
from google.genai import types

import config
from providers import ProviderError
from sanitize import strip_thinking

_client = None


def _get_client() -> "genai.Client":
    """Create the client on first use, with a readable error if the key is absent."""
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ProviderError(
            "GEMINI_API_KEY belum diset.\n"
            "Tambahkan ke file .env:  GEMINI_API_KEY=xxxxx\n"
            "Dapatkan kunci di https://aistudio.google.com/apikey"
        )

    _client = genai.Client(api_key=api_key)

    return _client


def get_reply(messages: list[dict]) -> str:
    """Send the conversation to Gemini and return TAKAI's reply."""
    client = _get_client()

    # Gemini labels assistant turns "model" rather than "assistant".
    contents = [
        types.Content(
            role="model" if message["role"] == "assistant" else "user",
            parts=[types.Part(text=message["content"])],
        )
        for message in messages
    ]

    try:
        response = client.models.generate_content(
            model=config.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=config.load_system_prompt(),
                temperature=config.TEMPERATURE,
                max_output_tokens=config.MAX_TOKENS,
            ),
        )

    except Exception as error:
        raise ProviderError(
            f"Permintaan ke Gemini gagal ({type(error).__name__}): {error}\n"
            f"Periksa GEMINI_API_KEY dan nama model "
            f"({config.GEMINI_MODEL!r}) di .env."
        ) from error

    text = getattr(response, "text", None)

    if not text:
        raise ProviderError(
            "Gemini tidak mengembalikan teks. Respons mungkin diblokir oleh "
            "filter keamanan atau terpotong."
        )

    return strip_thinking(text)
