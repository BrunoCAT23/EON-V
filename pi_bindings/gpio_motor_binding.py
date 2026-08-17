from pi_bindings.pi_env import safe_import


class GPIOMotorBinding:
    def __init__(self) -> None:
        self.gpiozero_available = safe_import("gpiozero")
        self.motion_state = "stopped"

    def move(self, direction: str) -> None:
        self.motion_state = direction

        if self.gpiozero_available:
            print(f"[GPIO_MOTOR_BINDING] Real motor move via gpiozero: {direction}")
        else:
            print(f"[GPIO_MOTOR_BINDING_STUB] Would move motor: {direction}")

    def stop(self) -> None:
        self.motion_state = "stopped"

        if self.gpiozero_available:
            print("[GPIO_MOTOR_BINDING] Real motor stop via gpiozero")
        else:
            print("[GPIO_MOTOR_BINDING_STUB] Would stop motor")

    def sleep_mode(self) -> None:
        self.motion_state = "sleep"

        if self.gpiozero_available:
            print("[GPIO_MOTOR_BINDING] Real motor sleep mode")
        else:
            print("[GPIO_MOTOR_BINDING_STUB] Would enter motor sleep mode")

    def get_motion_state(self) -> str:
        return self.motion_state