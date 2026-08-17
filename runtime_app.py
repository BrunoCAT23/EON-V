from __future__ import annotations

import logging
from pathlib import Path

from brain.core import Brain
from hardware.backend_factory import create_hardware_backend
from live_runtime import LiveRuntime
from logging_config import setup_logging
import settings
from settings import LAST_FRAME_PATH, PROJECT_ROOT, VOICE_TEST_PHRASE
from sounds.sound_registry import list_sounds, play_event_sound, play_sound
from sounds.startup_sound import play_startup_sound
from tools.self_test import main as run_self_test
from voice.wake_calibrator import WakeCalibrator
from voice.wake_word import WakeWordDetector
from tools.healthcheck import main as run_healthcheck
from tools.dashboard import build_dashboard
from voice.voice_loop import VoiceLoop
from voice.voice_pipeline import VoicePipeline
from vision.vision_loop import VisionLoop
from vision.vision_pipeline import VisionPipeline


logger = logging.getLogger(__name__)


class RuntimeApp:
    def __init__(self) -> None:
        setup_logging()
        play_startup_sound()

        hardware = create_hardware_backend(settings.HARDWARE_MODE)
        self.brain = Brain(hardware_manager=hardware)

        self.voice_pipeline = VoicePipeline()
        self.vision_pipeline = VisionPipeline()
        self.voice_loop = VoiceLoop(self)
        self.vision_loop = VisionLoop(self)
        self.live_runtime = LiveRuntime(self)
        self.do_not_disturb = settings.DO_NOT_DISTURB

    def print_help(self) -> None:
        print("EON-V Core v35 Runtime App")
        print("Text commands: voice, face, think, sleep, sad, wake, idle, idle_auto, battery_low, status, meet <name>")
        print("Voice mode: say <phrase>")
        print("Vision mode: see <scene>")
        print("Runtime mode: auto_on, auto_off, step, update, run, run_all, run_steps <n>, queue_status")
        print("Mode command: mode")
        print("Memory commands: memory_context")
        print("Companion commands: event_log, diagnostics, safety_status, schedule_status, remind_in <ticks> <text>")
        print("Profile commands: profile <name>, profile_set_name <name> <preferred>, profile_add_date <name> <label> <date>")
        print("Learning commands: teach <key> = <value>, head <left|right|center|down>")
        print("Dashboard command: dashboard")
        print("Loop commands: voice_loop_once [text], vision_loop_once [scene]")
        print("Live commands: live, live_test [cycles], stop_live")
        print("Diagnostic commands: voice_test [phrase], camera_test [scene], self_test")
        print("Mic commands: vad_status, mic_test")
        print("Wake commands: wake_calibrate <samples...>, wake_calibrate_mic [count]")
        print("Focus commands: dnd_on, dnd_off")
        print("Sound commands: startup_sound, sound_list, sound_test <name>")
        print("Safety commands: estop [reason], estop_reset")
        print("Other commands: health, help, exit")

    def run_cli(self) -> None:
        self.print_help()

        while True:
            user_input = input("Enter command: ").strip()

            if not self.handle_command(user_input):
                break

    def handle_command(self, user_input: str) -> bool:
        command = user_input.strip()
        normalized = command.lower()

        if not command:
            return True

        logger.info("Command received: %s", command)

        if normalized == "exit":
            print("Shutting down EON-V...")
            return False

        if normalized == "help":
            self.print_help()
            return True

        if normalized == "health":
            run_healthcheck()
            return True

        if normalized == "mode":
            self.print_runtime_mode()
            return True

        if normalized == "dashboard":
            output_path = PROJECT_ROOT / "logs" / "dashboard.html"
            build_dashboard(self.brain, output_path)
            print(f"[DASHBOARD] Generated: {output_path}")
            return True

        if normalized == "memory_context":
            self.brain.process_event("dialogue_summary")
            self.brain.run_all_actions()
            return True

        if normalized == "self_test":
            run_self_test(play_audio=False)
            return True

        if normalized == "self_test_audio":
            run_self_test(play_audio=True)
            return True

        if normalized == "vad_status":
            self.print_vad_status()
            return True

        if normalized == "mic_test":
            self.mic_test()
            return True

        if normalized == "startup_sound":
            play_startup_sound(force=True)
            return True

        if normalized == "sound_list":
            self.print_sound_list()
            return True

        if normalized.startswith("sound_test"):
            sound_name = command[len("sound_test"):].strip()
            if not sound_name:
                print("[SOUND] Usage: sound_test <name>")
                return True
            play_sound(sound_name, force=True)
            return True

        if normalized == "dnd_on":
            self.do_not_disturb = True
            print("[DND] Do not disturb enabled. Wake word will be ignored until dnd_off.")
            return True

        if normalized == "dnd_off":
            self.do_not_disturb = False
            print("[DND] Do not disturb disabled.")
            return True

        if normalized.startswith("wake_calibrate_mic"):
            raw_count = command[len("wake_calibrate_mic"):].strip()
            try:
                count = int(raw_count) if raw_count else 5
            except ValueError:
                print("[WAKE_CALIBRATE] Usage: wake_calibrate_mic [count]")
                return True
            words = WakeCalibrator().calibrate_from_microphone(count)
            self.voice_pipeline.wake_word_detector = WakeWordDetector(words)
            print(f"[WAKE_CALIBRATE] Updated WAKE_WORDS: {', '.join(words)}")
            return True

        if normalized.startswith("wake_calibrate"):
            samples = command[len("wake_calibrate"):].strip()
            if not samples:
                print("[WAKE_CALIBRATE] Usage: wake_calibrate <sample1 | sample2 | ...>")
                return True
            words = WakeCalibrator().calibrate_from_samples(
                [sample.strip() for sample in samples.split("|")]
            )
            self.voice_pipeline.wake_word_detector = WakeWordDetector(words)
            print(f"[WAKE_CALIBRATE] Updated WAKE_WORDS: {', '.join(words)}")
            return True

        if normalized.startswith("voice_test"):
            phrase = command[len("voice_test"):].strip() or VOICE_TEST_PHRASE
            self.voice_test(phrase)
            return True

        if normalized.startswith("camera_test"):
            scene = command[len("camera_test"):].strip()
            self.camera_test(scene)
            return True

        if normalized == "live":
            self.live_runtime.start()
            return True

        if normalized.startswith("live_test"):
            raw_count = command[len("live_test"):].strip()
            try:
                count = max(1, min(100, int(raw_count))) if raw_count else 3
            except ValueError:
                print("[LIVE] Usage: live_test <cycles>")
                return True
            self.live_runtime.start(max_cycles=count, enable_voice=False)
            return True

        if normalized == "stop_live":
            self.live_runtime.stop()
            return True

        if normalized.startswith("run_steps "):
            self.run_steps(normalized.replace("run_steps ", "", 1).strip())
            return True

        if normalized.startswith("voice_loop_once"):
            raw_text = command[len("voice_loop_once"):].strip()
            self.voice_loop.run_once(raw_text)
            return True

        if normalized.startswith("vision_loop_once"):
            raw_scene = command[len("vision_loop_once"):].strip()
            self.vision_loop.run_once(raw_scene)
            return True

        if normalized == "estop_reset":
            self.brain.hardware_manager.reset_emergency_stop()
            return True

        if normalized.startswith("estop"):
            reason = command[len("estop"):].strip() or "manual"
            self.brain.hardware_manager.emergency_stop(reason)
            return True

        if normalized in [
            "run", "run_all", "queue_status",
            "idle_auto", "auto_on", "auto_off",
            "tick", "update", "step",
        ]:
            self.brain.process_event(normalized)
            return True

        if normalized.startswith("behavior "):
            self.brain.process_event(command)
            self.brain.run_all_actions()
            return True

        if normalized.startswith("skill "):
            skill_name = command[6:].strip().lower()
            self.brain.execute_skill(skill_name)
            self.brain.run_all_actions()
            return True

        if normalized.startswith("say "):
            self.handle_voice_input(command[4:].strip())
            return True

        if normalized.startswith("see "):
            self.handle_vision_input(command[4:].strip())
            return True

        self.brain.process_event(command)
        self.brain.run_all_actions()
        return True

    def run_steps(self, raw_count: str) -> None:
        try:
            count = max(1, min(100, int(raw_count)))
        except ValueError:
            print("[RUNTIME] Usage: run_steps <number>")
            return

        if not self.brain.life_state.is_enabled():
            self.brain.life_state.enable()

        for _ in range(count):
            self.brain.runtime_orchestrator.step(self.brain)
            self.brain.handle_check_reminders()

    def handle_voice_input(self, raw_phrase: str) -> dict:
        if self.do_not_disturb:
            print("[DND] Voice input ignored.")
            return {
                "heard": raw_phrase,
                "wake_word_detected": False,
                "intent_data": None,
                "response": {"event": None, "text": "Do not disturb is enabled."},
            }

        result = self.voice_pipeline.process_raw_input(raw_phrase)

        print(f"[VOICE] Heard: {result.get('heard')}")
        print(f"[VOICE] Wake word detected: {result.get('wake_word_detected')}")

        if result.get("wake_word_detected") and not result.get("cleaned_text", "").strip():
            self.handle_wake_ack(raw_phrase)
            return result

        intent_data = result.get("intent_data")
        if intent_data:
            self.brain.process_voice_context(
                raw_text=result.get("cleaned_text", raw_phrase),
                intent_name=intent_data.get("intent"),
            )

        self.brain.submit_voice_perception(result)
        self._execute_response_event(result.get("response", {}))
        self.brain.perception_sync.consume()
        return result

    def handle_wake_ack(self, raw_phrase: str) -> None:
        play_sound(settings.WAKE_ACK_SOUND)
        print(f"[WAKE] {settings.WAKE_REPLY_TEXT}")

        should_capture_followup = (
            settings.WAKE_FOLLOWUP_CAPTURE
            and not raw_phrase.strip()
            and settings.MIC_MODE == "mic_ready"
        )
        if not should_capture_followup:
            return

        print("[WAKE] Listening for command...")
        followup = self.voice_pipeline.process_command_input("")
        print(f"[VOICE] Heard command: {followup.get('heard')}")

        intent_data = followup.get("intent_data")
        if intent_data:
            self.brain.process_voice_context(
                raw_text=followup.get("cleaned_text", ""),
                intent_name=intent_data.get("intent"),
            )

        self.brain.submit_voice_perception(followup)
        self._execute_response_event(followup.get("response", {}))
        self.brain.perception_sync.consume()

    def handle_vision_input(self, raw_scene: str) -> dict:
        known_people = list(self.brain.memory_manager.get_people().keys())
        known_pets = self.brain.memory_manager.get_pets()

        self.vision_pipeline.update_known_people(known_people)
        self.vision_pipeline.update_known_pets(known_pets)

        result = self.vision_pipeline.process_scene(raw_scene)

        print(f"[VISION] Frame: {result.get('frame_data')}")
        print(f"[VISION] Detections: {result.get('detections')}")
        print(f"[VISION] Recognition: {result.get('recognition_result')}")

        response = result.get("response", {})
        text = response.get("text")

        if text:
            print(f"[VISION] {text}")

        self.brain.submit_vision_perception(result)
        self._execute_response_event(response)
        self.brain.perception_sync.consume()
        return result

    def voice_test(self, phrase: str) -> None:
        print(f"[VOICE_TEST] {phrase}")
        try:
            from voice.tts import TextToSpeech

            TextToSpeech().speak(phrase)
        except Exception as exc:
            print(f"[VOICE_TEST] Failed: {exc}")

    def print_vad_status(self) -> None:
        print("[VAD] Configuration")
        print(f" - MIC_CAPTURE_MODE={settings.MIC_CAPTURE_MODE}")
        print(f" - MIC_SAMPLE_RATE={settings.MIC_SAMPLE_RATE}")
        print(f" - MIC_RECORD_SECONDS={settings.MIC_RECORD_SECONDS}")
        print(f" - VAD_FRAME_MS={settings.VAD_FRAME_MS}")
        print(f" - VAD_MAX_RECORD_SECONDS={settings.VAD_MAX_RECORD_SECONDS}")
        print(f" - VAD_MIN_SPEECH_SECONDS={settings.VAD_MIN_SPEECH_SECONDS}")
        print(f" - VAD_SILENCE_MS={settings.VAD_SILENCE_MS}")
        print(f" - VAD_ENERGY_THRESHOLD={settings.VAD_ENERGY_THRESHOLD}")
        print(f" - VAD_NOISE_MULTIPLIER={settings.VAD_NOISE_MULTIPLIER}")

    def print_runtime_mode(self) -> None:
        print("[MODE] Runtime configuration")
        print(f" - RUNTIME_MODE={settings.RUNTIME_MODE}")
        print(f" - Voice: mic={settings.MIC_MODE}, speaker={settings.SPEAKER_MODE}, stt={settings.STT_MODE}, tts={settings.TTS_MODE}")
        print(f" - Vision: camera={settings.CAMERA_MODE}, detector={settings.DETECTOR_MODE}")
        print(f" - Hardware: {settings.HARDWARE_MODE}")
        print(f" - Motion: enabled={settings.MOTION_ENABLED}, dry_run={settings.MOTION_DRY_RUN}")
        print(f" - LLM: openai={settings.OPENAI_ENABLED}, ollama={settings.OLLAMA_ENABLED}")

    def mic_test(self) -> dict:
        packet = self.voice_pipeline.stt.microphone_connector.capture("")
        print(f"[MIC_TEST] Source: {packet.get('audio_source')}")
        print(f"[MIC_TEST] VAD detected: {packet.get('vad_detected')}")
        print(f"[MIC_TEST] Duration: {packet.get('vad_duration', 0):.2f}s")
        print(f"[MIC_TEST] Threshold: {packet.get('vad_threshold')}")
        print(f"[MIC_TEST] Noise floor: {packet.get('vad_noise_floor')}")
        print(f"[MIC_TEST] Audio bytes: {len(packet.get('audio_data') or b'')}")
        if packet.get("error"):
            print(f"[MIC_TEST] Error: {packet.get('error')}")
        return packet

    def camera_test(self, scene: str = "") -> dict:
        result = self.handle_vision_input(scene)
        self.save_last_frame(result)
        return result

    def save_last_frame(self, vision_packet: dict) -> None:
        frame_data = vision_packet.get("frame_data", {})
        frame = frame_data.get("frame")

        if frame is None:
            print("[CAMERA_TEST] No image frame to save")
            return

        output_path = Path(LAST_FRAME_PATH)
        if not output_path.is_absolute():
            output_path = PROJECT_ROOT / output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            import cv2

            cv2.imwrite(str(output_path), frame)
            print(f"[CAMERA_TEST] Saved frame: {output_path}")
        except Exception as exc:
            print(f"[CAMERA_TEST] Failed to save frame: {exc}")

    def _execute_response_event(self, response: dict) -> None:
        event = response.get("event")

        if not event:
            return

        play_event_sound(event)
        self.brain.process_event(event)
        self.brain.run_all_actions()

    def print_sound_list(self) -> None:
        sounds = list_sounds()
        if not sounds:
            print("[SOUND] No audio files found.")
            return

        print("[SOUND] Available sounds:")
        for name, entry in sorted(sounds.items()):
            print(f" - {name}: {entry.path.name} ({entry.source})")
