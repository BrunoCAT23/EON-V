from settings import SPEAKER_MODE
from hardware.safety_guard import HardwareSafetyGuard
from voice.voice_profile import VoiceProfile


class SimulationHardware:
    def __init__(self) -> None:
        self.safety_guard = HardwareSafetyGuard()
        self.voice_profile = VoiceProfile()

    def get_status(self):
        return {
            "mode": "simulation",
            "display": "mock",
            "audio": "piper_or_text_fallback",
            "voice_profile": self.voice_profile.snapshot(),
            "motors": "mock",
            "servos": "mock",
            "safety": self.safety_guard.status(),
        }

    def get_device_map(self):
        return {
            "display": "simulation_display",
            "speaker": "simulation_speaker",
            "head_servo": "simulation_head_servo",
            "drive": "simulation_drive",
        }

    def show_emotion(self, value):
        print(f"[EON-V EMOTION]: {value}")

    def speak(self, text):
        text = self.voice_profile.shape_text(text)
        print(f"[EON-V VOICE]: {text}")
        if SPEAKER_MODE != "real_ready":
            return

        try:
            from voice_ai import speak as ai_speak
            ai_speak(text)
        except Exception as exc:
            print(f"[EON-V AUDIO_FALLBACK]: {exc}")

    def voice_reply(self, text):
        self.speak(text)  # ← використовує той самий метод

    def track_face(self):
        if not self.safety_guard.allow_motion():
            return
        print("[EON-V VISION]: tracking face")

    def gentle_track(self):
        if not self.safety_guard.allow_motion():
            return
        print("[EON-V VISION]: gentle tracking")

    def soft_idle(self):
        if not self.safety_guard.allow_motion():
            return
        print("[EON-V IDLE]: soft idle")

    def set_head_position(self, value):
        if not self.safety_guard.allow_motion():
            return
        print(f"[EON-V SERVO]: head position {value}")

    def listen(self):
        print("[EON-V AUDIO]: listening...")

    def sleep_mode(self):
        print("[EON-V SLEEP]: going to sleep")

    def idle_animation(self):
        print("[EON-V IDLE]: idle animation")

    def alert(self, text):
        print(f"[ALERT]: {text}")

    def log(self, text):
        print(f"[LOG]: {text}")

    def stop_motion(self):
        print("[EON-V MOTION]: stop")

    def move_forward(self, speed: int = 50):
        if not self.safety_guard.allow_motion():
            return
        print(f"[EON-V MOTION]: forward speed {speed}")

    def move_backward(self, speed: int = 50):
        if not self.safety_guard.allow_motion():
            return
        print(f"[EON-V MOTION]: backward speed {speed}")

    def turn_left(self, speed: int = 50):
        if not self.safety_guard.allow_motion():
            return
        print(f"[EON-V MOTION]: turn left speed {speed}")

    def turn_right(self, speed: int = 50):
        if not self.safety_guard.allow_motion():
            return
        print(f"[EON-V MOTION]: turn right speed {speed}")

    def emergency_stop(self, reason: str = "manual"):
        self.safety_guard.emergency_stop.trigger(reason)
        self.stop_motion()

    def reset_emergency_stop(self):
        self.safety_guard.emergency_stop.reset()
