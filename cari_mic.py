import sounddevice as sd

# Senarai semua mic. Nombor ni ikut sounddevice (sama macam dalam audio/stt.py).
for i, d in enumerate(sd.query_devices()):
    if d["max_input_channels"] <= 0:
        continue
    if "stereo mix" in d["name"].lower():
        continue

    host = sd.query_hostapis(d["hostapi"])["name"]

    try:
        s = sd.RawInputStream(device=i, samplerate=16000, channels=1, dtype="int16")
        s.start()
        s.stop()
        s.close()
        status = "OK"
    except Exception:
        status = "tak boleh buka"

    print(f"[{i}] {d['name']}  ({host}) -> {status}")

print("\nDefault Windows:", sd.default.device[0])
print("TAKAI guna default, jadi mana-mana mic pun boleh.")
