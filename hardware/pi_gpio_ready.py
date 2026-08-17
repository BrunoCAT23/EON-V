from typing import Optional


class PiGPIOReady:
    def __init__(self) -> None:
        self.available: bool = False
        self.gpio: Optional[object] = None

        try:
            import importlib

            gpio_module = importlib.import_module("RPi.GPIO")
            self.gpio = gpio_module

            # type: ignore
            self.gpio.setmode(self.gpio.BCM)

            self.available = True
            print("[PI_GPIO] RPi.GPIO loaded successfully")

        except Exception as exc:
            print(f"[PI_GPIO] GPIO unavailable (expected on PC): {exc}")

    def setup_output(self, pin: int) -> None:
        if not self.available or self.gpio is None:
            print(f"[PI_GPIO] setup_output skipped for pin {pin}")
            return

        # type: ignore
        self.gpio.setup(pin, self.gpio.OUT)

    def setup_input(self, pin: int) -> None:
        if not self.available or self.gpio is None:
            print(f"[PI_GPIO] setup_input skipped for pin {pin}")
            return

        # type: ignore
        self.gpio.setup(pin, self.gpio.IN)

    def write(self, pin: int, value: int) -> None:
        if not self.available or self.gpio is None:
            print(f"[PI_GPIO] write skipped for pin {pin} value {value}")
            return

        # type: ignore
        self.gpio.output(pin, value)

    def read(self, pin: int) -> int:
        if not self.available or self.gpio is None:
            print(f"[PI_GPIO] read skipped for pin {pin}")
            return 0

        # type: ignore
        return self.gpio.input(pin)

    def cleanup(self) -> None:
        if self.available and self.gpio is not None:
            # type: ignore
            self.gpio.cleanup()
            print("[PI_GPIO] cleanup done")