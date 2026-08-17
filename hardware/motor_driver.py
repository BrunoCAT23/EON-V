from hardware.hardware_config import LEFT_MOTOR_PINS, RIGHT_MOTOR_PINS


class MotorDriver:
    def __init__(self, gpio_adapter) -> None:
        self.gpio = gpio_adapter
        self.left = LEFT_MOTOR_PINS
        self.right = RIGHT_MOTOR_PINS
        self._setup()

    def _setup(self) -> None:
        for pin in self.left.values():
            self.gpio.setup_output(pin)

        for pin in self.right.values():
            self.gpio.setup_output(pin)

    def stop(self) -> None:
        for pin in [self.left["in1"], self.left["in2"], self.right["in1"], self.right["in2"]]:
            self.gpio.write(pin, 0)

        print("[MOTOR_DRIVER] stop")

    def forward(self, speed: float = 60.0) -> None:
        self.gpio.write(self.left["in1"], 1)
        self.gpio.write(self.left["in2"], 0)
        self.gpio.write(self.right["in1"], 1)
        self.gpio.write(self.right["in2"], 0)
        self.gpio.pwm_change(self.left["enable"], speed)
        self.gpio.pwm_change(self.right["enable"], speed)
        print(f"[MOTOR_DRIVER] forward speed={speed}")

    def backward(self, speed: float = 60.0) -> None:
        self.gpio.write(self.left["in1"], 0)
        self.gpio.write(self.left["in2"], 1)
        self.gpio.write(self.right["in1"], 0)
        self.gpio.write(self.right["in2"], 1)
        self.gpio.pwm_change(self.left["enable"], speed)
        self.gpio.pwm_change(self.right["enable"], speed)
        print(f"[MOTOR_DRIVER] backward speed={speed}")

    def turn_left(self, speed: float = 50.0) -> None:
        self.gpio.write(self.left["in1"], 0)
        self.gpio.write(self.left["in2"], 1)
        self.gpio.write(self.right["in1"], 1)
        self.gpio.write(self.right["in2"], 0)
        self.gpio.pwm_change(self.left["enable"], speed)
        self.gpio.pwm_change(self.right["enable"], speed)
        print(f"[MOTOR_DRIVER] turn_left speed={speed}")

    def turn_right(self, speed: float = 50.0) -> None:
        self.gpio.write(self.left["in1"], 1)
        self.gpio.write(self.left["in2"], 0)
        self.gpio.write(self.right["in1"], 0)
        self.gpio.write(self.right["in2"], 1)
        self.gpio.pwm_change(self.left["enable"], speed)
        self.gpio.pwm_change(self.right["enable"], speed)
        print(f"[MOTOR_DRIVER] turn_right speed={speed}")