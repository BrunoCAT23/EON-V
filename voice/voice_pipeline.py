import logging

from voice.wake_word import WakeWordDetector
from voice.speech_to_text import SpeechToText
from voice.intent_parser import IntentParser
from voice.response_generator import ResponseGenerator
from voice.tts import TextToSpeech


logger = logging.getLogger(__name__)


class VoicePipeline:
    def __init__(self) -> None:
        self.wake_word_detector = WakeWordDetector()
        self.stt = SpeechToText()
        self.intent_parser = IntentParser()
        self.response_generator = ResponseGenerator()
        self.tts = TextToSpeech()

    def process_raw_input(self, raw_input: str) -> dict:
        transcribed = self.stt.transcribe(raw_input)
        logger.info("voice.stt heard=%s", transcribed)

        if not self.wake_word_detector.detect(transcribed):
            logger.info("voice.wake_word detected=false")
            return {
                "heard": transcribed,
                "wake_word_detected": False,
                "intent_data": None,
                "response": {
                    "event": None,
                    "text": "Wake word not detected.",
                },
            }

        cleaned_text = self.wake_word_detector.remove_wake_word(transcribed)
        logger.info("voice.wake_word detected=true cleaned=%s", cleaned_text)
        intent_data = self.intent_parser.parse(cleaned_text)
        logger.info("voice.intent intent=%s", intent_data.get("intent"))
        response = self.response_generator.generate(intent_data)
        logger.info("voice.response event=%s", response.get("event"))

        return {
            "heard": transcribed,
            "wake_word_detected": True,
            "cleaned_text": cleaned_text,
            "intent_data": intent_data,
            "response": response,
        }

    def process_command_input(self, raw_input: str) -> dict:
        transcribed = self.stt.transcribe(raw_input)
        logger.info("voice.followup heard=%s", transcribed)
        intent_data = self.intent_parser.parse(transcribed)
        logger.info("voice.followup intent=%s", intent_data.get("intent"))
        response = self.response_generator.generate(intent_data)

        return {
            "heard": transcribed,
            "wake_word_detected": True,
            "cleaned_text": transcribed.strip().lower(),
            "intent_data": intent_data,
            "response": response,
            "wake_followup": True,
        }

    def speak(self, text: str) -> None:
        self.tts.speak(text)
