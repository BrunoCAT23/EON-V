class FallbackDetector:
    def detect(self, frame_data: dict) -> list[dict]:
        return [
            {
                "label": "unknown_object",
                "confidence": 0.10,
                "bbox": [0, 0, 0, 0],
            }
        ]