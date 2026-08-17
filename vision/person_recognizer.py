class PersonRecognizer:
    def __init__(self) -> None:
        self.known_people = []
        self.known_pets = {}

    def update_known_people(self, known_people: list[str]) -> None:
        self.known_people = [name.lower() for name in known_people]

    def update_known_pets(self, known_pets: dict) -> None:
        self.known_pets = {name.lower(): data for name, data in known_pets.items()}

    def recognize(self, frame_data: dict, detections: list[dict]) -> dict:
        scene = frame_data.get("scene", "").lower()
        pet_detection = None
        person_detection = None

        for detection in detections:
            label = detection.get("label")

            if label in ["cat", "dog"] and pet_detection is None:
                pet_detection = detection

            if label == "person" and person_detection is None:
                person_detection = detection

        for pet_name, pet_data in self.known_pets.items():
            if pet_name in scene:
                return {
                    "recognized": True,
                    "entity_type": "pet",
                    "name": pet_name,
                    "pet_type": pet_data.get("type", "unknown_pet"),
                    "confidence": 0.99,
                    "bbox": None,
                }

        # Pet detection gets priority because movement around pets should be gentler.
        if pet_detection:
            return {
                "recognized": True,
                "entity_type": "pet",
                "name": None,
                "pet_type": pet_detection.get("label"),
                "confidence": pet_detection.get("confidence"),
                "bbox": pet_detection.get("bbox"),
            }

        for person_name in self.known_people:
            if person_name in scene:
                return {
                    "recognized": True,
                    "entity_type": "person",
                    "name": person_name,
                    "confidence": 0.99,
                    "bbox": None,
                }

        if person_detection:
            return {
                "recognized": True,
                "entity_type": "person",
                "name": None,
                "confidence": person_detection.get("confidence"),
                "bbox": person_detection.get("bbox"),
            }

        return {
            "recognized": False,
            "entity_type": "unknown",
            "name": None,
            "confidence": 0.0,
            "bbox": None,
        }
