from voice.audio_config import SPEAKER_MODE
from voice.stub_speaker import StubSpeaker


class SpeakerConnector:
    def __init__(self) -> None:
        if SPEAKER_MODE == "real_ready":
            self.speaker = StubSpeaker()
        else:
            self.speaker = StubSpeaker()

    def play(self, text: str) -> None:
        self.speaker.play(text)