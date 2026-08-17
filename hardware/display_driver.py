from hardware.hardware_config import DISPLAY_CONFIG


class DisplayDriver:
    def __init__(self) -> None:
        self.config = DISPLAY_CONFIG

    def show_text(self, text: str) -> None:
        print(f"[DISPLAY_DRIVER] TEXT: {text}")

    def show_emotion(self, emotion: str) -> None:
        print(f"[DISPLAY_DRIVER] EMOTION: {emotion}")

    def clear(self) -> None:
        print("[DISPLAY_DRIVER] clear")