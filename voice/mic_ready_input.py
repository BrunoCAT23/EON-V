class MicReadyInput:
    def capture(self, raw_input: str = "") -> dict:
        if raw_input.strip():
            return {
                "audio_source": "manual_text",
                "raw_text": raw_input.strip(),
                "audio_data": None,
            }

        try:
            import sounddevice as sd
            from settings import MIC_CAPTURE_MODE, MIC_RECORD_SECONDS, MIC_SAMPLE_RATE

            if MIC_CAPTURE_MODE == "vad":
                from voice.vad_recorder import VADRecorder

                return VADRecorder().record()

            print(f"[MIC_READY] Recording {MIC_RECORD_SECONDS:.1f}s at {MIC_SAMPLE_RATE} Hz")
            recording = sd.rec(
                int(MIC_RECORD_SECONDS * MIC_SAMPLE_RATE),
                samplerate=MIC_SAMPLE_RATE,
                channels=1,
                dtype="int16",
            )
            sd.wait()

            return {
                "audio_source": "sounddevice",
                "raw_text": "",
                "audio_data": recording.tobytes(),
                "sample_rate": MIC_SAMPLE_RATE,
            }
        except Exception as exc:
            print(f"[MIC_READY] Error: {exc}")
            return {
                "audio_source": "mic_ready_failed",
                "raw_text": raw_input.strip(),
                "audio_data": None,
            }
