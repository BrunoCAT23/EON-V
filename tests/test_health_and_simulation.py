import os
import unittest

os.environ["MEMORY_SANDBOX"] = "true"
os.environ["SPEAKER_MODE"] = "stub"
os.environ["STARTUP_SOUND_ENABLED"] = "false"
os.environ["SOUND_EFFECTS_ENABLED"] = "false"

from tools.healthcheck import main as healthcheck_main
from tools.simulate_eon import main as simulate_main


class HealthAndSimulationTests(unittest.TestCase):
    def test_healthcheck_passes(self) -> None:
        self.assertEqual(healthcheck_main(), 0)

    def test_simulation_passes(self) -> None:
        self.assertEqual(simulate_main([]), 0)


if __name__ == "__main__":
    unittest.main()
