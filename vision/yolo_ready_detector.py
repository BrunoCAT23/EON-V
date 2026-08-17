from vision.vision_config import YOLO_MODEL_PATH


class YOLOReadyDetector:
    def detect(self, frame_data: dict) -> list[dict] | None:
        frame = frame_data.get("frame")

        if frame is None:
            return None

        try:
            # Тут у майбутньому буде реальний inference
            # Наприклад: ONNX Runtime / Ultralytics / OpenCV DNN
            _ = YOLO_MODEL_PATH
            print("[YOLO_READY] Real YOLO backend not connected yet")
            return None
        except Exception as exc:
            print(f"[YOLO_READY] Error: {exc}")
            return None