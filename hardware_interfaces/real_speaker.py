from hardware_interfaces.base_speaker import BaseSpeaker
from pi_bindings.audio_binding import AudioBinding


class RealSpeaker(BaseSpeaker):
    def __init__(self) -> None:
        self.binding = AudioBinding()

    def speak(self, text: str) -> None:
        self.binding.speak(text)

    def beep(self, sound_name: str = "default") -> None:
        self.binding.beep(sound_name)

    def get_last_spoken_text(self) -> str | None:
        return self.binding.get_last_spoken_text()