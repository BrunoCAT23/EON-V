class DetectorBackend:
    def detect(self, frame_data: dict) -> list[dict]:
        raise NotImplementedError("Detector backend must implement detect()")