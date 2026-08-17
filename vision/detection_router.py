from vision.detector_connector import DetectorConnector


class DetectionRouter:
    def __init__(self) -> None:
        self.detector_connector = DetectorConnector()

    def detect(self, frame_data: dict) -> list[dict]:
        return self.detector_connector.detect(frame_data)