class BaseDisplay:
    def show_emotion(self, emotion: str) -> None:
        raise NotImplementedError

    def show_text(self, text: str) -> None:
        raise NotImplementedError

    def get_current_face(self) -> str:
        raise NotImplementedError