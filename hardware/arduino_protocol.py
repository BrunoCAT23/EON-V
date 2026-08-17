class ArduinoProtocol:
    def build_move_forward(self, speed: int = 60) -> str:
        return f"MOVE FORWARD {speed}\n"

    def build_move_backward(self, speed: int = 60) -> str:
        return f"MOVE BACKWARD {speed}\n"

    def build_turn_left(self, speed: int = 50) -> str:
        return f"TURN LEFT {speed}\n"

    def build_turn_right(self, speed: int = 50) -> str:
        return f"TURN RIGHT {speed}\n"

    def build_stop(self) -> str:
        return "STOP\n"

    def build_head_center(self) -> str:
        return "HEAD CENTER\n"

    def build_head_left(self) -> str:
        return "HEAD LEFT\n"

    def build_head_right(self) -> str:
        return "HEAD RIGHT\n"

    def build_head_down(self) -> str:
        return "HEAD DOWN\n"

    def build_ping(self) -> str:
        return "PING\n"