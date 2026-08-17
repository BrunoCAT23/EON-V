from hardware_config.pi_pins import PI_INTERFACES, GPIO_MAP
from hardware_config.robot_profile import ROBOT_HARDWARE_PROFILE


DEVICE_MAP = {
    "display": {
        "controller": "DisplayController",
        "interface": PI_INTERFACES["spi_bus"],
        "connection_type": "spi",
        "device_name": "front_face_display",
    },
    "camera": {
        "controller": "VisionPipeline",
        "interface": PI_INTERFACES["camera_interface"],
        "connection_type": "csi",
        "device_name": "main_camera",
    },
    "speaker": {
        "controller": "SpeakerController",
        "interface": PI_INTERFACES["audio_output"],
        "connection_type": "audio",
        "device_name": "voice_output",
    },
    "servo_head": {
        "controller": "ServoController",
        "interface": PI_INTERFACES["i2c_bus"],
        "connection_type": "pca9685_future",
        "device_name": "head_servo_axis",
        "channel": 0,
    },
    "servo_arm": {
        "controller": "ServoController",
        "interface": PI_INTERFACES["i2c_bus"],
        "connection_type": "pca9685_future",
        "device_name": "arm_servo_axis",
        "channel": 1,
    },
    "left_motor": {
        "controller": "MotorController",
        "pins": {
            "in1": GPIO_MAP["motor_driver_in1"],
            "in2": GPIO_MAP["motor_driver_in2"],
            "enable": GPIO_MAP["motor_driver_enable_a"],
        },
        "connection_type": "gpio_motor_driver",
        "device_name": "left_drive_motor",
    },
    "right_motor": {
        "controller": "MotorController",
        "pins": {
            "in1": GPIO_MAP["motor_driver_in3"],
            "in2": GPIO_MAP["motor_driver_in4"],
            "enable": GPIO_MAP["motor_driver_enable_b"],
        },
        "connection_type": "gpio_motor_driver",
        "device_name": "right_drive_motor",
    },
    "robot_profile": ROBOT_HARDWARE_PROFILE,
}