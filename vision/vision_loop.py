from __future__ import annotations

import time


class VisionLoop:
    def __init__(self, app) -> None:
        self.app = app
        self.running = False

    def run_once(self, scene_description: str = "") -> dict:
        return self.app.handle_vision_input(scene_description)

    def run_forever(self, poll_delay: float = 0.5) -> None:
        self.running = True
        print("[VISION_LOOP] Started. Real camera capture must be connected by CAMERA_MODE.")

        while self.running:
            self.run_once("")
            time.sleep(poll_delay)

    def stop(self) -> None:
        self.running = False
        print("[VISION_LOOP] Stopped")
