class PerceptionSync:
    def __init__(self) -> None:
        self.last_voice_packet = None
        self.last_vision_packet = None

    def update_voice(self, packet: dict) -> None:
        self.last_voice_packet = packet

    def update_vision(self, packet: dict) -> None:
        self.last_vision_packet = packet

    def consume(self) -> tuple[dict | None, dict | None]:
        voice = self.last_voice_packet
        vision = self.last_vision_packet

        self.last_voice_packet = None
        self.last_vision_packet = None

        return voice, vision