from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import settings


def check(name: str, ok: bool, detail: str = "") -> bool:
    status = "OK" if ok else "FAIL"
    suffix = f" - {detail}" if detail else ""
    print(f"[{status}] {name}{suffix}")
    return ok


def main(play_audio: bool = False) -> int:
    results: list[bool] = []

    print("EON-V self-test")
    print(f"Project root: {settings.PROJECT_ROOT}")
    print(f"Mic capture mode: {settings.MIC_CAPTURE_MODE}")

    results.append(check("settings", settings.PROJECT_ROOT.exists()))
    results.append(check("memory file parent", (settings.PROJECT_ROOT / settings.MEMORY_FILE).parent.exists()))

    try:
        from voice.wake_word import WakeWordDetector
        from voice.vad_recorder import EnergyVoiceActivityDetector

        detector = WakeWordDetector()
        results.append(check("wake word EON", detector.detect("eon test")))
        results.append(check("wake word variant", detector.detect("йон test")))
        vad = EnergyVoiceActivityDetector(energy_threshold=100)
        vad.calibrate([b"\x00\x00" * 160])
        loud_frame = (1000).to_bytes(2, byteorder="little", signed=True) * 160
        results.append(check("energy VAD", vad.analyze(loud_frame).is_speech))
    except Exception as exc:
        results.append(check("wake/VAD", False, str(exc)))

    try:
        from voice.voice_pipeline import VoicePipeline

        packet = VoicePipeline().process_raw_input("eon статус")
        results.append(check("voice pipeline", packet.get("wake_word_detected") is True))
    except Exception as exc:
        results.append(check("voice pipeline", False, str(exc)))

    try:
        from vision.vision_pipeline import VisionPipeline

        packet = VisionPipeline().process_scene("person near robot")
        results.append(check("vision pipeline", "detections" in packet))
    except Exception as exc:
        results.append(check("vision pipeline", False, str(exc)))

    try:
        from sounds.sound_registry import list_sounds, play_sound

        sounds = list_sounds()
        results.append(check("sound registry", bool(sounds), f"{len(sounds)} sounds"))
        if play_audio:
            results.append(check("wake ack sound", play_sound(settings.WAKE_ACK_SOUND, force=True)))
    except Exception as exc:
        results.append(check("sounds", False, str(exc)))

    try:
        piper = Path(settings.PIPER_EXE_PATH)
        if not piper.is_absolute():
            piper = settings.PROJECT_ROOT / piper
        vosk = Path(settings.VOSK_MODEL_PATH)
        if not vosk.is_absolute():
            vosk = settings.PROJECT_ROOT / vosk
        results.append(check("Piper path", piper.exists(), str(piper)))
        results.append(check("Vosk path", vosk.exists(), str(vosk)))
    except Exception as exc:
        results.append(check("voice model paths", False, str(exc)))

    if all(results):
        print("Self-test passed.")
        return 0

    print("Self-test found problems.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
