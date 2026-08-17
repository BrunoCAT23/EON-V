from hardware_interfaces.base_motor import BaseMotor


class MockMotor(BaseMotor):
    def __init__(self) -> None:
        self.motion_state = "stopped"

    def stop(self) -> None:
        self.motion_state = "stopped"
        print("[MOCK_MOTOR] Stop")

    def sleep_mode(self) -> None:
        self.motion_state = "sleep"
        print("[MOCK_MOTOR] Sleep mode")

    def move(self, direction: str) -> None:
        self.motion_state = direction
        print(f"[MOCK_MOTOR] Move: {direction}")

    def get_motion_state(self) -> str:
        return self.motion_state