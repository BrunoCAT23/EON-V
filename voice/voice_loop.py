from __future__ import annotations

import time


class VoiceLoop:
    def __init__(self, app) -> None:
        self.app = app
        self.running = False

    def run_once(self, raw_input: str = "") -> dict:
        return self.app.handle_voice_input(raw_input)

    def run_forever(self, poll_delay: float = 0.2) -> None:
        self.running = True
        print("[VOICE_LOOP] Started. Real microphone capture must be connected by MIC_MODE.")

        while self.running:
            self.run_once("")
            time.sleep(poll_delay)

    def stop(self) -> None:
        self.running = False
        print("[VOICE_LOOP] Stopped")
