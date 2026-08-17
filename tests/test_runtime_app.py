import os
import unittest
from pathlib import Path

os.environ["MEMORY_SANDBOX"] = "true"
os.environ["SPEAKER_MODE"] = "stub"
os.environ["CAMERA_MODE"] = "stub"
os.environ["MIC_MODE"] = "stub"
os.environ["STARTUP_SOUND_ENABLED"] = "false"
os.environ["SOUND_EFFECTS_ENABLED"] = "false"

from runtime_app import RuntimeApp


class RuntimeAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = RuntimeApp()

    def test_voice_wake_word_flow_executes_actions(self) -> None:
        packet = self.app.handle_voice_input("eon привіт")

        self.assertTrue(packet["wake_word_detected"])
        self.assertEqual(self.app.brain.action_queue.snapshot(), [])

    def test_voice_without_wake_word_does_not_execute_event(self) -> None:
        packet = self.app.handle_voice_input("привіт")

        self.assertFalse(packet["wake_word_detected"])
        self.assertEqual(packet["response"]["event"], None)

    def test_wake_word_alone_acknowledges_without_command(self) -> None:
        packet = self.app.handle_voice_input("eon")

        self.assertTrue(packet["wake_word_detected"])
        self.assertEqual(packet["cleaned_text"], "")

    def test_do_not_disturb_ignores_voice_input(self) -> None:
        self.app.handle_command("dnd_on")
        packet = self.app.handle_voice_input("eon привіт")

        self.assertFalse(packet["wake_word_detected"])
        self.app.handle_command("dnd_off")

    def test_memory_context_command_runs(self) -> None:
        self.app.handle_voice_input("eon привіт")

        self.assertTrue(self.app.handle_command("memory_context"))
        self.assertEqual(self.app.brain.action_queue.snapshot(), [])

    def test_vad_status_command_runs(self) -> None:
        self.assertTrue(self.app.handle_command("vad_status"))

    def test_vision_pet_has_priority_over_known_person(self) -> None:
        self.app.handle_command("meet serhii")
        packet = self.app.handle_vision_input("dog near serhii")

        self.assertEqual(packet["recognition_result"]["entity_type"], "pet")
        self.assertEqual(packet["recognition_result"]["pet_type"], "dog")

    def test_emergency_stop_blocks_motion_until_reset(self) -> None:
        self.app.handle_command("estop test")

        guard = self.app.brain.hardware_manager.safety_guard
        self.assertTrue(guard.emergency_stop.is_active())

        self.app.handle_command("estop_reset")
        self.assertFalse(guard.emergency_stop.is_active())

    def test_camera_test_stub_is_safe(self) -> None:
        packet = self.app.camera_test("person in front of robot")

        self.assertIn("detections", packet)

    def test_live_test_runs_limited_cycles(self) -> None:
        self.app.handle_command("live_test 1")

        self.assertFalse(self.app.brain.life_state.is_enabled())

    def test_companion_profile_commands_update_memory(self) -> None:
        self.app.handle_command("meet serhii")
        self.app.handle_command("profile_set_name serhii Сергій")
        self.app.handle_command("profile_add_date serhii birthday 15-03")

        person = self.app.brain.memory_manager.get_people()["serhii"]
        self.assertEqual(person["preferred_name"], "сергій")
        self.assertEqual(person["important_dates"]["birthday"], "15-03")

    def test_tick_reminder_runs_when_due(self) -> None:
        self.app.handle_command("remind_in 1 перевірити заряд")
        self.app.handle_command("auto_on")
        self.app.handle_command("run_steps 1")
        self.app.handle_command("run_all")

        reminders = self.app.brain.schedule_manager.snapshot()
        self.assertTrue(reminders[0]["done"])
        self.assertEqual(self.app.brain.action_queue.snapshot(), [])

    def test_dashboard_command_generates_html(self) -> None:
        self.assertTrue(self.app.handle_command("dashboard"))
        self.assertTrue((Path(os.getcwd()) / "logs" / "dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
