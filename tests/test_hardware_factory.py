import pytest

from brain.core import Brain
from hardware.backend_factory import create_hardware_backend
from hardware.simulation_hardware import SimulationHardware
from hardware.hardware_manager import HardwareManager


def test_simulation_backend_is_created():
    hardware = create_hardware_backend("simulation")

    assert isinstance(hardware, SimulationHardware)


def test_mock_backend_is_created():
    hardware = create_hardware_backend("mock")

    assert isinstance(hardware, SimulationHardware)


def test_brain_accepts_injected_hardware():
    hardware = create_hardware_backend("simulation")
    brain = Brain(hardware_manager=hardware)

    assert brain.hardware_manager is hardware

def test_real_backend_is_created():
    hardware = create_hardware_backend("real")

    assert isinstance(hardware, HardwareManager)


def test_invalid_backend_raises_error():
    with pytest.raises(ValueError):
        create_hardware_backend("unknown")
