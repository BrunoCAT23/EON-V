from hardware.hardware_config import ARDUINO_CONFIG


class SerialReady:
    def __init__(self) -> None:
        self.serial_conn = None
        self.available = False

        try:
            import serial
            self.serial_conn = serial.Serial(
                ARDUINO_CONFIG["port"],
                ARDUINO_CONFIG["baudrate"],
                timeout=ARDUINO_CONFIG["timeout"],
            )
            self.available = True
            print("[SERIAL_READY] Serial connected")
        except Exception as exc:
            print(f"[SERIAL_READY] Serial unavailable: {exc}")

    def write_line(self, text: str) -> None:
        if not self.available or self.serial_conn is None:
            print(f"[SERIAL_READY] write skipped: {text.strip()}")
            return

        self.serial_conn.write(text.encode("utf-8"))

    def read_line(self) -> str:
        if not self.available or self.serial_conn is None:
            print("[SERIAL_READY] read skipped")
            return "NO_RESPONSE"

        try:
            return self.serial_conn.readline().decode("utf-8").strip()
        except Exception as exc:
            print(f"[SERIAL_READY] read error: {exc}")
            return "READ_ERROR"

    def close(self) -> None:
        if self.serial_conn is not None:
            self.serial_conn.close()
            print("[SERIAL_READY] Serial closed")