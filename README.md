# TAKAI

Asisten suara Bahasa Indonesia — a voice assistant that listens, thinks and
replies in Indonesian. Runs fully locally by default (Ollama), with optional
cloud providers.

```
  Mikrofon ──▶ STT (id-ID) ──▶ LLM + system prompt ──▶ TTS (id-ID) ──▶ Speaker
              sounddevice      ollama / gemini /        edge-tts
            + SpeechRecognition    anthropic          (+ offline fallback)
```

---

## 1. Architecture

| Layer | Module | What it does |
|---|---|---|
| Entry point | `main.py` | CLI, mode selection, conversation loop, memory |
| Config | `config.py` | All settings, loaded from `.env` |
| Text clean-up | `sanitize.py` | Strips `<think>` blocks and Markdown before speaking |
| Speech-to-text | `audio/stt.py` | Mic capture + Indonesian transcription |
| Text-to-speech | `audio/tts.py` | Indonesian neural voice, with offline fallback |
| LLM adapters | `providers/` | `ollama` (default), `gemini`, `anthropic` |
| Persona | `TAKAI_SYSTEM.md` | System prompt enforcing Indonesian + personality |
| Dictation tool | `Takai.py` | Standalone voice-typing utility (not part of the loop) |

**Conversation memory** is kept in-process: the last `TAKAI_HISTORY_TURNS`
user/assistant pairs are resent on every request, so TAKAI follows context
across turns. It resets when you exit or type `reset`.

### Not implemented

Be aware these are *absent*, not broken — building them is new work:

- **Wake-word detection** ("Hai Takai"). Input is push-to-talk only.
- **Intent/NLP routing & tools.** Everything goes to the LLM as free text;
  there is no timer, alarm, smart-home or skill dispatch.
- **Web/GUI frontend.** Terminal only.
- **Persistent memory.** History is lost on exit.

---

## 2. Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.12 – 3.14** | Verified on 3.14.2 (Windows 11) |
| **Ollama** | Only for the default local provider — https://ollama.com/download |
| Microphone | Any input device; needed for voice mode only |
| Internet | Needed for speech recognition and the Indonesian TTS voice |

**ffmpeg is not required.** **PyAudio is not required** either — `sounddevice`
bundles PortAudio, which sidesteps the fact that PyAudio has no prebuilt wheel
for Python 3.14 and otherwise needs a C++ toolchain on Windows.

No API key is needed for the default setup.

---

## 3. Install

```bash
git clone https://github.com/Kurumicchi/Project-TAKAI.git
cd Project-TAKAI
```

Keep the repo on a **short path** (e.g. `Desktop\Project-TAKAI`). Cloning into
a deeply nested directory fails on Windows with `Filename too long`.

Create the virtual environment:

```bash
python -m venv .venv
```

Activate it — PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Create your config from the template:

```bash
copy .env.example .env
```

---

## 4. Set up the model (Ollama)

Install Ollama, then pull a model with good Indonesian:

```bash
ollama pull qwen3:8b
```

On a machine with 8 GB RAM or less, use the smaller variant and set
`OLLAMA_MODEL=qwen3:4b` in `.env`:

```bash
ollama pull qwen3:4b
```

Confirm the server is reachable:

```bash
ollama list
```

Ollama serves on `http://localhost:11434` once running.

---

## 5. Run

Text mode (type to TAKAI, replies are spoken aloud):

```bash
python main.py
```

Voice mode (push-to-talk — speak, pause, and TAKAI answers):

```bash
python main.py --voice
```

Useful flags:

```bash
python main.py --no-tts              # silent output
python main.py --provider gemini     # override the provider
python main.py --voice --no-tts      # listen, reply in text only
```

In-conversation commands: `keluar` to exit, `reset` to clear history.

---

## 6. Diagnostics

Run these first whenever audio misbehaves.

List microphones (then set `TAKAI_STT_DEVICE` in `.env`):

```bash
python -m audio.stt --devices
```

Test transcription — speak after the prompt appears:

```bash
python -m audio.stt
```

List Indonesian voices:

```bash
python -m audio.tts --voices
```

Test speech output:

```bash
python -m audio.tts
```

---

## 7. Troubleshooting

