from time import monotonic

from settings import (
    MAX_MOTOR_SPEED,
    MAX_SERVO_ANGLE,
    MIN_SERVO_ANGLE,
    MOTION_COMMAND_TIMEOUT,
    MOTION_DRY_RUN,
    MOTION_ENABLED,
)


class EmergencyStop:
    def __init__(self) -> None:
        self.active = False
        self.reason = None

    def trigger(self, reason: str = "manual") -> None:
        self.active = True
        self.reason = reason
        print(f"[EMERGENCY_STOP] Triggered: {reason}")

    def reset(self) -> None:
        self.active = False
        self.reason = None
        print("[EMERGENCY_STOP] Reset")

    def is_active(self) -> bool:
        return self.active


class HardwareSafetyGuard:
    def __init__(self) -> None:
        self.emergency_stop = EmergencyStop()
        self.motion_enabled = MOTION_ENABLED
        self.dry_run = MOTION_DRY_RUN
        self.last_motion_time = None

    def clamp_motor_speed(self, speed: float) -> float:
        return max(0.0, min(float(speed), MAX_MOTOR_SPEED))

    def clamp_servo_angle(self, angle: float) -> float:
        return max(MIN_SERVO_ANGLE, min(float(angle), MAX_SERVO_ANGLE))

    def allow_motion(self) -> bool:
        if not self.motion_enabled:
            print("[SAFETY_GUARD] Motion blocked: motion disabled")
            return False

        if self.emergency_stop.is_active():
            print(f"[SAFETY_GUARD] Motion blocked: {self.emergency_stop.reason}")
            return False

        self.last_motion_time = monotonic()
        return True

    def should_dry_run(self) -> bool:
        return self.dry_run

    def motion_timed_out(self) -> bool:
        if self.last_motion_time is None:
            return False
        return (monotonic() - self.last_motion_time) > MOTION_COMMAND_TIMEOUT

    def status(self) -> dict:
        return {
            "emergency_stop": self.emergency_stop.is_active(),
            "emergency_stop_reason": self.emergency_stop.reason,
            "motion_enabled": self.motion_enabled,
            "dry_run": self.dry_run,
            "motion_timeout_seconds": MOTION_COMMAND_TIMEOUT,
            "motion_timed_out": self.motion_timed_out(),
        }
