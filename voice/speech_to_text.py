from voice.microphone_connector import MicrophoneConnector
from voice.stt_connector import STTConnector


class SpeechToText:
    def __init__(self) -> None:
        self.microphone_connector = MicrophoneConnector()
        self.stt_connector = STTConnector()

    def transcribe(self, raw_input: str) -> str:
        audio_packet = self.microphone_connector.capture(raw_input)
        return self.stt_connector.transcribe(audio_packet)