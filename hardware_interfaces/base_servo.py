class BaseServo:
    def track_face(self) -> None:
        raise NotImplementedError

    def idle_motion(self) -> None:
        raise NotImplementedError

    def set_head_position(self, position: str) -> None:
        raise NotImplementedError

    def get_head_position(self) -> str:
        raise NotImplementedError