from hardware.hardware_config import AUDIO_CONFIG
from voice.voice_profile import VoiceProfile


class AudioDriver:
    def __init__(self) -> None:
        self.config = AUDIO_CONFIG
        self.voice_profile = VoiceProfile()

    def speak(self, text: str) -> None:
        print(f"[AUDIO_DRIVER] {self.voice_profile.shape_text(text)}")

    def beep(self) -> None:
        print("[AUDIO_DRIVER] beep")
