import json
from pathlib import Path

HISTORY_FILE = Path(__file__).with_name("chat_history.json")
MAX_TURNS = 5

def _group_into_turns(history):
    turns = []

    for message in history:
        if message["role"] == "user":
            turns.append([message])

        elif message["role"] == "assistant" and turns:
            turns[-1].append(message)

    return turns

def _trim_history(history):
    turns = _group_into_turns(history)
    recent_turns = turns[-MAX_TURNS:]

    return [
        message
        for turn in recent_turns
        for message in turn
    ]

def load_history():
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        history = json.load(file)

    if not isinstance(history, list):
        raise ValueError("Chat history must be a JSON list.")

    for message in history:
        if (
            not isinstance(message, dict)
            or message.get("role") not in ("user", "assistant")
            or not isinstance(message.get("content"), str)
        ):
            raise ValueError("Chat history contains an invalid message.")

    return _trim_history(history)


def add_message(role, content):
    if role not in ("user", "assistant"):
        raise ValueError(f"Invalid message role: {role}")

    history = load_history()

    history.append({
        "role": role,
        "content": content
    })

    history = _trim_history(history)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)
