"""LLM provider adapters.

Every provider module exposes a single function:

    get_reply(messages: list[dict]) -> str

where `messages` is the conversation so far as ``{"role", "content"}`` dicts
(user/assistant only -- each provider attaches the system prompt itself).

Providers are imported lazily through `load()` so that an uninstalled optional
SDK (google-genai, anthropic) can never break the default local setup.
"""

import importlib
from types import ModuleType

AVAILABLE = ("ollama", "gemini", "anthropic")

_INSTALL_HINT = {
    "ollama": "pip install requests",
    "gemini": "pip install google-genai",
    "anthropic": "pip install anthropic",
}


class ProviderError(RuntimeError):
    """Raised for any provider problem that should be shown to the user."""


def load(name: str) -> ModuleType:
    """Import and return the adapter module for `name`."""
    key = (name or "").strip().lower()

    if key not in AVAILABLE:
        raise ProviderError(
            f"Provider tidak dikenali: {name!r}. "
            f"Pilihan yang tersedia: {', '.join(AVAILABLE)}. "
            "Periksa TAKAI_PROVIDER di .env."
        )

    try:
        return importlib.import_module(f"providers.{key}")

    except ImportError as error:
        raise ProviderError(
            f"Provider {key!r} tidak dapat dimuat: {error}\n"
            f"Kemungkinan dependensi belum terpasang. Jalankan: "
            f"{_INSTALL_HINT[key]}"
        ) from error
