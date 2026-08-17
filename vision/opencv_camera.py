from vision.vision_config import OPENCV_CAMERA_INDEX


class OpenCVCamera:
    def capture(self, scene_description: str = "") -> dict:
        try:
            import cv2
        except ImportError:
            print("[OPENCV_CAMERA] OpenCV is not installed")
            return {
                "scene": scene_description.strip(),
                "source": "opencv_camera_unavailable",
                "frame": None,
            }

        cap = cv2.VideoCapture(OPENCV_CAMERA_INDEX)

        if not cap.isOpened():
            print("[OPENCV_CAMERA] Failed to open camera")
            return {
                "scene": scene_description.strip(),
                "source": "opencv_camera_failed",
                "frame": None,
            }

        ok, frame = cap.read()
        cap.release()

        if not ok:
            print("[OPENCV_CAMERA] Failed to read frame")
            return {
                "scene": scene_description.strip(),
                "source": "opencv_frame_failed",
                "frame": None,
            }

        return {
            "scene": scene_description.strip(),
            "source": "opencv_camera",
            "frame": frame,
        }