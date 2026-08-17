from brain.core import Brain
from hardware.backend_factory import create_hardware_backend
import settings

hardware = create_hardware_backend(settings.HARDWARE_MODE)
brain = Brain(hardware_manager=hardware)

while True:
    cmd = input(">>> ")
    brain.process_event(cmd)
    brain.run_all_actions()