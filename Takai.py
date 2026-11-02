"""Voice typing / dictation tool (Bahasa Indonesia).

Transcribes whatever you say, one utterance at a time, and prints it. Useful on
its own for dictation; it is not part of the assistant pipeline -- that is
`main.py`.

    python Takai.py

Press Ctrl+C to stop.

Note: the original version of this file ran microphone calibration and a
blocking input loop at *import* time, and depended on the `keyboard` package
(which needs elevated privileges for global hotkeys on Windows). Both problems
are gone -- it now reuses `audio.stt` and only runs when executed directly.
"""

import sys

import config
from audio.stt import MicrophoneError, listen


def main() -> int:
    print("=" * 58)
    print("  TAKAI - Voice Typing (Bahasa Indonesia)")
    print("=" * 58)
    print(f"  Bahasa : {config.LANGUAGE}")
    print("  Tekan Ctrl+C untuk berhenti.")
    print("=" * 58 + "\n")

    lines: list[str] = []

    try:
        while True:
            try:
                text = listen()

            except MicrophoneError as error:
                print(f"\n[MIKROFON] {error}\n", file=sys.stderr)
                return 1

            if text:
                lines.append(text)
                print(f"  > {text}\n")

    except KeyboardInterrupt:
        print("\n" + "-" * 58)

        if lines:
            print("Hasil transkripsi lengkap:\n")
            print(" ".join(lines))

        else:
            print("Tidak ada teks yang ditranskripsi.")

        print("-" * 58)

    return 0


if __name__ == "__main__":
    sys.exit(main())
