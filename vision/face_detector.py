class FaceDetector:
    def detect(self, frame_data: str) -> dict:
        keywords = ["face", "person", "human", "serhii", "olena", "unknown"]

        has_face = any(word in frame_data for word in keywords)

        return {
            "face_detected": has_face,
            "raw_frame": frame_data
        }