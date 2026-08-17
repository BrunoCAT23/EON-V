import subprocess
from pathlib import Path
from settings import PIPER_EXE_PATH, PIPER_VOICE_PATH, PROJECT_ROOT, VOICE_RATE

def _resolve_path(path_value):
    path = Path(path_value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


MODEL_PATH = _resolve_path(PIPER_VOICE_PATH)
PIPER_EXE = _resolve_path(PIPER_EXE_PATH)

def speak(text, speed=None):
    if not text:
        return

    if speed is None:
        speed = VOICE_RATE

    if not PIPER_EXE.exists() or not MODEL_PATH.exists():
        print(f"[VOICE_AI_FALLBACK] {text}")
        return

    try:
        import numpy as np
        import sounddevice as sd
    except ImportError as exc:
        print(f"[VOICE_AI_FALLBACK] Audio dependency missing: {exc}. Text: {text}")
        return

    try:
        result = subprocess.run(
            [
                str(PIPER_EXE),
                "--model", str(MODEL_PATH),
                "--output-raw",
            ],
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"[VOICE_AI_FALLBACK] Piper failed: {exc}. Text: {text}")
        return

    if result.returncode != 0 or not result.stdout:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        print(f"[VOICE_AI_FALLBACK] Piper returned {result.returncode}: {error}. Text: {text}")
        return

    audio = np.frombuffer(result.stdout, dtype=np.int16)

    try:
        sd.play(audio, samplerate=22050)
        sd.wait()
    except Exception as exc:
        print(f"[VOICE_AI_FALLBACK] Audio playback failed: {exc}. Text: {text}")
