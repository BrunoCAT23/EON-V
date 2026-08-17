from hardware.hardware_config import HEAD_SERVO_PIN
from hardware.safety_guard import HardwareSafetyGuard


class ServoDriver:
    def __init__(self, gpio_adapter) -> None:
        self.gpio = gpio_adapter
        self.pin = HEAD_SERVO_PIN
        self.safety_guard = HardwareSafetyGuard()
        self.gpio.setup_output(self.pin)

    def set_angle(self, angle: float) -> None:
        angle = self.safety_guard.clamp_servo_angle(angle)
        duty_cycle = 2.5 + (angle / 180.0) * 10.0
        self.gpio.pwm_change(self.pin, duty_cycle)
        print(f"[SERVO_DRIVER] angle={angle} duty={duty_cycle:.2f}")

    def center(self) -> None:
        self.set_angle(90.0)

    def look_left(self) -> None:
        self.set_angle(140.0)

    def look_right(self) -> None:
        self.set_angle(40.0)

    def look_down(self) -> None:
        self.set_angle(70.0)
