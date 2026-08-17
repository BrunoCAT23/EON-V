import pytest

from hardware.backend_factory import create_hardware_backend


@pytest.mark.parametrize("backend_name", ["simulation", "mock"])
def test_hardware_backend_contract(backend_name):
    hardware = create_hardware_backend(backend_name)

    assert hardware is not None

    required_methods = [
    "move_forward",
    "move_backward",
    "turn_left",
    "turn_right",
    "stop_motion",
]

    for method_name in required_methods:
        assert hasattr(hardware, method_name), (
            f"{backend_name} backend is missing method: {method_name}"
        )

        method = getattr(hardware, method_name)

        assert callable(method), (
            f"{backend_name}.{method_name} must be callable"
        )

from hardware_interfaces.hardware_backend import HardwareBackend


@pytest.mark.parametrize("backend_name", ["simulation", "mock"])
def test_backend_implements_full_protocol(backend_name):
    hardware = create_hardware_backend(backend_name)

    required_methods = [
        name
        for name, value in HardwareBackend.__dict__.items()
        if callable(value) and not name.startswith("_")
    ]

    missing_methods = [
        name
        for name in required_methods
        if not callable(getattr(hardware, name, None))
    ]

    assert not missing_methods, (
        f"{backend_name} backend is missing HardwareBackend methods: "
        f"{missing_methods}"
    )