**`Tidak dapat terhubung ke Ollama`** — Ollama isn't running. Start the app, or
run `ollama serve`.

**`Model 'qwen3:8b' tidak ditemukan`** — run `ollama pull qwen3:8b`. Check what
you have with `ollama list`.

**Ollama times out** — the model is too large for your RAM or is still loading.
Switch to `qwen3:4b`, or raise `OLLAMA_TIMEOUT` in `.env`.

**`Tidak dapat membuka mikrofon`** — run `python -m audio.stt --devices` and set
`TAKAI_STT_DEVICE` to a listed index. Also check Windows mic privacy settings
(Settings → Privacy & security → Microphone).

**`Suara tidak dikenali`** — speech recognition needs internet. If it keeps
missing quiet speech, lower `TAKAI_STT_THRESHOLD_FACTOR` (try `2.0`); in a noisy
room, raise it.

**TAKAI cuts you off mid-sentence** — raise `TAKAI_STT_SILENCE_SECONDS` to
`1.5`.

**Speech sounds English-accented** — edge-tts couldn't reach the network, so the
offline engine took over using an English system voice. Check your connection.
For a proper offline Indonesian voice, add one via Settings → Time & language →
Speech → Manage voices → Add voices → Indonesian.

**`Provider 'gemini' tidak dapat dimuat`** — install the optional SDK:
`pip install google-genai` (or `pip install anthropic`), and set the matching
API key in `.env`.

---

## 8. Configuration reference

See [`.env.example`](.env.example) — every option is documented inline with its
default. The settings you are most likely to touch:

| Variable | Default | Purpose |
|---|---|---|
| `TAKAI_PROVIDER` | `ollama` | `ollama` \| `gemini` \| `anthropic` |
| `OLLAMA_MODEL` | `qwen3:8b` | Must match a pulled model |
| `TAKAI_MODE` | `text` | `text` \| `voice` |
| `TAKAI_LANGUAGE` | `id-ID` | Recognition language — **keep as `id-ID`** |
| `TAKAI_TTS_VOICE` | `id-ID-ArdiNeural` | Or `id-ID-GadisNeural` (female) |
| `TAKAI_TTS` | `true` | Spoken output on/off |
| `TAKAI_HISTORY_TURNS` | `8` | Turn pairs kept in context |
| `TAKAI_STT_DEVICE` | *(default)* | Mic index from `--devices` |

---

## 9. Repair log

The upstream repository did not run. What was fixed:

| # | Issue | Resolution |
|---|---|---|
| 1 | `providers/anthropic.py` imported **itself** (`from providers.anthropic import Anthropic`) — guaranteed `ImportError` | Corrected to the real SDK import |
| 2 | `audio/tts.py` was an **empty 0-byte file** — no speech output existed | Implemented with Indonesian neural voice + offline fallback |
| 3 | STT ran in **English** (`recognize_google` with no `language`) | Pinned to `config.LANGUAGE` (`id-ID`) |
| 4 | Provider switch was **dead code** inside a `"""string"""` — selecting gemini/anthropic raised `ValueError` | Real lazy dispatch via `providers.load()` |
| 5 | `open("TAKAI_SYSTEM.md")` at import time, relative path | Resolved from `BASE_DIR`, loaded lazily |
| 6 | No env-var handling anywhere, despite `.gitignore` expecting `.env.example` | Added `config.py` + documented `.env.example` |
| 7 | No `requirements.txt`; `PyAudio` needed but undeclared *and* uninstallable on Python 3.14 | Added pinned `requirements.txt`; switched to `sounddevice` |
| 8 | Invalid/outdated model IDs (`gemini-3.6-flash`, `claude-3-5-sonnet-20241022`, a nonexistent Qwen GGUF tag) | Replaced with current, configurable defaults |
| 9 | Unhandled `raise_for_status()` — a stopped Ollama crashed the app with a traceback | Typed errors with actionable Indonesian messages |
| 10 | `Takai.py` ran mic calibration + a blocking loop **at import time** and needed `keyboard` | Rewritten as a guarded dictation tool reusing `audio/stt.py` |
| 11 | Stateless — each message sent with no history | Conversation memory with configurable window |
| 12 | Reasoning models' `<think>` scratchpad would be printed and read aloud | `sanitize.strip_thinking()` removes it |
