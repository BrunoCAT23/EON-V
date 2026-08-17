from __future__ import annotations

import audioop
from collections import deque
from dataclasses import dataclass

from settings import (
    MIC_SAMPLE_RATE,
    VAD_CALIBRATION_MS,
    VAD_ENERGY_THRESHOLD,
    VAD_FRAME_MS,
    VAD_MAX_RECORD_SECONDS,
    VAD_MIN_SPEECH_SECONDS,
    VAD_NOISE_MULTIPLIER,
    VAD_PREROLL_MS,
    VAD_SILENCE_MS,
)


@dataclass(frozen=True)
class VADDecision:
    is_speech: bool
    rms: int
    threshold: int


class EnergyVoiceActivityDetector:
    def __init__(
        self,
        energy_threshold: int = VAD_ENERGY_THRESHOLD,
        noise_multiplier: float = VAD_NOISE_MULTIPLIER,
    ) -> None:
        self.energy_threshold = energy_threshold
        self.noise_multiplier = noise_multiplier
        self.noise_floor = 0.0

    def calibrate(self, frames: list[bytes]) -> None:
        if not frames:
            self.noise_floor = 0.0
            return

        levels = [self.rms(frame) for frame in frames if frame]
        self.noise_floor = sum(levels) / len(levels) if levels else 0.0

    def threshold(self) -> int:
        adaptive = int(self.noise_floor * self.noise_multiplier)
        return max(self.energy_threshold, adaptive)

    def analyze(self, frame: bytes) -> VADDecision:
        rms = self.rms(frame)
        threshold = self.threshold()
        return VADDecision(rms >= threshold, rms, threshold)

    def rms(self, frame: bytes) -> int:
        if not frame:
            return 0
        return audioop.rms(frame, 2)


class VADRecorder:
    def __init__(self) -> None:
        self.sample_rate = MIC_SAMPLE_RATE
        self.frame_ms = max(10, VAD_FRAME_MS)
        self.frame_samples = int(self.sample_rate * self.frame_ms / 1000)
        self.detector = EnergyVoiceActivityDetector()

    def record(self) -> dict:
        try:
            import sounddevice as sd
        except Exception as exc:
            print(f"[VAD] sounddevice unavailable: {exc}")
            return self._failed_packet(str(exc))

        calibration_frames = max(1, VAD_CALIBRATION_MS // self.frame_ms)
        silence_frames_limit = max(1, VAD_SILENCE_MS // self.frame_ms)
        preroll_frames = max(1, VAD_PREROLL_MS // self.frame_ms)
        max_frames = max(1, int(VAD_MAX_RECORD_SECONDS * 1000 / self.frame_ms))
        min_speech_frames = max(1, int(VAD_MIN_SPEECH_SECONDS * 1000 / self.frame_ms))

        calibration: list[bytes] = []
        preroll: deque[bytes] = deque(maxlen=preroll_frames)
        captured: list[bytes] = []
        speech_frames = 0
        silence_frames = 0
        started = False

        print(
            "[VAD] Listening "
            f"max={VAD_MAX_RECORD_SECONDS:.1f}s, "
            f"silence={VAD_SILENCE_MS}ms, "
            f"frame={self.frame_ms}ms"
        )

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=self.frame_samples,
            ) as stream:
                for frame_index in range(max_frames):
                    frame, overflowed = stream.read(self.frame_samples)
                    frame_bytes = bytes(frame)

                    if overflowed:
                        print("[VAD] Input overflow")

                    if frame_index < calibration_frames:
                        calibration.append(frame_bytes)
                        preroll.append(frame_bytes)
                        if frame_index == calibration_frames - 1:
                            self.detector.calibrate(calibration)
                            print(
                                "[VAD] Calibrated "
                                f"noise={self.detector.noise_floor:.0f}, "
                                f"threshold={self.detector.threshold()}"
                            )
                        continue

                    decision = self.detector.analyze(frame_bytes)

                    if decision.is_speech:
                        if not started:
                            started = True
                            captured.extend(preroll)
                            print(f"[VAD] Speech started rms={decision.rms}")

                        captured.append(frame_bytes)
                        speech_frames += 1
                        silence_frames = 0
                    elif started:
                        captured.append(frame_bytes)
                        silence_frames += 1
                        if speech_frames >= min_speech_frames and silence_frames >= silence_frames_limit:
                            print("[VAD] Speech ended after silence")
                            break
                    else:
                        preroll.append(frame_bytes)

        except Exception as exc:
            print(f"[VAD] Recording error: {exc}")
            return self._failed_packet(str(exc))

        audio_data = b"".join(captured)
        duration = len(audio_data) / 2 / self.sample_rate if audio_data else 0.0

        return {
            "audio_source": "sounddevice_vad",
            "raw_text": "",
            "audio_data": audio_data,
            "sample_rate": self.sample_rate,
            "vad_detected": started,
            "vad_duration": duration,
            "vad_threshold": self.detector.threshold(),
            "vad_noise_floor": self.detector.noise_floor,
        }

    def _failed_packet(self, error: str) -> dict:
        return {
            "audio_source": "vad_failed",
            "raw_text": "",
            "audio_data": None,
            "sample_rate": self.sample_rate,
            "vad_detected": False,
            "error": error,
        }
