class FallbackSTT:
    def transcribe(self, audio_packet: dict) -> str:
        return audio_packet.get("raw_text", "").strip()