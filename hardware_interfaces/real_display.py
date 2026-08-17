from hardware_interfaces.base_display import BaseDisplay


class RealDisplay(BaseDisplay):
    def __init__(self) -> None:
        self.current_face = "neutral"

    def show_emotion(self, emotion: str) -> None:
        self.current_face = emotion
        print(f"[REAL_DISPLAY_STUB] Would show emotion on real display: {emotion}")

    def show_text(self, text: str) -> None:
        print(f"[REAL_DISPLAY_STUB] Would show text on real display: {text}")

    def get_current_face(self) -> str:
        return self.current_face