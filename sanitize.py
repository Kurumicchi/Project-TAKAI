"""Text clean-up helpers shared by the providers and the speech layer."""

import re

_THINK_BLOCK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_UNCLOSED_THINK = re.compile(r"<think>.*\Z", re.DOTALL | re.IGNORECASE)

_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`([^`]*)`")
_BOLD_ITALIC = re.compile(r"(\*{1,3}|_{1,3})(.+?)\1", re.DOTALL)
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
_BULLET = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_EMOJI = re.compile(
    "[" "\U0001f300-\U0001faff" "\U00002600-\U000027bf" "\U0001f000-\U0001f2ff" "]+",
    flags=re.UNICODE,
)
_BLANK_RUN = re.compile(r"\n{3,}")
_SPACE_RUN = re.compile(r"[ \t]{2,}")


def strip_thinking(text: str) -> str:
    """Remove reasoning-model scratchpad blocks.

    Models such as Qwen3 emit `<think>...</think>` before their actual answer.
    That is internal monologue, not a reply -- it must never be printed to the
    user or read aloud.
    """
    if not text:
        return ""

    text = _THINK_BLOCK.sub("", text)

    # A truncated or still-streaming response can leave an unclosed tag.
    text = _UNCLOSED_THINK.sub("", text)

    return text.strip()


def for_speech(text: str) -> str:
    """Flatten Markdown into something a TTS engine can read naturally.

    Without this, the synthesiser pronounces asterisks, backticks and hash
    marks, and tries to read entire code blocks character by character.
    """
    if not text:
        return ""

    text = strip_thinking(text)

    text = _CODE_FENCE.sub(" ", text)
    text = _LINK.sub(r"\1", text)
    text = _INLINE_CODE.sub(r"\1", text)
    text = _BOLD_ITALIC.sub(r"\2", text)
    text = _HEADING.sub("", text)
    text = _BULLET.sub("", text)
    text = _EMOJI.sub("", text)

    text = _BLANK_RUN.sub("\n\n", text)
    text = _SPACE_RUN.sub(" ", text)

    return text.strip()
