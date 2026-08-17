# Legacy Runtime Notes

These root-level modules are older runtime experiments and are not the primary EON-V runtime path:

- `ai_brain.py`
- `listen_ai.py`
- `main_test.py`
- `eyes_system.py`
- `eyes_thread.py`
- `voice_ai.py`
- `wake_word.py`

The current primary path is:

- `main.py`
- `runtime_app.py`
- `brain/`
- `voice/`
- `vision/`
- `hardware/`

The files were not moved because some modules still import them directly. Clean migration should happen in small steps:

1. Replace direct legacy imports with package modules.
2. Add tests or simulations for the replacement.
3. Move the legacy file only after imports are gone.
