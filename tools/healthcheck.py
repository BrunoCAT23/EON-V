from __future__ import annotations

import importlib
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


def can_import(module_name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        return False, str(exc)
    return True, "imported"


def main() -> int:
    results: list[bool] = []

    print("EON-V healthcheck")
    print(f"Project root: {settings.PROJECT_ROOT}")
    print(f"Robot: {settings.ROBOT_NAME}")
    print("")

    results.append(check("settings loaded", settings.PROJECT_ROOT.exists()))
    results.append(check("memory directory", (settings.PROJECT_ROOT / "memory").exists()))
    piper_exe = Path(settings.PIPER_EXE_PATH)
    if not piper_exe.is_absolute():
        piper_exe = settings.PROJECT_ROOT / piper_exe

    piper_voice = Path(settings.PIPER_VOICE_PATH)
    if not piper_voice.is_absolute():
        piper_voice = settings.PROJECT_ROOT / piper_voice

    vosk_model = Path(settings.VOSK_MODEL_PATH)
    if not vosk_model.is_absolute():
        vosk_model = settings.PROJECT_ROOT / vosk_model

    if settings.TTS_MODE == "local_ready":
        results.append(check("Configured Piper executable", piper_exe.is_file(), str(piper_exe)))
        results.append(check("Configured Piper voice", piper_voice.is_file(), str(piper_voice)))
    else:
        print("[SKIP] Piper assets: TTS_MODE does not select local_ready")
    if settings.STT_MODE == "local_ready":
        results.append(check("Configured Vosk model", vosk_model.is_dir(), str(vosk_model)))
    else:
        print("[SKIP] Vosk model: STT_MODE does not select local_ready")

    startup_sound = Path(settings.STARTUP_SOUND_PATH)
    if not startup_sound.is_absolute():
        startup_sound = settings.PROJECT_ROOT / startup_sound
    results.append(check("Startup sound path parent", startup_sound.parent.exists(), str(startup_sound.parent)))

    try:
        from sounds.sound_registry import list_sounds

        sounds = list_sounds()
        results.append(check("Sound registry", bool(sounds), f"{len(sounds)} sounds available"))
    except Exception as exc:
        results.append(check("Sound registry", False, str(exc)))

    last_frame = Path(settings.LAST_FRAME_PATH)
    if not last_frame.is_absolute():
        last_frame = settings.PROJECT_ROOT / last_frame
    last_frame.parent.mkdir(parents=True, exist_ok=True)
    results.append(check("Last frame path parent", last_frame.parent.exists(), str(last_frame.parent)))

    print("")
    print("Configured modes")
    print(f"Runtime: {settings.RUNTIME_MODE}")
    print(f"Voice: mic={settings.MIC_MODE}, speaker={settings.SPEAKER_MODE}, stt={settings.STT_MODE}, tts={settings.TTS_MODE}")
    print(f"Mic capture: mode={settings.MIC_CAPTURE_MODE}, vad_silence={settings.VAD_SILENCE_MS}ms, vad_threshold={settings.VAD_ENERGY_THRESHOLD}")
    print(f"Vision: camera={settings.CAMERA_MODE}, detector={settings.DETECTOR_MODE}")
    print(f"Hardware: {settings.HARDWARE_MODE}")
    print(f"Motion: enabled={settings.MOTION_ENABLED}, dry_run={settings.MOTION_DRY_RUN}, timeout={settings.MOTION_COMMAND_TIMEOUT}s")
    print(f"LLM: openai={settings.OPENAI_ENABLED}, ollama={settings.OLLAMA_ENABLED}")
    print(f"Startup sound: enabled={settings.STARTUP_SOUND_ENABLED}, path={settings.STARTUP_SOUND_PATH}")
    print(
        "Sound effects: "
        f"enabled={settings.SOUND_EFFECTS_ENABLED}, "
        f"dir={settings.SOUND_EFFECTS_DIR}, "
        f"volume={settings.SOUND_EFFECTS_VOLUME}"
    )
    print(
        "Live intervals: "
        f"voice={settings.LIVE_VOICE_INTERVAL}s, "
        f"vision={settings.LIVE_VISION_INTERVAL}s, "
        f"runtime={settings.LIVE_RUNTIME_INTERVAL}s"
    )
    print(f"Last frame path: {settings.LAST_FRAME_PATH}")
    print("")

    for module_name in [
        "brain.core",
        "voice.voice_pipeline",
        "vision.vision_pipeline",
        "memory.memory_manager",
        "llm.llm_manager",
    ]:
        ok, detail = can_import(module_name)
        results.append(check(f"import {module_name}", ok, detail))

    try:
        from brain.core import Brain

        Brain()
        results.append(check("Brain initialization", True))
    except Exception as exc:
        results.append(check("Brain initialization", False, str(exc)))

    try:
        from voice.voice_pipeline import VoicePipeline

        pipeline = VoicePipeline()
        packet = pipeline.process_raw_input("eon привіт")
        results.append(check("Voice pipeline stub", packet.get("wake_word_detected") is True))
    except Exception as exc:
        results.append(check("Voice pipeline stub", False, str(exc)))

    try:
        from voice.vosk_stt import VoskSTT

        stt = VoskSTT()
        text = stt.transcribe({"raw_text": "eon test", "audio_data": None})
        results.append(check("Vosk STT text bypass", text == "eon test"))
    except Exception as exc:
        results.append(check("Vosk STT text bypass", False, str(exc)))

    try:
        from vision.vision_pipeline import VisionPipeline

        pipeline = VisionPipeline()
        packet = pipeline.process_scene("person in front of robot")
        results.append(check("Vision pipeline stub", "detections" in packet))
    except Exception as exc:
        results.append(check("Vision pipeline stub", False, str(exc)))

    if settings.OPENAI_ENABLED:
        results.append(check("OpenAI API key", bool(settings.OPENAI_API_KEY), "OPENAI_API_KEY required when OPENAI_ENABLED=true"))

    if settings.DETECTOR_MODE == "yolo_ready":
        yolo_path = Path(settings.YOLO_MODEL_PATH)
        if not yolo_path.is_absolute():
            yolo_path = settings.PROJECT_ROOT / yolo_path
        results.append(check("YOLO model file", yolo_path.exists(), str(yolo_path)))

    print("")
    if all(results):
        print("Healthcheck passed.")
        return 0

    print("Healthcheck found problems.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
