import json
from pathlib import Path

from settings import PROJECT_ROOT, VOSK_MODEL_PATH


class VoskSTT:
    def __init__(self) -> None:
        self.model = None

    def _model_path(self) -> Path:
        path = Path(VOSK_MODEL_PATH)
        if path.is_absolute():
            return path
        return PROJECT_ROOT / path

    def _load_model(self):
        if self.model is not None:
            return self.model

        from vosk import Model

        self.model = Model(str(self._model_path()))
        return self.model

    def transcribe(self, audio_packet: dict) -> str | None:
        raw_text = audio_packet.get("raw_text", "").strip()
        if raw_text:
            return raw_text

        audio_data = audio_packet.get("audio_data")
        if not audio_data:
            return None

        try:
            from vosk import KaldiRecognizer
        except ImportError:
            print("[VOSK_STT] vosk is not installed")
            return None

        try:
            sample_rate = int(audio_packet.get("sample_rate", 16000))
            recognizer = KaldiRecognizer(self._load_model(), sample_rate)
            recognizer.AcceptWaveform(audio_data)
            result = json.loads(recognizer.FinalResult())
            return result.get("text", "").strip()
        except Exception as exc:
            print(f"[VOSK_STT] Error: {exc}")
            return None
