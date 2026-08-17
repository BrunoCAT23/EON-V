class MotorController:
    def __init__(self) -> None:
        self.motion_state = "stopped"

    def stop(self) -> None:
        self.motion_state = "stopped"
        print("[MOTOR_CONTROLLER] Motors stopped")

    def sleep_mode(self) -> None:
        self.motion_state = "sleep"
        print("[MOTOR_CONTROLLER] Entering sleep posture")

    def move(self, direction: str) -> None:
        self.motion_state = direction
        print(f"[MOTOR_CONTROLLER] Moving: {direction}")

    def get_motion_state(self) -> str:
        return self.motion_state