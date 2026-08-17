class AudioBinding:
    def __init__(self) -> None:
        self.last_spoken_text = None

    def speak(self, text: str) -> None:
        self.last_spoken_text = text
        print(f"[AUDIO_BINDING_STUB] Would output audio: {text}")

    def beep(self, sound_name: str = "default") -> None:
        print(f"[AUDIO_BINDING_STUB] Would play beep: {sound_name}")

    def get_last_spoken_text(self) -> str | None:
        return self.last_spoken_text