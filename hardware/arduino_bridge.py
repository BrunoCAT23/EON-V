from hardware.hardware_config import HARDWARE_MODE
from hardware.arduino_protocol import ArduinoProtocol
from hardware.mock_serial import MockSerial
from hardware.serial_ready import SerialReady


class ArduinoBridge:
    def __init__(self) -> None:
        self.protocol = ArduinoProtocol()

        if HARDWARE_MODE == "arduino_bridge":
            self.transport = SerialReady()
        else:
            self.transport = MockSerial()

    def send(self, command: str) -> str:
        self.transport.write_line(command)
        return self.transport.read_line()

    def move_forward(self, speed: int = 60) -> str:
        return self.send(self.protocol.build_move_forward(speed))

    def move_backward(self, speed: int = 60) -> str:
        return self.send(self.protocol.build_move_backward(speed))

    def turn_left(self, speed: int = 50) -> str:
        return self.send(self.protocol.build_turn_left(speed))

    def turn_right(self, speed: int = 50) -> str:
        return self.send(self.protocol.build_turn_right(speed))

    def stop(self) -> str:
        return self.send(self.protocol.build_stop())

    def head_center(self) -> str:
        return self.send(self.protocol.build_head_center())

    def head_left(self) -> str:
        return self.send(self.protocol.build_head_left())

    def head_right(self) -> str:
        return self.send(self.protocol.build_head_right())

    def head_down(self) -> str:
        return self.send(self.protocol.build_head_down())

    def ping(self) -> str:
        return self.send(self.protocol.build_ping())

    def close(self) -> None:
        self.transport.close()