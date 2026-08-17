from __future__ import annotations

import time

from settings import (
    LIVE_MAX_CYCLES,
    LIVE_RUNTIME_INTERVAL,
    LIVE_VISION_INTERVAL,
    LIVE_VOICE_INTERVAL,
)


class LiveRuntime:
    def __init__(self, app) -> None:
        self.app = app
        self.running = False

    def start(self, max_cycles: int | None = None, enable_voice: bool = True) -> None:
        if self.running:
            print("[LIVE] Already running")
            return

        cycle_limit = LIVE_MAX_CYCLES if max_cycles is None else max_cycles
        self.running = True

        if not self.app.brain.life_state.is_enabled():
            self.app.brain.life_state.enable()

        print("[LIVE] Started")
        print("[LIVE] Use Ctrl+C or estop from another control surface to stop.")

        last_voice = 0.0
        last_vision = 0.0
        last_runtime = 0.0
        cycles = 0

        try:
            while self.running:
                now = time.monotonic()

                if now - last_vision >= LIVE_VISION_INTERVAL:
                    self.app.vision_loop.run_once("")
                    last_vision = now

                if enable_voice and now - last_voice >= LIVE_VOICE_INTERVAL:
                    self.app.voice_loop.run_once("")
                    last_voice = now

                if now - last_runtime >= LIVE_RUNTIME_INTERVAL:
                    self.app.brain.runtime_orchestrator.step(self.app.brain)
                    last_runtime = now
                    cycles += 1

                if cycle_limit and cycles >= cycle_limit:
                    break

                time.sleep(0.05)
        except KeyboardInterrupt:
            print("[LIVE] Interrupted")
        finally:
            self.stop()

    def stop(self) -> None:
        if not self.running:
            return

        self.running = False
        self.app.brain.life_state.disable()
        print("[LIVE] Stopped")
