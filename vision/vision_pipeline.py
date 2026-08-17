from vision.frame_input import FrameInput
from vision.detection_router import DetectionRouter
from vision.person_recognizer import PersonRecognizer
from vision.visual_event_generator import VisualEventGenerator


class VisionPipeline:
    def __init__(self) -> None:
        self.frame_input = FrameInput()
        self.detection_router = DetectionRouter()
        self.person_recognizer = PersonRecognizer()
        self.visual_event_generator = VisualEventGenerator()

    def update_known_people(self, known_people: list[str]) -> None:
        self.person_recognizer.update_known_people(known_people)

    def update_known_pets(self, known_pets: dict) -> None:
        self.person_recognizer.update_known_pets(known_pets)

    def process_scene(self, scene_description: str) -> dict:
        frame_data = self.frame_input.capture(scene_description)
        detections = self.detection_router.detect(frame_data)
        recognition_result = self.person_recognizer.recognize(frame_data, detections)
        response = self.visual_event_generator.generate(detections, recognition_result)

        return {
            "frame_data": frame_data,
            "detections": detections,
            "recognition_result": recognition_result,
            "response": response,
        }