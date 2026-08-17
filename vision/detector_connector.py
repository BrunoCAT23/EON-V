from vision.vision_config import DETECTOR_MODE
from vision.stub_detector import StubDetector
from vision.yolo_ready_detector import YOLOReadyDetector
from vision.fallback_detector import FallbackDetector


class DetectorConnector:
    def __init__(self) -> None:
        self.fallback = FallbackDetector()

        if DETECTOR_MODE == "yolo_ready":
            self.detector = YOLOReadyDetector()
        else:
            self.detector = StubDetector()

    def detect(self, frame_data: dict) -> list[dict]:
        result = self.detector.detect(frame_data)

        if result is None:
            return self.fallback.detect(frame_data)

        return result