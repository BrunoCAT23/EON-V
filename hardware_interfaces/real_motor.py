from hardware_interfaces.base_motor import BaseMotor
from pi_bindings.gpio_motor_binding import GPIOMotorBinding


class RealMotor(BaseMotor):
    def __init__(self) -> None:
        self.binding = GPIOMotorBinding()

    def stop(self) -> None:
        self.binding.stop()

    def sleep_mode(self) -> None:
        self.binding.sleep_mode()

    def move(self, direction: str) -> None:
        self.binding.move(direction)

    def get_motion_state(self) -> str:
        return self.binding.get_motion_state()