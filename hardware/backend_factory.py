from hardware.simulation_hardware import SimulationHardware
from hardware.hardware_manager import HardwareManager


def create_hardware_backend(mode: str = "simulation"):
    mode = (mode or "simulation").strip().lower()

    if mode == "simulation":
        return SimulationHardware()

    if mode in {"mock", "stub"}:
        return SimulationHardware()

    if mode in {"real", "hardware"}:
        return HardwareManager()

    raise ValueError(f"Unsupported hardware backend mode: {mode}")