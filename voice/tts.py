from voice.tts_connector import TTSConnector
from voice.speaker_connector import SpeakerConnector


class TextToSpeech:
    def __init__(self) -> None:
        self.tts_connector = TTSConnector()
        self.speaker_connector = SpeakerConnector()

    def speak(self, text: str) -> None:
        audio_text = self.tts_connector.synthesize(text)
        if audio_text:
            self.speaker_connector.play(audio_text)
