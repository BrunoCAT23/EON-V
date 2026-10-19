import os
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

os.environ["SOUND_EFFECTS_ENABLED"] = "false"
os.environ["STARTUP_SOUND_ENABLED"] = "false"

from sounds.sound_registry import list_sounds, resolve_sound


class SoundRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        fixture = Path(directory.name) / "freesound_community-robot-6282.wav"
        from sounds.startup_sound import generate_startup_sound
        generate_startup_sound(fixture)
        override = patch("sounds.sound_registry.SOUND_EFFECTS_DIR", directory.name)
        override.start()
        self.addCleanup(override.stop)

    def test_startup_alias_is_available(self) -> None:
        sounds = list_sounds()

        self.assertIn("startup", sounds)
        self.assertTrue(sounds["startup"].path.exists())

    def test_uploaded_robot_sound_is_registered(self) -> None:
        sounds = list_sounds()

        self.assertIn("robot", sounds)
        self.assertEqual(sounds["robot"].path.name, "freesound_community-robot-6282.wav")

    def test_event_prefix_resolves(self) -> None:
        entry = resolve_sound("recognized_pet dog")

        self.assertIsNotNone(entry)
        self.assertEqual(entry.path.name, "freesound_community-robot-6282.wav")


if __name__ == "__main__":
    unittest.main()
