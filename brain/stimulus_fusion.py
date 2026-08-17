class StimulusFusion:
    def fuse(self, voice_packet: dict | None, vision_packet: dict | None) -> list[dict]:
        fused = []

        if voice_packet:
            fused.append(
                {
                    "channel": "voice",
                    "data": voice_packet,
                    "priority": 0.8 if voice_packet.get("wake_word_detected") else 0.3,
                }
            )

        if vision_packet:
            recognition = vision_packet.get("recognition_result", {})
            entity_type = recognition.get("entity_type")

            priority = 0.2
            if entity_type == "person":
                priority = 0.9
            elif entity_type == "pet":
                priority = 0.7

            fused.append(
                {
                    "channel": "vision",
                    "data": vision_packet,
                    "priority": priority,
                }
            )

        fused.sort(key=lambda item: item["priority"], reverse=True)
        return fused