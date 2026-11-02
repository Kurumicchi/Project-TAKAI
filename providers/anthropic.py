"""Anthropic Claude adapter -- optional cloud provider.

Requires `pip install anthropic` and an ANTHROPIC_API_KEY.

Note: this module is `providers.anthropic`, while the SDK is the top-level
`anthropic` package. Python 3 uses absolute imports, so the import below
resolves to the installed SDK and not to this file. (The original code read
`from providers.anthropic import Anthropic`, which imported itself and raised
ImportError on every run.)
"""

import os

from anthropic import Anthropic

import config
from providers import ProviderError
from sanitize import strip_thinking

_client = None


def _get_client() -> Anthropic:
    """Create the client on first use, with a readable error if the key is absent."""
    global _client

    if _client is not None:
        return _client

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ProviderError(
            "ANTHROPIC_API_KEY belum diset.\n"
            "Tambahkan ke file .env:  ANTHROPIC_API_KEY=sk-ant-xxxxx\n"
            "Dapatkan kunci di https://console.anthropic.com/settings/keys"
        )

    _client = Anthropic()

    return _client


def get_reply(messages: list[dict]) -> str:
    """Send the conversation to Claude and return TAKAI's reply."""
    client = _get_client()

    try:
        response = client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
            system=config.load_system_prompt(),
            messages=messages,
        )

    except Exception as error:
        raise ProviderError(
            f"Permintaan ke Anthropic gagal ({type(error).__name__}): {error}\n"
            f"Periksa ANTHROPIC_API_KEY dan nama model "
            f"({config.ANTHROPIC_MODEL!r}) di .env."
        ) from error

    chunks = [
        block.text
        for block in response.content
        if getattr(block, "type", None) == "text"
    ]

    if not chunks:
        raise ProviderError("Claude tidak mengembalikan teks apa pun.")

    return strip_thinking("".join(chunks))
