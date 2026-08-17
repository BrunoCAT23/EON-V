from settings import VOICE_PITCH, VOICE_PROFILE, VOICE_RATE, VOICE_STYLE


class VoiceProfile:
    def __init__(self) -> None:
        self.profile = VOICE_PROFILE
        self.style = VOICE_STYLE
        self.rate = VOICE_RATE
        self.pitch = VOICE_PITCH

    def shape_text(self, text: str) -> str:
        if not text or self.profile != "cinematic_ai":
            return text

        if len(text) <= 180:
            return text

        return text[:177].rstrip() + "..."

    def snapshot(self) -> dict:
        return {
            "profile": self.profile,
            "style": self.style,
            "rate": self.rate,
            "pitch": self.pitch,
        }
