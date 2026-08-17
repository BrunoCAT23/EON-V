from hardware_interfaces.base_servo import BaseServo
from pi_bindings.pca9685_servo_binding import PCA9685ServoBinding


class RealServo(BaseServo):
    def __init__(self) -> None:
        self.binding = PCA9685ServoBinding()

    def track_face(self) -> None:
        self.binding.track_face()

    def idle_motion(self) -> None:
        self.binding.idle_motion()

    def set_head_position(self, position: str) -> None:
        self.binding.set_head_position(position)

    def get_head_position(self) -> str:
        return self.binding.get_head_position()