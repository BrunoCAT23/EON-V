from vision.camera_connector import CameraConnector


class FrameInput:
    def __init__(self) -> None:
        self.camera_connector = CameraConnector()

    def capture(self, scene_description: str) -> dict:
        return self.camera_connector.capture(scene_description)