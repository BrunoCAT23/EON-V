class StubDetector:
    def detect(self, frame_data) -> list[dict]:
        if isinstance(frame_data, str):
            scene = frame_data.lower()
        else:
            scene = frame_data.get("scene", "").lower()

        detections = []

        if any(word in scene for word in ["serhii", "andriy", "person", "людина"]):
            detections.append(
                {
                    "label": "person",
                    "confidence": 0.95,
                    "bbox": [100, 100, 220, 260],
                }
            )

        if any(word in scene for word in ["cat", "кіт", "кот"]):
            detections.append(
                {
                    "label": "cat",
                    "confidence": 0.91,
                    "bbox": [240, 120, 340, 240],
                }
            )

        if any(word in scene for word in ["dog", "собака", "пес"]):
            detections.append(
                {
                    "label": "dog",
                    "confidence": 0.93,
                    "bbox": [260, 130, 390, 270],
                }
            )

        if not detections:
            detections.append(
                {
                    "label": "unknown_object",
                    "confidence": 0.40,
                    "bbox": [0, 0, 0, 0],
                }
            )

        return detections