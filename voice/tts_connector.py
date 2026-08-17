from voice.audio_config import TTS_MODE
from voice.fallback_tts import FallbackTTS
from voice.voice_profile import VoiceProfile


class TTSConnector:
    def __init__(self) -> None:
        self.fallback = FallbackTTS()
        self.voice_profile = VoiceProfile()

    def synthesize(self, text: str) -> str:
        text = self.voice_profile.shape_text(text)

        if TTS_MODE == "fallback":
            return self.fallback.synthesize(text)

        if TTS_MODE == "local_ready":
            try:
                from voice_ai import speak

                speak(text)
                return ""
            except Exception as exc:
                print(f"[TTS_CONNECTOR] Local TTS failed: {exc}")
                return self.fallback.synthesize(text)

        print(f"[TTS_CONNECTOR] TTS mode '{TTS_MODE}' not connected yet")
        return self.fallback.synthesize(text)
