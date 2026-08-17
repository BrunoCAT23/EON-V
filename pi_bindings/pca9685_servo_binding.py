from pi_bindings.pi_env import safe_import


class PCA9685ServoBinding:
    def __init__(self) -> None:
        self.pca_available = (
            safe_import("board")
            and safe_import("busio")
            and safe_import("adafruit_pca9685")
        )
        self.head_position = "center"

    def track_face(self) -> None:
        self.head_position = "tracking"

        if self.pca_available:
            print("[PCA9685_SERVO_BINDING] Real face tracking via PCA9685")
        else:
            print("[PCA9685_SERVO_BINDING_STUB] Would track face")

    def idle_motion(self) -> None:
        self.head_position = "idle_scan"

        if self.pca_available:
            print("[PCA9685_SERVO_BINDING] Real idle servo motion")
        else:
            print("[PCA9685_SERVO_BINDING_STUB] Would perform idle motion")

    def set_head_position(self, position: str) -> None:
        self.head_position = position

        if self.pca_available:
            print(f"[PCA9685_SERVO_BINDING] Real servo set position: {position}")
        else:
            print(f"[PCA9685_SERVO_BINDING_STUB] Would set servo position: {position}")

    def get_head_position(self) -> str:
        return self.head_position