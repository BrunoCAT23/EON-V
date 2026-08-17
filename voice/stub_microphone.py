class StubMicrophone:
    def capture(self, raw_input: str = "") -> dict:
        return {
            "audio_source": "stub_microphone",
            "raw_text": raw_input.strip(),
            "audio_data": None,
        }