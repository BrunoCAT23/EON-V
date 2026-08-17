class MockGPIO:
    def setup_output(self, pin: int) -> None:
        print(f"[MOCK_GPIO] setup output pin {pin}")

    def write(self, pin: int, value: int) -> None:
        print(f"[MOCK_GPIO] write pin {pin} -> {value}")

    def pwm_start(self, pin: int, duty_cycle: float) -> None:
        print(f"[MOCK_GPIO] pwm start pin {pin} duty={duty_cycle}")

    def pwm_change(self, pin: int, duty_cycle: float) -> None:
        print(f"[MOCK_GPIO] pwm change pin {pin} duty={duty_cycle}")

    def cleanup(self) -> None:
        print("[MOCK_GPIO] cleanup")