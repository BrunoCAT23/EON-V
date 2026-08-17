from hardware.hardware_config import HARDWARE_MODE
from hardware.mock_gpio import MockGPIO
from hardware.pi_gpio_ready import PiGPIOReady


class GPIOAdapter:
    def __init__(self) -> None:
        if HARDWARE_MODE == "pi_ready":
            self.backend = PiGPIOReady()
        else:
            self.backend = MockGPIO()

    def setup_output(self, pin: int) -> None:
        self.backend.setup_output(pin)

    def write(self, pin: int, value: int) -> None:
        self.backend.write(pin, value)

    def pwm_start(self, pin: int, duty_cycle: float) -> None:
        self.backend.pwm_start(pin, duty_cycle)

    def pwm_change(self, pin: int, duty_cycle: float) -> None:
        self.backend.pwm_change(pin, duty_cycle)

    def cleanup(self) -> None:
        self.backend.cleanup()