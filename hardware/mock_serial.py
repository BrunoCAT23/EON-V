class MockSerial:
    def write_line(self, text: str) -> None:
        print(f"[MOCK_SERIAL] >> {text.strip()}")

    def read_line(self) -> str:
        response = "OK"
        print(f"[MOCK_SERIAL] << {response}")
        return response

    def close(self) -> None:
        print("[MOCK_SERIAL] closed")