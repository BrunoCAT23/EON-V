from __future__ import annotations


def run_diagnostics(brain) -> dict:
    hardware_status = brain.hardware_manager.get_status()
    device_map = brain.hardware_manager.get_device_map()
    safety_guard = getattr(brain.hardware_manager, "safety_guard", None)
    emergency_active = False
    if safety_guard is not None:
        emergency_active = safety_guard.emergency_stop.is_active()

    return {
        "brain": "ok",
        "memory": "ok" if brain.memory_manager.get_robot_profile() else "missing",
        "hardware_mode": hardware_status.get("mode"),
        "devices": list(device_map.keys()),
        "emergency_stop": emergency_active,
        "queued_actions": len(brain.action_queue.snapshot()),
        "autonomous": brain.life_state.is_enabled(),
    }
