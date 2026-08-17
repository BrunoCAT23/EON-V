from vision.vision_config import CAMERA_MODE
from vision.stub_camera import StubCamera
from vision.opencv_camera import OpenCVCamera


class CameraConnector:
    def __init__(self) -> None:
        if CAMERA_MODE == "opencv_ready":
            self.camera = OpenCVCamera()
        else:
            self.camera = StubCamera()

    def capture(self, scene_description: str) -> dict:
        return self.camera.capture(scene_description)