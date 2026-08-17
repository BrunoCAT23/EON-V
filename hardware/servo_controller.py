class ServoController:
    def __init__(self) -> None:
        self.head_position = "center"

    def track_face(self) -> None:
        self.head_position = "tracking"
        print("[SERVO_CONTROLLER] Head tracking face")

    def idle_motion(self) -> None:
        self.head_position = "idle_scan"
        print("[SERVO_CONTROLLER] Small idle head motion")

    def set_head_position(self, position: str) -> None:
        self.head_position = position
        print(f"[SERVO_CONTROLLER] Head moved to: {position}")

    def get_head_position(self) -> str:
        return self.head_position