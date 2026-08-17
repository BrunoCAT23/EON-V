import time
from settings import RUNTIME_TICK_DELAY


class LifeLoop:
    def __init__(self, brain) -> None:
        self.brain = brain
        self.running = False
        self.tick_delay = RUNTIME_TICK_DELAY

    def start(self) -> None:
        print("[LIFE_LOOP] Starting...")
        self.running = True

        while self.running:
            self.brain.runtime_orchestrator.step(self.brain)
            time.sleep(self.tick_delay)

    def stop(self) -> None:
        print("[LIFE_LOOP] Stopping...")
        self.running = False
