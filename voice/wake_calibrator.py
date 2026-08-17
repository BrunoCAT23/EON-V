from __future__ import annotations

from pathlib import Path

from settings import ENV_FILE, WAKE_WORDS
from voice.speech_to_text import SpeechToText
from voice.wake_word import WakeWordDetector


class WakeCalibrator:
    def __init__(self) -> None:
        self.stt = SpeechToText()
        self.detector = WakeWordDetector()

    def calibrate_from_samples(self, samples: list[str]) -> list[str]:
        variants = set(word.strip() for word in WAKE_WORDS.split(",") if word.strip())

        for sample in samples:
            text = sample.strip().lower()
            if not text:
                continue

            first_word = text.split()[0].strip(" ,.!?-")
            if not first_word:
                continue

            if self.detector.detect(first_word) or len(first_word) <= 5:
                variants.add(first_word)

        ordered = sorted(variants, key=lambda item: (item not in ["eon", "еон"], item))
        self._write_wake_words(ordered)
        return ordered

    def calibrate_from_microphone(self, count: int) -> list[str]:
        samples = []
        for index in range(max(1, min(20, count))):
            print(f"[WAKE_CALIBRATE] Say EON sample {index + 1}/{count}")
            samples.append(self.stt.transcribe(""))
        return self.calibrate_from_samples(samples)

    def _write_wake_words(self, words: list[str], env_file: Path = ENV_FILE) -> None:
        line = f"WAKE_WORDS={','.join(words)}"

        if not env_file.exists():
            env_file.write_text(line + "\n", encoding="utf-8")
            return

        lines = env_file.read_text(encoding="utf-8").splitlines()
        for index, current in enumerate(lines):
            if current.startswith("WAKE_WORDS="):
                lines[index] = line
                break
        else:
            lines.append(line)

        env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
