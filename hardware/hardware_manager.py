from hardware.gpio_adapter import GPIOAdapter
from hardware.motor_driver import MotorDriver
from hardware.servo_driver import ServoDriver
from hardware.display_driver import DisplayDriver
from hardware.audio_driver import AudioDriver
from hardware.arduino_bridge import ArduinoBridge
from hardware.hardware_config import HARDWARE_MODE
from hardware.safety_guard import HardwareSafetyGuard


class HardwareManager:
    def __init__(self) -> None:
        self.gpio = GPIOAdapter()
        self.motor_driver = MotorDriver(self.gpio)
        self.servo_driver = ServoDriver(self.gpio)
        self.display_driver = DisplayDriver()
        self.audio_driver = AudioDriver()
        self.arduino_bridge = ArduinoBridge()
        self.safety_guard = HardwareSafetyGuard()

        self.device_map = {
            "gpio": self.gpio,
            "motor_driver": self.motor_driver,
            "servo_driver": self.servo_driver,
            "display_driver": self.display_driver,
            "audio_driver": self.audio_driver,
            "arduino_bridge": self.arduino_bridge,
            "safety_guard": self.safety_guard,
        }

    def get_status(self) -> dict:
        return {
            "mode": HARDWARE_MODE,
            "devices": list(self.device_map.keys()),
            "safety": self.safety_guard.status(),
        }

    def get_device_map(self) -> dict:
        return self.device_map

    def show_emotion(self, emotion: str) -> None:
        self.display_driver.show_emotion(emotion)

    def speak(self, text: str) -> None:
        self.audio_driver.speak(text)

    def track_face(self) -> None:
        if not self.safety_guard.allow_motion():
            return

        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.head_center()
        else:
            self.servo_driver.center()
        print("[HARDWARE_MANAGER] track_face")

    def gentle_track(self) -> None:
        if not self.safety_guard.allow_motion():
            return

        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.head_center()
        else:
            self.servo_driver.center()
        print("[HARDWARE_MANAGER] gentle_track")

    def soft_idle(self) -> None:
        if not self.safety_guard.allow_motion():
            return

        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.head_left()
            self.arduino_bridge.head_right()
            self.arduino_bridge.head_center()
        else:
            self.servo_driver.look_left()
            self.servo_driver.look_right()
            self.servo_driver.center()
        print("[HARDWARE_MANAGER] soft_idle")

    def set_head_position(self, value: str) -> None:
        if not self.safety_guard.allow_motion():
            return

        if HARDWARE_MODE == "arduino_bridge":
            if value == "left":
                self.arduino_bridge.head_left()
            elif value == "right":
                self.arduino_bridge.head_right()
            elif value == "down":
                self.arduino_bridge.head_down()
            else:
                self.arduino_bridge.head_center()
            return

        if value == "left":
            self.servo_driver.look_left()
        elif value == "right":
            self.servo_driver.look_right()
        elif value == "down":
            self.servo_driver.look_down()
        else:
            self.servo_driver.center()

    def idle_animation(self) -> None:
        self.soft_idle()
        print("[HARDWARE_MANAGER] idle_animation")

    def sleep_mode(self) -> None:
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.stop()
            self.arduino_bridge.head_down()
        else:
            self.motor_driver.stop()
            self.servo_driver.look_down()

        self.display_driver.show_text("sleep")
        print("[HARDWARE_MANAGER] sleep_mode")

    def alert(self, text: str) -> None:
        self.audio_driver.beep()
        self.display_driver.show_text(text)

    def move_forward(self, speed: int = 60) -> None:
        if not self.safety_guard.allow_motion():
            return

        speed = int(self.safety_guard.clamp_motor_speed(speed))
        if self.safety_guard.should_dry_run():
            print(f"[HARDWARE_MANAGER] dry-run move_forward speed={speed}")
            return
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.move_forward(speed)
        else:
            self.motor_driver.forward(speed)

    def move_backward(self, speed: int = 60) -> None:
        if not self.safety_guard.allow_motion():
            return

        speed = int(self.safety_guard.clamp_motor_speed(speed))
        if self.safety_guard.should_dry_run():
            print(f"[HARDWARE_MANAGER] dry-run move_backward speed={speed}")
            return
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.move_backward(speed)
        else:
            self.motor_driver.backward(speed)

    def turn_left(self, speed: int = 50) -> None:
        if not self.safety_guard.allow_motion():
            return

        speed = int(self.safety_guard.clamp_motor_speed(speed))
        if self.safety_guard.should_dry_run():
            print(f"[HARDWARE_MANAGER] dry-run turn_left speed={speed}")
            return
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.turn_left(speed)
        else:
            self.motor_driver.turn_left(speed)

    def turn_right(self, speed: int = 50) -> None:
        if not self.safety_guard.allow_motion():
            return

        speed = int(self.safety_guard.clamp_motor_speed(speed))
        if self.safety_guard.should_dry_run():
            print(f"[HARDWARE_MANAGER] dry-run turn_right speed={speed}")
            return
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.turn_right(speed)
        else:
            self.motor_driver.turn_right(speed)

    def stop_motion(self) -> None:
        if HARDWARE_MODE == "arduino_bridge":
            self.arduino_bridge.stop()
        else:
            self.motor_driver.stop()

    def emergency_stop(self, reason: str = "manual") -> None:
        self.safety_guard.emergency_stop.trigger(reason)
        self.stop_motion()

    def reset_emergency_stop(self) -> None:
        self.safety_guard.emergency_stop.reset()

    def ping_arduino(self) -> None:
        response = self.arduino_bridge.ping()
        print(f"[HARDWARE_MANAGER] Arduino response: {response}")

    def cleanup(self) -> None:
        self.arduino_bridge.close()
        self.gpio.cleanup()
