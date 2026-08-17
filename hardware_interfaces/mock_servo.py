from hardware_interfaces.base_servo import BaseServo


class MockServo(BaseServo):
    def __init__(self) -> None:
        self.head_position = "center"

    def track_face(self) -> None:
        self.head_position = "tracking"
        print("[MOCK_SERVO] Tracking face")

    def idle_motion(self) -> None:
        self.head_position = "idle_scan"
        print("[MOCK_SERVO] Idle motion")

    def set_head_position(self, position: str) -> None:
        self.head_position = position
        print(f"[MOCK_SERVO] Set head position: {position}")

    def get_head_position(self) -> str:
        return self.head_position