class ActionExecutor:
    def __init__(self, hardware_manager) -> None:
        self.hardware_manager = hardware_manager

    def execute(self, actions: list[dict]) -> None:
        if not actions:
            print("[ACTION] No actions to execute")
            return

        for action in actions:
            action_type = action.get("type")
            value = action.get("value", "")

            if action_type == "speak":
                self.hardware_manager.speak(value)

            elif action_type == "voice_reply":
                self.hardware_manager.speak(value)

            elif action_type == "show_emotion":
                self.hardware_manager.show_emotion(value)

            elif action_type == "track_face":
                self.hardware_manager.track_face()

            elif action_type == "gentle_track":
                self.hardware_manager.gentle_track()

            elif action_type == "listen":
                print("[AUDIO] Listening for speech")

            elif action_type == "sleep_mode":
                self.hardware_manager.sleep_mode()

            elif action_type == "idle_animation":
                self.hardware_manager.idle_animation()

            elif action_type == "soft_idle":
                self.hardware_manager.soft_idle()

            elif action_type == "alert":
                self.hardware_manager.alert(value)

            elif action_type == "log":
                print(f"[LOG] {value}")

            elif action_type == "set_head_position":
                self.hardware_manager.set_head_position(value)

            elif action_type == "move_forward":
                self.hardware_manager.move_forward(action.get("speed", 50))

            elif action_type == "move_backward":
                self.hardware_manager.move_backward(action.get("speed", 50))

            elif action_type == "turn_left":
                self.hardware_manager.turn_left(action.get("speed", 50))

            elif action_type == "turn_right":
                self.hardware_manager.turn_right(action.get("speed", 50))

            elif action_type == "stop_motion":
                self.hardware_manager.stop_motion()

            elif action_type == "visual_reply":
                print(f"[VISUAL] {value}")

            elif action_type == "gesture":
                print(f"[GESTURE] {value}")

            else:
                print(f"[ACTION] Unknown action: {action_type} ({value})")
