from voice.audio_config import STT_MODE
from voice.fallback_stt import FallbackSTT
from voice.vosk_stt import VoskSTT


class STTConnector:
    def __init__(self) -> None:
        self.fallback = FallbackSTT()
        self.vosk = VoskSTT()

    def transcribe(self, audio_packet: dict) -> str:
        if STT_MODE == "fallback":
            return self.fallback.transcribe(audio_packet)

        if STT_MODE == "local_ready":
            result = self.vosk.transcribe(audio_packet)
            if result:
                return result
            return self.fallback.transcribe(audio_packet)

        print(f"[STT_CONNECTOR] STT mode '{STT_MODE}' not connected yet")
        return self.fallback.transcribe(audio_packet)
