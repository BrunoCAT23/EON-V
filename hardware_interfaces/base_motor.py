class BaseMotor:
    def stop(self) -> None:
        raise NotImplementedError

    def sleep_mode(self) -> None:
        raise NotImplementedError

    def move(self, direction: str) -> None:
        raise NotImplementedError

    def get_motion_state(self) -> str:
        raise NotImplementedError