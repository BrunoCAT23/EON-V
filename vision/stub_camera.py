class StubCamera:
    def capture(self, scene_description: str) -> dict:
        return {
            "scene": scene_description.strip(),
            "source": "stub_camera",
            "frame": None,
        }