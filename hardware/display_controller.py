class DisplayController:
    def __init__(self) -> None:
        self.current_face = "neutral"

    def show_emotion(self, emotion: str) -> None:
        self.current_face = emotion
        print(f"[DISPLAY_CONTROLLER] Showing emotion: {emotion}")

    def show_text(self, text: str) -> None:
        print(f"[DISPLAY_CONTROLLER] Text on display: {text}")

    def get_current_face(self) -> str:
        return self.current_face