import os
import unittest

os.environ["MEMORY_SANDBOX"] = "true"
os.environ["MIC_MODE"] = "mic_ready"
os.environ["STT_MODE"] = "local_ready"
os.environ["TTS_MODE"] = "fallback"
os.environ["SPEAKER_MODE"] = "stub"

from voice.mic_ready_input import MicReadyInput
from voice.stt_connector import STTConnector
from voice.tts import TextToSpeech
from voice.vad_recorder import EnergyVoiceActivityDetector


class VoiceConnectorTests(unittest.TestCase):
    def test_mic_ready_manual_text_bypass(self) -> None:
        packet = MicReadyInput().capture("eon привіт")

        self.assertEqual(packet["audio_source"], "manual_text")
        self.assertEqual(packet["raw_text"], "eon привіт")

    def test_local_ready_stt_accepts_manual_text(self) -> None:
        text = STTConnector().transcribe(
            {
                "audio_source": "manual_text",
                "raw_text": "eon привіт",
                "audio_data": None,
            }
        )

        self.assertEqual(text, "eon привіт")

    def test_text_to_speech_fallback_is_safe(self) -> None:
        TextToSpeech().speak("тест")

    def test_energy_vad_detects_loud_frame(self) -> None:
        vad = EnergyVoiceActivityDetector(energy_threshold=100)
        silence = b"\x00\x00" * 160
        loud = (1200).to_bytes(2, byteorder="little", signed=True) * 160

        vad.calibrate([silence, silence])

        self.assertFalse(vad.analyze(silence).is_speech)
        self.assertTrue(vad.analyze(loud).is_speech)
        self.assertGreaterEqual(vad.threshold(), 100)


if __name__ == "__main__":
    unittest.main()
