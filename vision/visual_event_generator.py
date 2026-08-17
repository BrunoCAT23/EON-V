class VisualEventGenerator:
    def generate(self, detections: list[dict], recognition_result: dict) -> dict:
        if recognition_result.get("entity_type") == "person":
            name = recognition_result.get("name")
            if name:
                return {
                    "event": f"recognized_face {name}",
                    "text": f"Я бачу {name}."
                }

            return {
                "event": "face",
                "text": "Я бачу людину."
            }

        if recognition_result.get("entity_type") == "pet":
            name = recognition_result.get("name")
            pet_type = recognition_result.get("pet_type", "unknown_pet")

            if name:
                return {
                    "event": f"recognized_pet {name}:{pet_type}",
                    "text": f"Я бачу {name}, це {pet_type}."
                }

            return {
                "event": f"pet_detected {pet_type}",
                "text": f"Я бачу домашнього улюбленця: {pet_type}."
            }

        real_labels = [
            d.get("label") for d in detections
            if d.get("label") != "unknown_object"
        ]

        if real_labels:
            return {
                "event": "face",
                "text": f"Я бачу об'єкти в кадрі: {real_labels}"
            }

        return {
            "event": "no_face",
            "text": "Я нікого не бачу."
        }