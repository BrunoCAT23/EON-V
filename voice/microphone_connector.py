from voice.audio_config import MIC_MODE
from voice.stub_microphone import StubMicrophone
from voice.mic_ready_input import MicReadyInput


class MicrophoneConnector:
    def __init__(self) -> None:
        if MIC_MODE == "mic_ready":
            self.microphone = MicReadyInput()
        else:
            self.microphone = StubMicrophone()

    def capture(self, raw_input: str = "") -> dict:
        return self.microphone.capture(raw_input)